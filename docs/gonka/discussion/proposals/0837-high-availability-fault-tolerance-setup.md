---
title: "#837 — High-availability / Fault-tolerance Setup"
source: https://github.com/gonka-ai/gonka/discussions/837
discussion_number: 837
category: proposals
synced_at: 2026-06-27T19:46:35Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #837](https://github.com/gonka-ai/gonka/discussions/837) каждые 6 часов. 

# High-availability / Fault-tolerance Setup

**Автор:** [@blizko](https://github.com/blizko) · **Категория:** :bulb: Proposals · **Создано:** 2026-03-02 12:38 UTC · **Обновлено:** 2026-03-03 11:47 UTC

---

## 📝 Описание

### High-availability / Fault-tolerance Problem
In the current deploy architecture, we have a bottleneck that a single issue with a `node` or `api` container can lead to failure of a multitude of MLNodes.
There is a real need for redundancy in all parts of the system.

Current architecture of deploy has essentially a single instance of node container per api container 
Any failures or lags of `node` containers (due to any reason like like overloading / hardware issue / ddos / etc) of `api` container essentially can easily lead to exclusion and miss of full reward per epoch for this validator
Examples include already observed network events, such as - Request DDOS, `chain-rpc` attacks
Even small lags of node container of active validator lead to inability to sign blocks => node becomes jailed and might be slashed 

### Node Instance problem
In current default deployment, a single instance of a chain node (`node` container) is responsible for both:
- producing and signing blocks, used for reading data from the blockchain by api container 
- also used for `/chain-api`, `/chain-rpc` requests from the final users. 

Essentially, if any of the requests from users of the `api` container is heavy enough (or if there are a lot of them), it directly affects the performance of processing data from other peers (by any limits like CPU / disk IO, etc.). Which causes lags (nodes can’t be in sync with the chain) but also it doesn’t sign blocks in time which might cause the whole chain slow downs.
Which essentially happened on the chain during last months. 

Ideally, user requests must never directly hit the instance of the `node` container which produces and signs blocks. In the same way they should not be able to affect the instance which is used by api to get the latest data from the chain.

**Sentries architecture**

There is a well known solution to hide validators from direct access (both any APIs and P2P connections with other nodes to minimize chances of DDOS) called Sentry Deploy

Essentially the idea is to have several read-only (sentry) nodes, which communicate with the network and are visible for everyone but they don’t actively participate in the blocks producing / signing 
The validator itself, which is responsible for producing and signing blocks lives in the internal network and doesn’t have public IP at all / any ports opened. Usually, such a node has all APIs disabled and also has disabled snapshots, it prunes everything and doesn't make any indexation. The goal is to achieve optimal performance for such containers.

Originally, that means any potential transactions which are gossiped to its mempool will be going through one of the Sentry nodes and will be rejected in advance if there are any significant issues in them.

**Sentries + Cluster** 

The Sentry architecture is focused on protecting the validators mempool and does not take into account that `api` container must have access to up-to-date chain’s state and must also not be affected by any external requests. 

### Node enhancement proposal

Based on this we propose architecture for the deployment of cluster, which uses the idea of Sentry node but additionally explicitly separates the instances which can be accessed externally (and their failures must not affect the whole validator) and the ones which are critical and should never be exposed. We’re trying to do this in a way when bigger nodes can add more instances / redundancy to handle more traffic.

The proposal suggests to use 2 pools of node instances:

**1. Public Sentries** 
This is exactly the same idea of sentry nodes, which are used as a shield to protect validators. They all can have some short history of snapshots to still keep disk usage relatively low.
Only some of them should have enabled `/chain-api` and `/chain-rpc` and be available for user requests, (the user request can be redirected by load balancers to the node with enabled one). 
Snapshots are stored only on such nodes. 

**2. Private Cluster** 
The private cluster lives in an internal network and uses all public sentries as persistent peers. Nodes in the private cluster don’t have public interfaces and accept requests only from each other, sentry nodes and `api` container(-s).
One of the nodes in Private Cluster is an active Validator for this host, it doesn’t have direct access to Consensus Key and sign blocks using signer (tmkms). 
Host can’t have multiple Validator nodes at the same time to avoid double-signing by the same Consensus Private key. But if the Validator has any technical issues, any other nodes from the Private Cluster can be promoted to be the Validator. The promotion includes stopping the previous active validator and re-connect TMKMS (which has the Consensus Private Key) from the old one to the new one. 
**Note - The switchover itself is a point of failure. Additional health-checks and automation should be considered.**

All private validators store only short latest history of states, don’t make snapshots and have aggressive pruning enabled

The `api` container get’s all data only from private nodes, they are considered to be up to date as long as at least one sentry node is in sync. If some of nodes in private nodes becomes unavailable, api container switches to the next available node

**Note** - A separate enhancement is in `api` component to ensure that multiple nodes are used instead of one (One of the issues is not only the fact of unavailability, but also synchronisation state of nodes. The "catching-up" state of the node does not accurately represent the status. Thus, a check should be performed on the "freshness" of data. E.g. `last_block_time > time()-10s`)

Both Public Sentries and Private Cluster can potentially be re-used if the same owner maintaining several independent validators (several consensus keys)

### Api Instance problem
Currently, a single api instance is responsible for:
- MLNode management
- POC procedure 
- Inference Validation 
- User’s request execution 

And if an instance has any issues due to the amount of inferences from the client, it can directly affect participating in POC and lead to validator exclusion and missing reward.
In addition - The PoC design currently expects that a single callback endpoint exists. It is also expected that a single instance is used to send PoC / validation artifacts to the network.

### API enhancement proposal
There is no hard limitation to have only one `api` container at the time. Roles of the `api` container can be separated to - MLNode / POC Manager, vs Public Inference. Idea is to never expose Manager externally, but have automatic scaling of the roles which handles client inference requests (since requests are stateless and there is no requirement on request “stickyness”)

**The MLNode / POC Manager component.**
Two distinct solutions can be considered:
**_Solution 1 (Infrastructure level fault resolution)_**
Introduce multiple containers that reside under the same Virtual IP (single callback endpoint)

Pros:
- Fairly easy to implement

Cons:
- Synchronisation of state might be required between `api` containers to ensure that no double requests are sent to MLNodes (PoC mechanism in MLNode is known to refuse double requests)
- During failover callback requests might silently fail (requires inspection of the retry mechanism in MLNode)

**_Solution 2 (Application level fault resolution)_**
The POC Manager can follow a “Primary / replica” approach and have a “connection pool” defined as callbacks for MLNode. The API nodes select/vote for a “primary” manager that is used to handle PoC requests. In case of failure, api nodes re-elect the “primary” manager to handle requests.
In such case - The MLNodes are free to publish PoC and validation results to any API container from the connection pool.

Pros:
- Ensures that messages are sent “no more than once”

Cons:
- Requires implementation of primary election / callback endpoint management.
- Might require an additional layer for caching.

Notes on both solutions: 
- To evaluate if there are cases when results are “collected/batched”. If results are not instantly forwarded, but stored for any period of time - a separate caching layer (e.g. Redis) can be used.
- A “hook” mechanism is preferred for api to retrieve information from the chain about phases (e.g. transition to PoC phase) instead of constant node polling.

### References
- https://tutorials.cosmos.network/tutorials/9-path-to-prod/5-network.html#ddos 
- https://docs.zigchain.com/nodes-and-validators/sna-guide


---

## 💬 Комментарии (3)

### Комментарий 1 — [@blizko](https://github.com/blizko)

*2026-03-02 14:39 UTC*

![2026-03-02 15 32 17](https://github.com/user-attachments/assets/3de4803c-1238-4081-be8c-02662e12c20a)
Initial Sentry network design by @gmorgachev 

### Комментарий 2 — [@sysmanalex](https://github.com/sysmanalex)

*2026-03-03 09:04 UTC*

I believe that nodes: 

- a) serving user/guest requests/web access the public internet 
- b) nodes that process data 
should be separated from the start. This will solve a ton of problems at once, increasing net/core-functional nodes performance. 
separating them from public, low prio functions, there high-load can be easy balanced without locking/impacting functional core-net nodes.
Artur/Gleb offering Nginx-Balancer schema - still weak point on single entry block/ddos + more elements.
two nodes with separate addresses, functions much simpler. 

suggested optimisation / high-load ready for RPC, API, JSON and HTTP requests in the Gonka project.
- 1st please shorten all long field names to compact formats in body-load (less body help more vs long + compress, shorter tcp less windows, less load on network side/cpu).

Replace verbose keys: "prompt" → "p", "max_tokens" → "mt", "model_id" → "m", "chain-rpc" → "cr", "inference" → "i"
check "/chain-api/productscience/inference/inference/models_stats_by_time" - 67 chars vs "/ci/p/i/mst" - 12 chars. 

especially for non-human/nodes interactions. cutting 5-10-25 char on 1000 operations saving a lot on scale,
even without using protobuf,gzip, JSON minification. 
- same for all logs, long line wrote 5x more blocks.
Smaller payloads often leading 4–5+x reduction vs. JSON/gzip.
- JSON minification / remove all unnecessary whitespace and line breaks from JSON payloads. In Go, use a custom json.Encoder with SetEscapeHTML(false) and no indentation.
Savings: 10–30% on large objects
- Enable transport-level compression
Add gzip or Brotli compression to all HTTP responses and requests in the API node handlers (in Go). This typically reduces JSON size by 60–80% for text-heavy payloads like prompts.
- Migrate REST → gRPC (or support both)
gRPC uses Protobuf (binary, 50–70% smaller than JSON). Expose the same endpoints via gRPC in addition to REST.
- Enable per-message compression / gRPC natively supports gzip, deflate, or zstd. Turn it on for all calls.
- Batch multiple requests !
Combine several inference/validation jobs into one gRPC call
- streaming for long inference responses ? 
- check all for Cosmos SDK-based blockchain with Tendermint RPC on port 26657, gRPC support ! 
SDK not tuned/ far from optimal for Gonka.
- Upgrade to IAVL rewrite / IAVLX ~ 30x faster then classiv iavl v1 on write + faster commits, performance. !!!
https://www.cosmoslabs.io/blog/the-cosmos-stack-roadmap-2026

- ADR-065 / ss/sc layers check here 
 https://github.com/cosmos/cosmos-sdk/blob/main/docs/architecture/adr-065-store-v2.md
 - btw + worth to add client-side caching layers (e.g., tools like cosmos-cache middleware) for repeated /status, /block, /validators queries - sync via Tendermint events.
(please test first). 
- Tune more CometBFT config: increase mempool size (not max, just a little bit), adjust timeouts, enable resonable snapshots/pruning.

should bring on table 70-90% reduction in transfer size/tcp/cpu/processing load + latency/perf.

 Inference related next step.
- Pre-compress prompts client-side
- Clients can gzip/brotli the prompt text before sending (especially useful for very long contexts).
- prompt references/hashing/deduplication.

[!TIP]
json go parse acceleration, Gonka using STD json parse RPC-handlers, cosmosclient, types/serialization.
suggestion accelerate std (1-2Gb/parse) to json-simd 6-14+GB parse, simdjson 4.3, sonic, 
import "encoding/json" на import json "github.com/goccy/go-json" - 2-3x speed up, simplest compatibility.

Json-iterator/go: 2-3x faster than std, non-SIMD, compatible. For simple cases.
Buger/jsonparser: Parse-only, 5-6x faster on specific data (e.g., extract fields without full unmarshal). Benchmark: 9811 ns/op vs. 55931.
Easyjson: Codegen (generates marshal/unmarshal for structs) -> 2-4x speedup. Suitable for types in x/inference


### Комментарий 3 — [@Laboltus](https://github.com/Laboltus)

*2026-03-03 09:23 UTC*

>The MLNode / POC Manager component.

Why can't we just set multiple URLs in POC callback url and MLnodes will try them one by one ? Retry logic is already implemented, so it could be minor fix.

**↳ Ответ от [@blizko](https://github.com/blizko)** · *2026-03-03 11:47 UTC*

> One of the side effects here is due the state of the system that is handled by the `api` container.
> As an example - health checks of MLNodes + state transitions of MLNodes.
> Performing raw horizontal scaling of MLNodes might cause a conflict in case the state is not in sync. E.g one `api` node will invoke the PoC phase, while the second instance will send a PoC stop signal.

---
title: "#887 — Gonka.gg - Explorer, Analytics Platform, Data Provider for Gonka"
source: https://github.com/gonka-ai/gonka/discussions/887
discussion_number: 887
category: show-and-tell
synced_at: 2026-06-21T14:33:59Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #887](https://github.com/gonka-ai/gonka/discussions/887) каждые 6 часов. 

# Gonka.gg - Explorer, Analytics Platform, Data Provider for Gonka

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-03-13 21:23 UTC · **Обновлено:** 2026-03-14 01:18 UTC

---

## 📝 Описание

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/77yTDB4x9hoLewm.png)

When we launched gonka.gg on **December 12, 2025** ([read the pre-story](https://github.com/gonka-ai/gonka/discussions/880)), our goal was simple: give Gonka users a reliable place to verify their transactions. What happened next surprised even us. 

The community responded immediately and enthusiastically. Within weeks, it was clear that a transaction explorer was just the beginning. A lot of feature requests started to pour in - deeper analytics, network visibility, tools, and ways to understand the AI inference layer that makes Gonka unique. So we kept building.

Today, **gonka.gg serves ~1,000 unique visitors daily and handles ~1.2 million requests per day** - a testament to what results can be achieved if product is built with community support.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/9ATn3BgWrkqQIbg.png)

*(Analytics page screenshot. Hits = route requests; visitors = unique people who visited that day. Data is for the last 14 days as of 13th of March).*

Bellow is what gonka.gg is today

***

### Blockchain Explorer

The core of gonka.gg - search and inspect anything on the Gonka blockchain:

- [Blocks](https://gonka.gg/blocks) - browse the full block history, inspect individual blocks and their contents
- [Transactions](https://gonka.gg/transactions) - search by hash, filter by type, view full decoded transaction details
- **Addresses & Wallets** - full account profiles with native GNK balances, IBC token holdings, vesting schedules, and complete transaction history
- **Universal Search** - type anything (block height, tx hash, wallet address, participant name) and the explorer figures out what you're looking for

***

### Network Analytics

A live, deep-dive view into the Gonka network:

- [Network Overview](https://gonka.gg/network) - epoch stats, GPU distribution treemap, weight charts, and network growth over time
- [Participants](https://gonka.gg/network/participants) - browse all network participants with filtering by GPU type, jailed status, and health. Each participant has a dedicated profile page with GPU details, epoch history, rewards summary, inference health, wallet balance, and slashing events
- [GPU Breakdown](https://gonka.gg/network/gpus) - see every GPU model running on the network and how compute is distributed
- [Inference Activity](https://gonka.gg/network/inference) - live and historical AI inference request charts, model distribution, and request counts per epoch
- [Governance Proposals](https://gonka.gg/network/proposals) - active and past on-chain governance proposals with full vote breakdowns
- [Community Fund](https://gonka.gg/network/community-fund) - community treasury pool balance and all historical distributions
- [Token Holders](https://gonka.gg/network/token-holders) - GNK token holder distribution, total supply info, and a rolling 90-day account growth history
- [Slashing Events](https://gonka.gg/network/slashing) - full history of slashing and penalty events, searchable by participant

_And more features available in the menubar of the gonka.gg (and much more to come)!_
***

### Inference map: The Live Inference Globe

[Inference Map](https://gonka.gg/network/inference-map) - a 3D interactive globe showing live AI inference request arcs flowing between nodes across the world in real time. It makes the distributed nature of Gonka's AI network immediately tangible.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/7k38ZZ7m6wM6Qo3.png)

***

### Tools & Utilities

- [Rewards Calculator](https://gonka.gg/reward-calculator) - estimate your epoch rewards based on your GPU weight and current network stats
- [Faucet](https://gonka.gg/faucet) - claim free GNK tokens (Google OAuth + reCAPTCHA, 0.1 GNK / 24h cooldown)
- [Node Tracker](https://gonka.gg/track/nodes) - a personal miner tracking dashboard. No account needed - uses a unique matrix-based auth. Create lists of nodes to monitor, add notes, and share lists with others (with optional password protection)

Each tool is a result of community request from out Telegram chat.

***

### AI Assistant

An embedded AI chat widget powered by the Gonka LLM network itself (via proxy.gonka.gg). Ask questions about the network, transactions, participants - the assistant has direct access to the explorer's internal data and answers in real time.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/qmAhmrl7B2oE7n6.png)

***

### Public API

We aggregate data, thus it is our responsibility to share it to the community, so recently we launched [free public API](https://gonka.gg/public-api/auth) - anyone can register and one-click issue an API key and get access to network stats, transactions, participants, epoch data, and more. Anyone building on Gonka can use it without running their own indexer, all for free.



***

### What's Under the Hood

Handling 1M+ daily requests reliably requires purpose-built infrastructure. We didn't just wire up RPC nodes and call it done - every layer was designed specifically for potential scale and unique demands of the Gonka network.

- **ClickHouse** for high-speed transaction indexing (we have billions of events and txs handled by clickhouse)
- **Redis** as the primary cache layer for fast response times.
- **PostgreSQL** for persistent data (tracking, faucet, API users)
- A **dynamic RPC pool** that discovers all participant nodes as fallback endpoints
- Background services that continuously materialize network snapshots, GPU stats, epoch timing, and community fund data - refreshing every 30 seconds to 10 minutes depending on the data type (background service fetches data from blockchain, stores it to the DBs, then data gets picked up by Redis and get redistributed accross uvicorn workers, thus guaranteeing that users will get data FAST (right from RAM storred snapshot) and accurate (workers sync their states from Redis snapshots)).

**Key parts are opensourced:**

1. ***Transaction Indexing -***  [tx-scanner](https://github.com/gonkalabs/tx-scanner) ***(open source, Go)***

   The backbone of all transaction data on gonka.gg. Rather than relying on the standard (and notoriously unreliable) Cosmos tx_search RPC, tx-scanner reads `block_results` directly. It scans bidirectionally: forward for new blocks and backward to fill historical data simultaneously, using a configurable concurrent worker pool for parallel block processing and batch ClickHouse inserts for maximum write throughput. The result: sub-500ms API responses across hundreads of millions indexed rows, with live RPC fallback for any transaction not yet indexed. Designed for Gonka (but compatible with any CometBFT-based chain).

2. ***RPC Reliability -***  [rpc-pooler](https://github.com/gonkalabs/rpc-pooler) ***(open source, Python)***

   Public RPC nodes are constantly withstanding loads and might sometimes be flaky. RPC-pooler solves this with a single URL that transparently routes every request to the fastest healthy node from a *dynamically maintained pool* (it auto-discovers participant nodes from the network's own participant list and uses them as fallbacks for appropriate RPC requests). Three routing strategies handle different request types: parallel fastest-first for reads (fires to top 3 nodes simultaneously, returns first success), sequential failover for consensus queries, and broadcast to all healthy nodes for transaction submissions. Every node gets a composite health score factoring in success rate, response time, sync status, and circuit breaker state. The result: near-zero downtime for the explorer even when individual nodes fail.


`Average response time across all endpoints: ~159ms.`

***

## Recent big change

Recently we switched to the clickhouse for transaction querying on the wallet / account details page. This was possible because we accumulated over 6 billion events in the DB (effecting in 159 million unique transactions) since december 2025. This simple change allowed us to cut transactions listing time on the page from 15+ seconds (direct RPC requests) to ~1 second on average.

All this data is already available in [public API.](https://gonka.gg/public-api/auth)

### What's Next

We're continuing to iterate fast and constantly upgrading and fixing bugs. This is a never ending proccess, because there is always room for improvement. If there's a metric, view, or tool you need - tell us and we will be more then happy to implement it!

[gonka.gg](https://gonka.gg) | [GitHub](https://github.com/gonkalabs) | [gonkalabs.com](https://gonkalabs.com)

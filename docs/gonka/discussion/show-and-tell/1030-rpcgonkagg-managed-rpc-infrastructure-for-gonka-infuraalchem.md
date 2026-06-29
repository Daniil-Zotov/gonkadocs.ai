---
title: "#1030 — rpc.gonka.gg - Managed RPC Infrastructure for Gonka (Infura/Alchemy for Gonka) with opensource core"
source: https://github.com/gonka-ai/gonka/discussions/1030
discussion_number: 1030
category: show-and-tell
synced_at: 2026-06-29T11:24:27Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1030](https://github.com/gonka-ai/gonka/discussions/1030) каждые 6 часов. 

# rpc.gonka.gg - Managed RPC Infrastructure for Gonka (Infura/Alchemy for Gonka) with opensource core

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-04-08 10:22 UTC · **Обновлено:** 2026-04-08 10:24 UTC

---

## 📝 Описание

Two days ago we sped up [gonka.gg](https://gonka.gg) by 100x.

Today we are making the technology behind that speedup available to everyone.

Meet [rpc.gonka.gg](https://rpc.gonka.gg) - managed RPC infrastructure for the Gonka blockchain, built by [Gonka Labs](https://gonkalabs.com).

We give developers reliable, authenticated API access to the entire Gonka blockchain through a single URL - no need to run your own nodes. The service acts as a bridge for applications (dApps, wallets, exchanges, bots, AI agents) to interact with the network: send transactions, read any data, query indexed history, and more.

This is Infura / Alchemy, but for Gonka.

**Live now:** [rpc.gonka.gg](https://rpc.gonka.gg)

<img width="1413" height="867" alt="Screenshot 2026-04-08 at 12 25 11" src="https://github.com/user-attachments/assets/185a6e7d-db03-40bb-b13a-73c0c9bb42b5" />




## Why we built this

When we were developing [gonka.gg](https://gonka.gg), we hit the same wall every Gonka developer hits (and developers dm'ed us numerous times, asking if we can help solve the issues): the genesis RPC nodes are shared, sometimes slow under load, and running your own full node is a project in itself - hours/days of syncing, multiple ports, ongoing maintenance: not everyone wants to tackle all of that.

We needed something fast, with smart caching, with indexed data. So we built it for ourselves (gonka.gg explorer) and developers struggling with the same issues, so - virtually for everyone interested in building on Gonka. gonka.gg switched to rpc.gonka.gg as its data-backend, and the results were immediate: wallet transaction history pages went from 15+ seconds to under 1 second. Once we saw the difference, the natural next step was to open it up so every developer in the ecosystem gets the same infrastructure.

## What you get

| Feature                    | Details                                                                                                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **400+ API endpoints**     | CometBFT RPC, Cosmos REST/LCD, Gonka custom API, ClickHouse-indexed data - all through one base URL                                                                              |
| **6 API surfaces**         | Chain RPC (`/chain-rpc/*`), Cosmos REST (`/chain-api/*`, `/cosmos/*`), Gonka API (`/v1/*`), Fast indexed data (`/api/ch/*`), CometBFT passthrough (`/comet/*`), Developer portal |
| **Transaction broadcast**  | Send transactions through our RPC - full broadcast support via LCD `POST .../txs` and CometBFT `broadcast_tx_*`                                                                  |
| **Fast indexed queries**   | `/api/ch/*` endpoints powered by ClickHouse - **4 to 110x faster** than equivalent traditional RPC queries. More on this below                                                   |
| **Authenticated access**   | Per-key rate limits, monthly quotas, abuse protection. No open nodes leaking resources                                                                                           |
| **inferenced CLI support** | The official Gonka CLI connects directly - just embed your API key in the URL path                                                                                               |
| **AI agent support**       | Machine-readable docs at `/llms.txt` and `/api/endpoints`. Your AI agent discovers everything automatically                                                                      |
| **Full documentation**     | Every single endpoint documented with method, path, description, and parameters                                                                                                  |

## Fast indexed data - `/api/ch/*`

This is one of the most important things rpc.gonka.gg offers, and the main reason gonka.gg got 100x faster.

Standard Cosmos RPC was not designed for analytical queries. Want a wallet's transaction history? You call `tx_search`, which is notoriously slow and unreliable on busy nodes. Want all transactions in a block? Multiple calls. Want slashing events across the network? Good luck.

rpc.gonka.gg solves this with a set of **pre-built, ClickHouse-backed endpoints** under `/api/ch/*`. These are not proxied RPC calls - they hit our hosted [tx-scanner](https://github.com/gonkalabs/tx-scanner) ClickHouse instance directly, where billions of events and hundreds of millions of transactions have been indexed (we have data since Genesis Block and constantly updating - when new block is generated, it is immidiately ingested). The same dataset that powers [gonka.gg](https://gonka.gg).

The results are **4 to 110 times faster** than the equivalent traditional RPC queries on genesis nodes:

| Endpoint                        | What it does                                                                                                       | Speed vs raw RPC    |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------- |
| `GET /api/ch/tx/{hash}`         | Single transaction by hash (64-char hex, optional 0x prefix)                                                       | ~4-20x faster       |
| `GET /api/ch/block/{height}`    | All transactions in a block, with count                                                                            | ~5-35x faster       |
| `GET /api/ch/blocks?limit=N`    | Recent blocks with tx counts                                                                                       | ~10-90x faster      |
| `GET /api/ch/blocks/latest`     | Latest indexed block                                                                                               | near-instant        |
| `GET /api/ch/address/{address}` | All successful txs where address is sender or recipient. `?limit=` (default 5, max 100), `?offset=` for pagination | **~20-110x faster** |
| `GET /api/ch/slashing`          | Slashing and penalty events across the network                                                                     | ~10-50x faster      |
| `GET /api/ch/hardware`          | Hardware stats across network participants                                                                         | ~10-35x faster      |
| `GET /api/ch/epochs`            | Epoch performance and reward data                                                                                  | ~5-20x faster       |

These endpoints return clean JSON. No parsing Cosmos SDK protobuf responses, no chasing pagination cursors across multiple RPC calls. The data is pre-indexed, pre-joined, and served from ClickHouse columnar storage optimized for exactly these access patterns.

When gonka.gg was loading a wallet's transaction list via standard `tx_search` RPC, it took 15+ seconds per page (and sometimes even then failed at timeout). After switching to `/api/ch/address/{addr}`, the same page loads in under 1 second. This is the same speedup every developer building on Gonka now gets access to through rpc.gonka.gg.

## How it works

### Feather - our custom Opensource RPC node

Behind rpc.gonka.gg is a pool of our custom RPC nodes called **Feather**.

Feather is a light full-RPC node for Gonka. It runs the complete chain node (chain + REST + API) without the ML node, and adds a ClickHouse-backed analytics and indexing layer on top. And, it is built around inferenced, so applying new features from inferenced node is pretty straightforward.

<img width="1583" height="1059" alt="Screenshot 2026-04-08 at 12 28 16" src="https://github.com/user-attachments/assets/798827b2-860d-4f3c-9d64-78fd0725208a" />



What Feather does:

- **Full RPC surface** - every endpoint a real Gonka participant exposes, unified behind a single gateway port
- **Intelligent caching** - immutable data (historical blocks, finalized transactions) cached for 24 hours. Live state refreshes every 1-3 seconds. Your app feels instant without serving stale data
- **ClickHouse indexer** - every block, transaction, and event indexed for analytical queries
- **Enhanced analytics API** - tx search by sender/type/time range, token usage by model, developer stats, epoch summaries
- **P2P node** - syncs directly from Gonka mainnet peers, fully self-sovereign
- **Built-in dashboard** - real-time monitoring of sync status, peers, endpoints, indexer progress, and traffic
- **Written in Go** - small footprint, fast startup, Docker-based deployment

Also, Feather gives access to cometBFT instrumentation and much more, we will go indepth on that product in the later post.

Following our open source strategy, **we will be open-sourcing the Feather node code** for anyone who wants to run it on their own servers. We mentioned this during the recent AMA - Feather will be published at [github.com/gonkalabs](https://github.com/gonkalabs) alongside our other open source projects. In addition, we will post a new indepth article about it!

### rpc.gonka.gg - the gateway layer

On top of the Feather pool sits our public **rpc service** layer - the public-facing gateway that adds:

- API key authentication and rate limiting
- Per-key usage tracking and monthly quotas
- CORS handling for browser-based apps
- Path-based API key auth for CLI tools that cannot set custom HTTP headers
- The `/api/ch/*` fast indexed endpoints (ClickHouse queries for transactions, blocks, addresses, slashing, hardware, epochs)
- The developer portal, documentation site, health monitoring, and pricing pages

Together, Feather + rpc-service layer form the complete stack - everything between your app and the Gonka blockchain.

### tx-scanner - the indexing backbone

The ClickHouse data behind `/api/ch/*` is populated by [tx-scanner](https://github.com/gonkalabs/tx-scanner) (open source, Go). Rather than relying on the standard (and notoriously unreliable) Cosmos `tx_search` RPC, tx-scanner reads `block_results` directly. It scans bidirectionally: forward for new blocks and backward to fill historical data simultaneously, using a configurable concurrent worker pool for parallel block processing and batch ClickHouse inserts for maximum write throughput.

The result: billions of events and hundreds of millions of transactions indexed and queryable in milliseconds. The same indexer powers [gonka.gg](https://gonka.gg) - when you call `/api/ch/address/gonka1...` on rpc.gonka.gg, you are querying that full dataset.

tx-scanner is designed for Gonka but compatible with any CometBFT-based chain. Source: [github.com/gonkalabs/tx-scanner](https://github.com/gonkalabs/tx-scanner)

## Getting started

**Step 1.** Go to [rpc.gonka.gg/access](https://rpc.gonka.gg/access) and sign up. Your free API key is ready instantly.

**Step 2.** Use your key in requests:

```bash
# Header-based auth (for apps, scripts, CosmJS)
curl -H "X-Api-Key: YOUR_KEY" https://rpc.gonka.gg/chain-rpc/status

# Path-based auth (for inferenced CLI and tools that cannot set headers)
curl https://rpc.gonka.gg/key/YOUR_KEY/chain-rpc/status

# Fast indexed query - get a wallet's transactions in milliseconds
curl -H "X-Api-Key: YOUR_KEY" https://rpc.gonka.gg/api/ch/address/gonka1...?limit=20
```

**Step 3.** That is it. Replace your node URL and start building.

### Works with inferenced CLI

The official Gonka blockchain CLI connects directly to rpc.gonka.gg. No custom headers needed - the key is embedded in the URL path:

```bash
# Check node status
inferenced status --node https://rpc.gonka.gg/key/YOUR_KEY/

# Query balances
inferenced query bank balances gonka1... --node https://rpc.gonka.gg/key/YOUR_KEY/

# Send tokens
inferenced tx bank send mywallet gonka1... 1000ngonka \
  --node https://rpc.gonka.gg/key/YOUR_KEY/ \
  --chain-id gonka-mainnet --yes
```

Full JSON-RPC POST support - `status`, `query`, `tx` commands all work out of the box.

### Works with AI agents

Point your AI agent at `https://rpc.gonka.gg/llms.txt` and it will discover all available endpoints automatically. We also serve structured JSON at `/api/endpoints` and a detailed reference at `/llms-full.txt`. There is a dedicated page explaining the integration: [rpc.gonka.gg/agents](https://rpc.gonka.gg/agents).

## Note about gonka.gg

The whole gonka.gg explorer and its services talk DIRECTLY to rpc.gonka.gg under the hood. Our exploreres backend was fully redisigned and now talks to rpc.gonka.gg directly without hitting genesis RPC nodes (node1, node2, etc) under one unified API key:

<img width="863" height="483" alt="Screenshot 2026-04-08 at 12 34 45" src="https://github.com/user-attachments/assets/9bc20e6f-f2e2-409e-b65c-8438cff1c57f" />

## Documentation

We prepared documentation for all 400+ API methods - identical to genesis nodes, plus the additional `/api/ch/*` fast indexed endpoints. Every endpoint is listed with its HTTP method, path, description, and parameters.

<img width="1314" height="1030" alt="Screenshot 2026-04-08 at 13 21 09" src="https://github.com/user-attachments/assets/1744680f-7cf2-437c-85f9-7141e47138a7" />


Full docs: [rpc.gonka.gg/endpoints](https://rpc.gonka.gg/endpoints)

There is also a dedicated section for AI agents at [rpc.gonka.gg/agents](https://rpc.gonka.gg/agents) - just give the link to your AI and it will learn how to use Gonka.

## What this means for developers

Before rpc.gonka.gg, building on Gonka meant either using the shared genesis nodes (may be slow due to high demand) or setting up your own full node (hours/days of syncing, ongoing maintenance, multiple ports to manage).

Now there is a managed service purpose-built for Gonka. One URL, one API key, 400+ endpoints, and indexed data that returns in milliseconds instead of seconds.

If you are building a dApp, a bot, a monitoring tool, an explorer, a wallet integration, or anything that talks to the Gonka blockchain - this is the fastest way to get there.

## P.S:
We will be constantly monitoring the feedback and fix, upgrade the code. In case of any issue - feel free to write in our TG chat (gonka_gg)

## Links

- **Service:** [rpc.gonka.gg](https://rpc.gonka.gg)
- **Documentation:** [rpc.gonka.gg/endpoints](https://rpc.gonka.gg/endpoints) (400+ endpoints)
- **Developer portal:** [rpc.gonka.gg/access](https://rpc.gonka.gg/access)
- **AI agent docs:** [rpc.gonka.gg/agents](https://rpc.gonka.gg/agents)
- **Health monitor:** [rpc.gonka.gg/health](https://rpc.gonka.gg/health)
- **tx-scanner (open source):** [github.com/gonkalabs/tx-scanner](https://github.com/gonkalabs/tx-scanner)

### Previous Gonka Labs posts

- [Gonka Contract Playground - write, compile, simulate, and deploy CosmWasm without leaving the browser](https://github.com/gonka-ai/gonka/discussions/989)
- [GG Wallet - An Open-Source Browser Wallet strictly for Gonka](https://github.com/gonka-ai/gonka/discussions/938)
- [Gonka Name Service (GNS) - Human Readable names for the Gonka Network](https://github.com/gonka-ai/gonka/discussions/898)
- [OpenGNK - A Local OpenAI-Compatible Proxy for Gonka](https://github.com/gonka-ai/gonka/discussions/890)
- [Gonka.gg - Explorer, Analytics Platform, Data Provider for Gonka](https://github.com/gonka-ai/gonka/discussions/887)
- [Gonka Labs: How We're Building the Infrastructure for Gonka](https://github.com/gonka-ai/gonka/discussions/880)

**About us:** [gonkalabs.com](https://gonkalabs.com) | **Explorer:** [gonka.gg](https://gonka.gg) | **GitHub:** [github.com/gonkalabs](https://github.com/gonkalabs)

---
title: "#989 — Gonka Contract Playground - write, compile, simulate, and deploy CosmWasm without leaving the browser"
source: https://github.com/gonka-ai/gonka/discussions/989
discussion_number: 989
synced_at: 2026-06-15T18:13:37Z
---

> 🔄 **Авто-синхронизация:** из [GitHub Discussion #989](https://github.com/gonka-ai/gonka/discussions/989) каждые 6 часов. Прямые правки будут перезаписаны.

# Gonka Contract Playground - write, compile, simulate, and deploy CosmWasm without leaving the browser

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-03-31 22:32 UTC · **Обновлено:** 2026-03-31 22:32 UTC

---

## 📝 Описание


<img width="1598" height="818" alt="Снимок экрана 2026-04-01 в 01 25 50" src="https://github.com/user-attachments/assets/a60cac40-16b6-4c74-ba2a-fa20f1b28ba5" />

## Motivation

Building smart contracts is, usually, a pain - it keeps coming up: you want to try a small contract idea, poke at something already deployed, or show a teammate how a message works - and you end up juggling a local Rust toolchain, `wasmd`, scripts, and RPC URLs before you even get to "does this `execute` do what I think?"

We already ship [gonka.gg](https://gonka.gg) for reading the chain and [GG Wallet](https://chromewebstore.google.com/detail/gg-wallet/elicodfmaffbndngiifcpmammicgjidd) for signing. The missing piece was a **developer surface** where anyone in the community could go from idea to wasm to "what happens if I call this?" in one place, without treating every experiment like a full infra project.

So we built the **Contract Playground** at [gonkalabs.com/playground](https://gonkalabs.com/playground).

It might be a full replacement for your production pipeline or It can be a **fast feedback loop** for learning, prototyping, and debugging - especially for people who are new to CosmWasm on Gonka or who do not want to maintain a local build farm just to try something.

## Why this matters for the community

- **Lower barrier**: You do not need a configured dev machine to get a wasm build and see errors. That helps newcomers and anyone on a laptop that is not set up for `wasm32`.
- **Safer learning**: Simulation runs in **your** browser against a **mock** chain. You can break things, replay messages, and read logs without spending gas or touching mainnet (or even a testnet) until you choose to.
- **Honest integration**: When you are ready, the same flow can connect **GG Wallet** and talk to **real** RPC/REST through the same origin as the site, so you are not fighting CORS or pasting secrets into random tools. Everything happens from the browser window itself.
- **Living chain**: The explorer tab pulls **live** code IDs and contracts from the network so you can orient yourself against what is actually deployed, not only against tutorial examples.

We use this internally. We hope it becomes a default link when someone asks "how do I try this or that idea for implementing contract on Gonka?"

Btw, we used it to develop our smart contract for gns.

## What it does (high level)

| Area              | What you get                                                                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Editor**        | Rust source with syntax highlighting, templates, and **multiple files** stored in the browser so you can keep small projects without losing work on refresh.                          |
| **Compile**       | One click sends your source to our **remote compiler** (Rust in Docker), returns wasm, checksum, size, and **build logs** so failed builds are readable, not a black box.             |
| **Simulate**      | Loads the wasm in the browser and runs **instantiate / execute / query** against mocked host functions (storage, accounts, etc.) so you can validate behavior before spending tokens. |
| **Mock accounts** | Create accounts with balances you choose, pick a sender, **copy full addresses** - useful when you are testing permissions or multi-party flows.                                      |
| **Hints**         | We parse your Rust and surface **method-style suggestions** for messages so you are not staring at an empty JSON box guessing field names.                                            |
| **On-chain**      | Browse deployed code and contracts from the chain; connect wallet to **deploy** and interact when you are ready for real execution.                                                   |
| **Wallet**        | Uses the same GG Wallet / Keplr-style provider story as the rest of the ecosystem.                       |

## Compile path: why remote, not "magic in the tab"

Rust to wasm builds are heavy. Browsers are the wrong place to run a full Cargo graph for every user. So we run a **small compilation service** next to the site: your code goes in, optimized wasm comes back, and you still get **transparent logs** when something fails.

That tradeoff is intentional: the community gets **reproducible builds** on our pinned toolchain without everyone installing the same Rust, `wasm-opt`, and CosmWasm versions locally.

BTW: we are NOT storing the code. It just gets recieved by the worker, compiled and returned as .wasm artefacts (deleted immidiately after browser fetches it fully)

> Compiler is opensourced at https://github.com/gonkalabs/wasm-cloud-compiler



## Simulation: quick feedback without mainnet

Simulation is where we think the playground helps **the most people**. You can:

- Instantiate with a JSON message and see storage effects.
- Fire `execute` and `query` and inspect responses.
- Iterate on message shapes before you care about gas or block height.

Under the hood this is WebAssembly with CosmWasm-style host imports (memory regions, `db_read` / `db_write`, and friends). It will not model every edge case of a full node - and that is OK. The goal is **fast, safe iteration** and teaching, not a second consensus client.

> SImulator code is available via browser devtools and opensourced at https://github.com/gonkalabs/wasm-cloud-compiler/blob/main/simulator.js

## Explorer and deploy: same network, same mental model

The playground is wired to Gonka mainnet data via our proxied REST/RPC (same origin as [gonkalabs.com](https://gonkalabs.com), so the browser stays happy). You can see what is live, then plug in GG Wallet when you want to go on-chain.

If you are building a dApp, this is also a low-friction way to **verify** how a deployed contract behaves with real signing, without writing a one-off script.


## Open source and trust

The playground lives in our site repo; the pieces that matter for trust and reuse (compiler service, simulator, wallet wiring) are there for inspection. Same philosophy as [GG Wallet](https://github.com/gonkalabs/ggwallet), [GNS](https://github.com/gonkalabs/gns), [OpenGNK](https://github.com/gonkalabs/opengnk), [tx-scanner](https://github.com/gonkalabs/tx-scanner), and [rpc-pooler](https://github.com/gonkalabs/rpc-pooler): **show the work**, let people fork, file issues, and suggest improvements.

## What we learned while building it

- **Developer UX beats feature count**: scrollable logs, downloadable wasm, and obvious error text save more time than another checkbox nobody reads.
- **CosmWasm in the browser is picky**: getting memory/regions and imports right is the difference between "unreachable" and "it works"; we fixed that so simulation matches what contracts expect, not a toy VM.
- **The community moves fast**: when Telegram asks for mock accounts, method hints, or multi-file projects, those requests are usually right - we added them because real people hit the wall.

## What's next

We will keep tightening the loop based on what builders ask for: better hints, richer simulation (where it still stays honest), clearer docs for GG Wallet + CosmWasm flows, and anything that helps **more people ship contracts on Gonka** without drowning in setup.

If something is confusing or broken, open an issue on [our repos at github.com/gonkalabs](https://github.com/gonkalabs) or ping us in Telegram. We ship fast when the request is concrete.

**Try it:** [gonkalabs.com/playground](https://gonkalabs.com/playground)  
**About us:** [gonkalabs.com](https://gonkalabs.com) | **Explorer:** [gonka.gg](https://gonka.gg) | **GitHub:** [github.com/gonkalabs](https://github.com/gonkalabs)

### Previous Gonka Labs posts

- [Gonka Labs: How We're Building the Infrastructure for Gonka](https://github.com/gonka-ai/gonka/discussions/880)
- [Gonka.gg - Explorer, Analytics Platform, Data Provider for Gonka](https://github.com/gonka-ai/gonka/discussions/887)
- [OpenGNK - A Local OpenAI-Compatible Proxy for Gonka](https://github.com/gonka-ai/gonka/discussions/890)
- [Gonka Name Service (GNS) - Human Readable names for the Gonka Network](https://github.com/gonka-ai/gonka/discussions/898)
- [GG Wallet - An Open-Source Browser Wallet strictly for Gonka](https://github.com/gonka-ai/gonka/discussions/938)

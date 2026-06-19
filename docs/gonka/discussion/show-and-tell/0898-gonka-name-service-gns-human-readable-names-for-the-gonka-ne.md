---
title: "#898 — Gonka Name Service (GNS) - Human Readable names for the Gonka Network"
source: https://github.com/gonka-ai/gonka/discussions/898
discussion_number: 898
category: show-and-tell
synced_at: 2026-06-19T10:58:10Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #898](https://github.com/gonka-ai/gonka/discussions/898) каждые 6 часов. 

# Gonka Name Service (GNS) - Human Readable names for the Gonka Network

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-03-16 18:09 UTC · **Обновлено:** 2026-03-16 19:43 UTC

---

## 📝 Описание

Every blockchain eventually needs a naming layer. Ethereum has ENS. Cosmos chains have ICNS. Until now, Gonka didn't have one. So we built it.

**Gonka Name Service (GNS)** lets anyone register a short, memorable `.gnk` name - like `mike.gnk` - that resolves to a `gonka1...` wallet address. It is live on mainnet, integrated into [GG Wallet](https://chromewebstore.google.com/detail/gg-wallet/elicodfmaffbndngiifcpmammicgjidd), [gonka.gg](https://gonka.gg) explorer (users can find by name, use aliases like gonka.gg/address/mike.gnk instead of longer gonka1..... address) and as of today the smart contract source code is fully open source.

**This is a community project by** [Gonka Labs](https://gonkalabs.com)**.** We built GNS because we needed it ourselves and because the community was asking for it. Our goal is to make it the standard naming layer for the Gonka ecosystem - the one that wallets, dApps, explorers, and tooling all converge on.

<img width="1094" height="520" alt="Снимок экрана 2026-03-16 в 21 08 00" src="https://github.com/user-attachments/assets/c9948e29-3b62-4fad-a628-985b35146949" />


> **Any user can obtain a name at** [https://gonka.gg/names](https://gonka.gg/names)

### By the Numbers

- **1,300+ names** already registered on mainnet
- **2.5 GNK** flat registration fee per name
- Names **never expire** - register once, own forever

### What GNS Does

| Feature                                 | Description                                                                    |
| --------------------------------------- | ------------------------------------------------------------------------------ |
| **Register**                            | Claim any available `.gnk` name (3-63 chars, lowercase alphanumeric + hyphens) |
| **Resolve**                             | Look up any `.gnk` name to get the wallet address it points to                 |
| **Reverse lookup**                      | Given a `gonka1...` address, find the owner's primary `.gnk` name              |
| **Text records**                        | Attach metadata to a name (e.g. `twitter` → `@mike`, `avatar` → URL)           |
| **Transfer**                            | Gift a name to another address for free                                        |
| **Marketplace** *(dapp ui in progress)* | List a name for sale, delist, or buy - peer-to-peer, no protocol fee           |
| **Primary name**                        | Set which of your names is displayed as your identity                          |

### How It's Integrated

**GG Wallet** already supports GNS natively:

- Your primary `.gnk` name is displayed on the main wallet screen
- You can send tokens to any `.gnk` name instead of pasting a long address - the wallet resolves it automatically

Any wallet, dApp, or tool can integrate GNS by querying the contract directly. The message interface is documented in the [README](https://github.com/gonkalabs/gns).

### Contract Details

|                      |                                                                                                                                                               |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Contract address** | [gonka1rd582xazhyxde68g099ed0zpjzq0j0shnhkegg06s8009h7lnxjqvyf0qf](https://gonka.gg/address/gonka1rd582xazhyxde68g099ed0zpjzq0j0shnhkegg06s8009h7lnxjqvyf0qf) |
| **Chain**            | gonka-mainnet                                                                                                                                                 |
| **Runtime**          | CosmWasm (Rust)                                                                                                                                               |
| **License**          | MIT                                                                                                                                                           |
| **Source**           | [github.com/gonkalabs/gns](https://github.com/gonkalabs/gns)                                                                                                  |

### Why Open Source

We believe the naming layer for a network should be transparent and auditable. Anyone can read the contract logic, verify the on-chain deployment matches the source, run the test suite, or fork it for their own use. The full contract - registration, resolution, reverse lookup, text records, marketplace - is a single CosmWasm crate with 25 passing unit tests.

This follows the same open source approach we take with all Gonka Labs projects: [GG Wallet](https://github.com/gonkalabs/ggwallet), [OpenGNK](https://github.com/gonkalabs/opengnk), [tx-scanner](https://github.com/gonkalabs/tx-scanner), [rpc-pooler](https://github.com/gonkalabs/rpc-pooler), and others.

### What's Next

We are actively working on the next iteration of GNS (we will just upgrade the smart contract, address will not change):

- **Misleading name detection** - flag or prevent registration of names that visually resemble standard wallet addresses (e.g. a `.gnk` name starting with `gonka1` and ending in characters that mimic a real address). This is important to prevent social engineering where a name like `gonka1abc...xyz.gnk` could trick users into thinking they are sending to a raw address when they are actually resolving a name controlled by someone else.
- **Subdomain support** - allow name owners to create subnames (e.g. `pay.mike.gnk`)
- **Broader ecosystem integration** - work with other Gonka tools and services to adopt GNS resolution as a standard, so `.gnk` names work everywhere across the network
- **On-chain profile enrichment** - expand text records into a richer profile system (avatars, social links, bios) queryable by any dApp

We ship fast and iterate based on what the community needs. If there is a feature you want - open an issue on the [repo](https://github.com/gonkalabs/gns) or tell us in the Telegram chat.

### Previous Gonka Labs Posts

- [Gonka Labs: How We're Building the Infrastructure for Gonka](https://github.com/gonka-ai/gonka/discussions/880)
- [Gonka.gg - Explorer, Analytics Platform, Data Provider for Gonka](https://github.com/gonka-ai/gonka/discussions/887)
- [OpenGNK - A Local OpenAI-Compatible Proxy for Gonka](https://github.com/gonka-ai/gonka/discussions/890)

***

[gonkalabs.com](https://gonkalabs.com) | [gonka.gg](https://gonka.gg) | [GitHub](https://github.com/gonkalabs)

---

## 💬 Комментарии (1)

### Комментарий 1 — [@andrey055](https://github.com/andrey055)

*2026-03-16 19:43 UTC*

First of all, I want to sincerely thank the Gonka Labs team for what they are doing for the project. Their dashboards, wallet, faucet, and open proxy are the best things I’ve encountered during my five months of participating in the project 🤝.

The launch of Gonka Name Service is a very important step for the entire ecosystem. Human-readable names are a fundamental component of any blockchain network. They make working with addresses much simpler and clearer for users, and they also open up new possibilities for integrations in wallets, dApps, and other tools.
It is especially great to see that the contract is fully open source and publicly available. This builds trust and allows the community to study, verify, and further develop this initiative.

I wish the team success in developing GNS and hope that .gnk names will eventually become the standard identity layer within the Gonka network💪.

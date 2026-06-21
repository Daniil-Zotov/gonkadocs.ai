---
title: "#938 — GG Wallet - An Open-Source Browser Wallet strictly for Gonka"
source: https://github.com/gonka-ai/gonka/discussions/938
discussion_number: 938
category: show-and-tell
synced_at: 2026-06-21T14:33:57Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #938](https://github.com/gonka-ai/gonka/discussions/938) каждые 6 часов. 

# GG Wallet - An Open-Source Browser Wallet strictly for Gonka

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-03-23 20:32 UTC · **Обновлено:** 2026-03-23 20:39 UTC

---

## 📝 Описание

When we launched [gonka.gg](https://gonka.gg) and started using the Gonka network daily, one thing kept slowing us down: there was no native browser wallet for Gonka. Every transaction meant using the CLI, copying long addresses, and manually constructing commands or using browser wallets that needed flaky configuration or using wallets where we needed to send private key to with some ui without access to the code processing the request. We believe that Gonka can potentially reach millions of users - thus onboarding experience needed to be simpler.

So we built **GG Wallet** - an open-source Chrome extension wallet built exclusively for the Gonka blockchain. It is live on the [Chrome Web Store](https://chromewebstore.google.com/detail/gg-wallet/elicodfmaffbndngiifcpmammicgjidd), and as with almost everything we build at Gonka Labs, the full source code is [open on GitHub](https://github.com/gonkalabs/ggwallet).

We built GG Wallet because we needed it ourselves - and because the community was experiencing issues with setting up non-chain-native wallets. It will be great if one day GG Wallet will become the wide spread wallet for everyday Gonka users: simple enough for newcomers, powerful enough for power users.

<img width="1644" height="927" alt="Снимок экрана 2026-03-23 в 23 29 49" src="https://github.com/user-attachments/assets/da6b014f-34e7-40f8-a43e-03a6bea3cc82" />


### What GG Wallet Does

| Feature                    | Description                                                                                                                                                                                |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Send & Receive**         | Send GNK and IBC tokens to any `gonka1...` address or `.gnk` name. Receive via QR code                                                                                                     |
| **GNS Integration**        | Your primary `.gnk` name is displayed on the main screen. Type a `.gnk` name in the Send page instead of pasting a long address - the wallet resolves it automatically                     |
| **Full-precision amounts** | All balances and transaction amounts displayed without rounding - down to the last ngonka                                                                                                  |
| **IBC tokens**             | View and send IBC tokens alongside native GNK. Denominations are resolved automatically                                                                                                    |
| **Governance**             | Browse active and past proposals, view tally results with quorum parameters, vote (Yes / No / Abstain / Veto), submit new proposals, and deposit to proposals                              |
| **Transaction history**    | Powered by the [gonka.gg](https://gonka.gg) Explorer API with smart caching - cached data loads instantly, fresh data syncs in the background                                              |
| **Address book**           | Save frequent recipients and quick-fill the Send form                                                                                                                                      |
| **Multi-wallet**           | Create or import multiple wallets, switch between them with one click. Watch-only (view-only) wallets are also supported                                                                   |
| **CLI import**             | Import your existing `inferenced` CLI wallet by entering the mnemonic phrase it gave you during setup                                                                                      |
| **Private key export**     | Export your private key in a format compatible with [opengnk](https://github.com/gonkalabs/opengnk) proxy                                                                                  |
| **Auto-lock**              | Configurable timeout (1 / 5 / 15 / 30 min or never) - the wallet locks itself when you step away                                                                                           |
| **dApp provider**          | Keplr-compatible provider at `window.gonkaWallet` - any dApp can connect, request signatures, and broadcast transactions through the wallet **(we already have hex.exchange integration)** |

### GNS - Send by Name, Not by Address

One of the features we are most proud of is the deep [Gonka Name Service](https://github.com/gonka-ai/gonka/discussions/898) integration. GNS is built into the wallet at every level:

- Your **primary** **`.gnk`** **.gnk name** appears on the dashboard next to your address
- On the **Send page**, type any `.gnk` name and the wallet resolves it to a `gonka1...` address in real time as you type
- A dedicated **Names page** lets you manage all your `.gnk` names: transfer them to another address, change the resolved address, set your primary name, attach text records, list for sale, or delist

This means you can send tokens to `mike.gnk` instead of `gonka1a8cyf...`. The wallet handles the rest.

### dApp Integration

_Wallet is already "dApping" with [hex.exchange](https://hex.exchange) and [gonkalabs.com/playground](https://gonkalabs.com/playground)_

GG Wallet exposes a **Keplr-compatible provider** at `window.gonkaWallet`, which means any dApp that supports Keplr can work with GG Wallet with minimal changes. The provider supports:

- `enable()` - request wallet access
- `getKey()` - get the user's address and public key
- `signAmino()` / `signDirect()` - sign transactions
- `sendTx()` - broadcast signed transactions
- `signArbitrary()` - sign arbitrary data (ADR-036)
- `experimentalSuggestChain()` - register new chain configurations
- `getOfflineSigner()` / `getOfflineSignerAuto()` - CosmJS-compatible offline signers

The wallet also fires both `gonkaWallet#initialized` and `keplr#initialized` events, so existing Keplr-aware dApps can detect it automatically. Every sensitive operation goes through an **approval popup** - the user always sees exactly what they are signing before confirming.

### Inference Signer

The wallet includes a **TypeScript port of the opengnk signing algorithm** - the same RFC 6979 ECDSA scheme used by the [opengnk](https://github.com/gonkalabs/opengnk) proxy to sign inference requests for the Gonka AI network. This means the wallet already has the cryptographic foundation to sign inference requests directly from the browser. The ML Ops permission grant UI is coming in a future update.

### Security

We take security seriously. The wallet stores your mnemonic encrypted with **AES-GCM** using a key derived from your password via **PBKDF2 with 600,000 iterations**. Your mnemonic is only decrypted in memory when the wallet is unlocked, and the wallet auto-locks after a configurable timeout.

The extension requests only two Chrome permissions: `storage` and `alarms`. No broad host permissions. No background network access beyond what you explicitly trigger. The content script runs on HTTPS pages only to provide the dApp provider - it does not read or modify page content.

If you discover a security vulnerability, please follow the process in [SECURITY.md](https://github.com/gonkalabs/ggwallet/blob/main/SECURITY.md). Do not open a public issue for security bugs.

### Under the Hood

| Layer   | Stack                                                             |
| ------- | ----------------------------------------------------------------- |
| UI      | React 18, TypeScript, Tailwind CSS, Zustand                       |
| Build   | Vite 5, CRXJS (Chrome Extension Manifest V3)                      |
| Chain   | CosmJS (Stargate), CosmWasm `MsgExecuteContract` for GNS          |
| Crypto  | Web Crypto API (AES-GCM, PBKDF2), @noble/hashes, @noble/secp256k1 |
| HD Path | `m/44'/1200'/0'/0/0` (BIP44 coin type 1200)                       |

The wallet is structured as a standard MV3 Chrome extension:

- **Service worker** (`background/`) handles all chain interactions, keystore management, and message routing
- **Popup** (`popup/`) is the React UI with pages for Dashboard, Send, Receive, Transactions, Governance, GNS Names, and Settings
- **Content script + inpage** (`provider/`) injects the `window.gonkaWallet` provider into web pages and bridges communication between dApps and the service worker
- **Shared libraries** (`lib/`) contain chain configuration, CosmJS helpers, GNS resolution, encryption, formatting, and the inference signer

### How It Evolved

We shipped v0.1.0 with the basics: create wallet, import mnemonic, send and receive GNK. Then we listened.

**v0.1.1** - auto-lock, IBC token support, address book, watch-only wallets  
**v0.1.2** - dApp provider (Keplr-compatible), stability improvements  
**v0.1.3** - governance (vote, proposals, tally, quorum), full-precision amounts, smarter transaction history  
**v0.1.5** - Cosmos Hub chain support in the provider (for dApps that require `cosmoshub-4`)  
**v0.1.6** - GNS integration: send by `.gnk` name, primary name display, full names management page, transaction caching

Every release was driven by what the community asked for. Someone needed IBC tokens - we added it. Someone needed governance - we added it. The GNS integration came because we built [GNS](https://github.com/gonka-ai/gonka/discussions/898) and wanted it to work seamlessly in the wallet from day one.

### Open Source

The full source code is available at [github.com/gonkalabs/ggwallet](https://github.com/gonkalabs/ggwallet) under the MIT license (with attribution). Anyone can read the code, verify what the extension does, build from source, or fork it. We believe a wallet - the tool that holds your keys - should be fully transparent.

If you are building a dApp on Gonka and want to integrate with GG Wallet, the provider API is documented in the source and follows the Keplr standard. If you need help - tell us in the Telegram chat.

### What's Next

- **Staking** - delegate, undelegate, and claim rewards (when network is ready)
- **ML Ops permissions** - grant dApps permission to sign inference requests through the wallet
- **Broader dApp ecosystem** - as more dApps launch on Gonka, we will keep improving the provider to support every use case

We ship fast and iterate based on what the community needs. If there is a feature you want - open an issue on the [repo](https://github.com/gonkalabs/ggwallet) or tell us in the Telegram chat.

### Install

[Chrome Web Store](https://chromewebstore.google.com/detail/gg-wallet/elicodfmaffbndngiifcpmammicgjidd) | [GitHub](https://github.com/gonkalabs/ggwallet) | [Build from source](https://github.com/gonkalabs/ggwallet#install--build)

### Previous Gonka Labs Posts

[Gonka Labs: How We're Building the Infrastructure for Gonka](https://github.com/gonka-ai/gonka/discussions/880)  
[Gonka.gg - Explorer, Analytics Platform, Data Provider for Gonka](https://github.com/gonka-ai/gonka/discussions/887)  
[OpenGNK - A Local OpenAI-Compatible Proxy for Gonka](https://github.com/gonka-ai/gonka/discussions/890)  
[Gonka Name Service (GNS) - Human Readable names for the Gonka Network](https://github.com/gonka-ai/gonka/discussions/898)

[gonkalabs.com](https://gonkalabs.com) | [gonka.gg](https://gonka.gg) | [GitHub](https://github.com/gonkalabs)

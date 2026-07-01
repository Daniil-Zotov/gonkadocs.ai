---
title: "#906 — Gonka Tools: Web Interface for Validators and Mining Operations"
source: https://github.com/gonka-ai/gonka/discussions/906
discussion_number: 906
category: show-and-tell
synced_at: 2026-07-01T10:15:45Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #906](https://github.com/gonka-ai/gonka/discussions/906) каждые 6 часов. 

# Gonka Tools: Web Interface for Validators and Mining Operations

**Автор:** [@aleks1k](https://github.com/aleks1k) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-03-17 20:20 UTC · **Обновлено:** 2026-03-17 20:20 UTC

---

## 📝 Описание

**URL:** [https://cloudmine.mingles.ai/gonka-tools](https://cloudmine.mingles.ai/gonka-tools)

Running a validator or managing mining operations on the Gonka network traditionally requires CLI expertise and careful key management. Gonka Tools eliminates this complexity with a browser-based interface that handles validator setup, collateral operations, and governance participation — all through your web3 wallet.

No backend services. No API keys. No command-line required. Just connect your Keplr wallet (software or Ledger hardware) and manage your entire Gonka validator lifecycle from a single interface.

## What Is Gonka Tools?

Gonka Tools is a web interface for performing operations on the Gonka network via a web3 wallet. It runs entirely in your browser and connects directly to Gonka RPC/API endpoints through the Keplr extension.

**Key characteristics:**
- Zero trust architecture — your keys never leave your wallet
- Supports both software wallets and Ledger hardware wallets via Keplr
- Auto-configures gonka-mainnet chain parameters via `experimentalSuggestChain`
- Real-time balance tracking across liquid, active collateral, and unbonding states
- Direct RPC/API communication — no intermediary servers

**Primary use cases:**
- New validator setup (extract pubkey for config.env)
- Collateral deposits and withdrawals
- Granting ML ops permissions to hot validator keys
- Governance voting on network proposals
- Validator unjailing and metadata editing
- Inspecting any Gonka address state (even without wallet connection)


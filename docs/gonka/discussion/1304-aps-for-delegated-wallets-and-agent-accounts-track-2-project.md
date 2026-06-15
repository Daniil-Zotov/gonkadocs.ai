---
title: "#1304 — APS for delegated wallets and agent accounts (Track 2, Project 3)"
source: https://github.com/gonka-ai/gonka/discussions/1304
discussion_number: 1304
synced_at: 2026-06-15T18:13:27Z
---

> 🔄 **Авто-синхронизация:** из [GitHub Discussion #1304](https://github.com/gonka-ai/gonka/discussions/1304) каждые 6 часов. Прямые правки будут перезаписаны.

# APS for delegated wallets and agent accounts (Track 2, Project 3)

**Автор:** [@aeoess](https://github.com/aeoess) · **Категория:** :speech_balloon: General · **Создано:** 2026-06-04 01:38 UTC · **Обновлено:** 2026-06-04 01:38 UTC

---

## 📝 Описание

Track 2, Project 3 is close to what APS was built for: an agent acting within scoped authority, without exposing the owner's main key and without manual approval on every call. That authorization and audit layer is what APS implements today, open and Apache-2.0, on npm.

The primitives map to the project directly:

- **Predefined limits without exposing the main key:** the agent acts under a delegated key with a scoped grant. The owner's main key never leaves them. Limits can cover scope, spend cap, time window, and allowed actions.
- **No manual confirmation per action:** the scope authorizes a class of calls up front. Each request is checked against the delegation before it executes, with no human in the loop.
- **Owner keeps control:** sub-delegations can only narrow authority, and revoking a grant cascades to everything downstream.
- **Audit-trail review:** every authorized action emits a signed receipt that verifies offline, so the trail does not depend on trusting the gateway that produced it.

Project 3 also covers agents buying compute, not only calling inference. The same model extends to payment: one rail-agnostic interface carrying the same scoped authorization, spend limits, and signed receipts. Reference adapters ship for x402 (USDC on Base) and Nano, with bindings to AP2 (Google's Agent Payments Protocol), Stripe Issuing, and ACP. A Gonka-token rail would implement the same interface and inherit the limits, revocation, and receipts without new machinery.

To be clear on the boundary, APS is not a wallet, custody, or settlement. It sits in front of whatever holds funds and calls inference, decides whether a given agent action is authorized, and leaves a verifiable record that it happened. It runs as a library or an opt-in sidecar and needs no protocol change.

I'd rather show this than describe it, so I'm happy to put up a small reference implementation against the delegated-wallet path. Two questions to target it:

1. Is there a current branch or interface for the delegated-wallet / agent-account work, or is Project 3 still at the roadmap level?
2. Do you expect the authorization check to live closer to the wallet/account layer or the inference gateway? That decides where the check sits.

Repo: github.com/aeoess/agent-passport-system · npm: npmjs.com/package/agent-passport-system


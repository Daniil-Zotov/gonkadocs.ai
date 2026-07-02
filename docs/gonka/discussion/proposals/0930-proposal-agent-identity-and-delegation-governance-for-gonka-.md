---
title: "#930 — Proposal: Agent identity and delegation governance for Gonka compute"
source: https://github.com/gonka-ai/gonka/discussions/930
discussion_number: 930
category: proposals
synced_at: 2026-07-02T04:31:38Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #930](https://github.com/gonka-ai/gonka/discussions/930) каждые 6 часов. 

# Proposal: Agent identity and delegation governance for Gonka compute

**Автор:** [@aeoess](https://github.com/aeoess) · **Категория:** :bulb: Proposals · **Создано:** 2026-03-20 00:42 UTC · **Обновлено:** 2026-03-22 19:48 UTC

---

## 📝 Описание

Gonka's agent-aware inference gateway handles the compute layer. One gap: when an agent requests inference, there's no cryptographic proof of who authorized that agent or what scope it operates under.

The Agent Passport System (APS) provides this layer:

- **Ed25519 cryptographic identity** for each agent
- **Scoped delegation chains** — a human grants an agent specific permissions with spend limits. The agent can sub-delegate with narrower scope. Authority monotonically narrows at each hop.
- **Cascade revocation** — revoke one delegation, all downstream sub-delegations die instantly
- **3-signature policy chain** — every action (including inference requests) produces a signed audit trail: intent → policy evaluation → execution receipt

**How this fits Gonka's architecture:**

When an agent calls Gonka's inference API, the request could carry a delegation proof showing:
1. Who authorized this agent to use compute
2. What models/capabilities are in scope
3. What spend limit applies
4. A signed receipt for billing attribution

This turns Gonka from "serve inference to whoever has an API key" into "serve inference to cryptographically authorized agents with verifiable spend limits." For subnet operators and compute providers, this means granular billing and access control without managing API keys per agent.

**Integration surface:**

APS ships as an MCP server (61 tools) and npm package (`agent-passport-system`, 866 tests). The gateway enforcement boundary could sit in front of Gonka's routing layer, checking delegation scope before forwarding to the appropriate model.

We're currently running cross-engine interop tests with three other governance protocols (AIP, Kanoniv, Guardian) — all Ed25519 based, all mutually verifying delegation chains. Gonka could be a compute provider in that ecosystem.

SDK: https://github.com/aeoess/agent-passport-system
Paper: https://doi.org/10.5281/zenodo.18749779
Site: https://aeoess.com

---

## 💬 Комментарии (1)

### Комментарий 1 — [@aeoess](https://github.com/aeoess)

*2026-03-21 17:14 UTC*

@hermesnousagent — the complementary framing is right. APS handles the machine-verifiable proof chain (was this agent cryptographically authorized, within what scope, at what spend limit), and the operator-visible layer handles what the human actually sees and approves.

The `delegation_ref` back-pointer pattern you described maps to how APS already links commerce receipts to delegation chains internally. Every `CommerceActionReceipt` in APS carries the delegation ID that authorized it, so the cryptographic proof and the human-readable record can cross-reference.

On your closing question: the open problem is both. Machine-to-machine billing attribution (which APS closes with signed delegation chains + Merkle attribution) and human-facing spend authorization (which needs a UX layer). APS has `request_human_approval` in the Commerce layer for the human-facing gap, but it is a protocol primitive, not a chat-native UX. That is where a chat-based approval surface like what you describe adds value — the protocol provides the cryptographic substrate, the chat interface provides the operator experience.

The composition would be: APS delegation chain proves authorization scope, Bit-Chat surfaces the approval request in a human-readable format, the operator approves, and the approval feeds back into APS as a signed receipt that closes the loop for both billing attribution and dispute resolution.

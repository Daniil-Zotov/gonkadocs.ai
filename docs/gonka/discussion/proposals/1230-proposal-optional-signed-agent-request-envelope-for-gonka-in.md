---
title: "#1230 — Proposal: optional signed agent request envelope for Gonka inference"
source: https://github.com/gonka-ai/gonka/discussions/1230
discussion_number: 1230
category: proposals
synced_at: 2026-06-18T05:03:12Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1230](https://github.com/gonka-ai/gonka/discussions/1230) каждые 6 часов. 

# Proposal: optional signed agent request envelope for Gonka inference

**Автор:** [@aeoess](https://github.com/aeoess) · **Категория:** :bulb: Proposals · **Создано:** 2026-05-22 17:24 UTC · **Обновлено:** 2026-05-24 03:00 UTC

---

## 📝 Описание

@gmorgachev, picking up your broker-side suggestion from [#1185](https://github.com/gonka-ai/gonka/discussions/1185#discussioncomment-17004938) with a concrete envelope schema and a reference implementation. I'd like input on placement and v1 scope before opening the PR.

## Proposal

Add an optional signed agent request envelope on `/v1/chat/completions` and `/v1/completions`. When the `X-Agent-Passport` header is absent, request behavior is byte-identical to today. Default config disables the layer. The envelope is additive metadata. No chain change, no new consensus message.

## What gap does it close

Gonka authenticates the network actors: Developer, Transfer Agent, Executor. `MsgFinishInference` records `RequestedBy`, `TransferredBy`, `ExecutedBy`. The signature chain works. AuthKey replay protection works. `x/authz` warm-key delegation works.

The narrower gap is *agent-subject context* when an automated agent calls Gonka under an already-authorized principal:

1. **Sub-principal identity is invisible.** `RequestedBy` resolves to the Developer or warm-key Grantee; the actual agent making the call is not on the wire.
2. **`x/authz` is message-type scoped, not attribute scoped.** A Developer cannot grant a warm key the right to run inference only for model X, only for purpose Y, only until next Tuesday. A custom `InferenceAuthorization` type in `x/authz` would address this but requires a chain change.
3. **No beneficiary distinct from payer.** When agent A pays the network on behalf of customer C, the on-chain record identifies A. There is no field that says the work was done *for* C.

## What the envelope does

When `X-Agent-Passport` is present, the verifier checks that:

- The envelope is signed by the Developer's Cosmos secp256k1 key via **ADR-036** (Keplr `signArbitrary` compatible). The principal pubkey is embedded; the verifier derives the address locally and asserts equality with the envelope's principal address. No chain query needed, which eliminates the first-tx-pubkey lookup and the associated DoS surface.
- The agent signed the specific request via **Ed25519** over a domain-separated, length-prefixed payload binding `chain_id`, HTTP method, full request URI, the JCS-canonicalized envelope, and the request body.
- The envelope is not expired, not older than `MaxEnvelopeTTL` (default 1h, configurable), and falls within `not_before` if present.
- If `allowed_models` is present, the requested model must be listed. If omitted, the envelope does not restrict model choice.
- The principal address matches `RequesterAddress`, or `x/authz` shows an active Grantee to Granter relationship for `/inference.inference.MsgStartInference`.

After `s.recorder.StartInference` succeeds, a structured attribution event is emitted asynchronously through a bounded queue. Drop-on-full with a counter; never blocks the request path.

## Composition with existing primitives

This follows existing Cosmos patterns and adds no new root of trust:

- **ADR-036** for the Developer's arbitrary-data signature on the passport, the same path Keplr `signArbitrary` produces.
- **`x/authz`** for warm-key resolution when the request comes from a Grantee distinct from the principal. Uses Gonka's existing `AuthzCache.GetPubKeyForSigner` directly.
- Ed25519 from the Go standard library for the agent's per-request signature.
- RFC 8785 JCS for canonicalization, vendored to the envelope schema. Numbers and Unicode surrogate cases are out of scope; the schema has no JSON numbers and unknown fields are rejected.

The envelope is an off-chain request-layer extension. Not a consensus message. Not a chain message. Not a new identity layer underneath the Developer key.

## Why request-layer first

A chain-native version could eventually add optional `AgentId` and `Beneficiary` fields to `MsgFinishInference`, but that's a separate governance discussion. For v1, broker-side middleware looks like the safer starting point:

- no consensus change
- no new chain message
- no change to existing request authentication
- easy opt-in and easy rollback
- clear place to test the schema before proposing anything on-chain

If you see a different placement that closes the gap with less surface area, I'd rather hear it now than after the PR is up.

## What stays unchanged

Listing the surface concerns explicitly because that's where reviewer attention naturally goes on any envelope proposal. This PR does NOT modify:

- Developer signature on AuthKey, AuthKey replay protection, `calculations.ValidateTimestamp`, or `checkAndRecordAuthKey`
- Transfer Agent signing or Executor signing
- `MsgStartInference` or `MsgFinishInference` schemas
- Escrow, settlement, pricing, tokenomics
- Consensus, ante handlers, ML node, PoC, validation
- Existing brokers, gateways, or their forwarding semantics

Default config is `enabled: false`. Operators opt in.

## What might come later

One Phase 2 direction worth flagging: extending `MsgFinishInference` with optional `AgentId` and `Beneficiary` fields so the data the envelope carries off-chain in v1 becomes queryable on-chain. That's a chain change requiring governance and is **not** assumed by this PR. If interest exists, it gets a separate Discussion.

Other items explicitly deferred to Phase 2: scoped delegation chains, multi-hop attribution receipts, multi-sig principal support, devshard daemon integration, and revocation beyond short TTL. @a-kuprin, the devshard authentication piece you raised in #1185 falls under devshard daemon integration here; I think that wants its own Discussion once v1 settles.

## What I'm asking for

Two things before opening the PR:

1. **Placement check.** Broker-side request-layer middleware on `/v1/chat/completions` and `/v1/completions` matches your #1185 suggestion. Confirm or redirect.
2. **Scope check.** Is the envelope schema (sub-principal identity, attribute scope, and beneficiary, all optional and signed by the existing Developer key) the right v1 surface, or is there a narrower starting point preferred?

The reference implementation is ready: single PR, single new package `internal/agentenvelope/`, ~25 modified lines across two existing files, opt-in via config, backward compatible by construction. I can open it as a linked PR shortly, but the design points above are the substance of the Discussion. Code can wait on placement confirmation if that's the cleaner sequence.

## Disclosure

I maintain APS (Agent Passport System), an Apache 2.0 open protocol for AI agent identity. The envelope format here is APS-compatible. The integration is fully isolated in `internal/agentenvelope/`, so the wire format can be swapped without re-architecting anything else. Adopting it Gonka-side does not require Gonka to adopt APS network-wide.


---

**Linked PR:** [#1232](https://github.com/gonka-ai/gonka/pull/1232) — reference implementation matching the design points above.

---

## 💬 Комментарии (2)

### Комментарий 1 — [@a-kuprin](https://github.com/a-kuprin)

*2026-05-23 04:57 UTC*

I think the proposal doesn't completely take into account `devshard` logic.

**Short story**:
When inferences was written directly to chain it even theoretically cannot serve large amount of inferences. Moreover only 10% of real hardware could be utilized (at current number of mlnodes). So devshards was introduced (L2 layer for Gonka), but they are not currently fully in production mode, as there are still unsolved problems, like handling cPoC, that is scheduled to next releases.
Devshard is created by one user account. He puts the escrow GNK and pays fee for devshard creation. And only this developer is authenticated to current devshard. And this is his responsibility to authenticate other users to his devshard. It shouldn't be in chain logic to check inferences. Devshard just processes inferences and then on finalization provides to chain how many GNK shouyld be taken from users escrow balance.

My intention is that any changes and proposals for legacy inference handling (not with devshard) are just out of date. We should design things that will feat future infrastructure.

### Комментарий 2 — [@aeoess](https://github.com/aeoess)

*2026-05-23 15:26 UTC*

Got it. Moving this to the devshard path and closing #1232. Should the verifier live inside dl/devshards-gateway-to-main, or as a sidecar in front of the devshard?

**↳ Ответ от [@a-kuprin](https://github.com/a-kuprin)** · *2026-05-24 03:00 UTC*

> There is already devshardctl that is runned by dev who initiated devshard escrow.
> dl/devshards-gateway-to-main - is just a git branch

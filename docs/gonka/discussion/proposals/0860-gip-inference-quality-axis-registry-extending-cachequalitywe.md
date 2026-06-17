---
title: "#860 — GiP: Inference Quality Axis Registry — extending CacheQualityWeight toward measurable useful work"
source: https://github.com/gonka-ai/gonka/discussions/860
discussion_number: 860
category: proposals
synced_at: 2026-06-17T11:18:35Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #860](https://github.com/gonka-ai/gonka/discussions/860) каждые 6 часов. 

# GiP: Inference Quality Axis Registry — extending CacheQualityWeight toward measurable useful work

**Автор:** [@Mayveskii](https://github.com/Mayveskii) · **Категория:** :bulb: Proposals · **Создано:** 2026-03-04 22:39 UTC · **Обновлено:** 2026-03-11 15:43 UTC

---

## 📝 Описание

## History of contributions

- PR #856 — Continuous PoC complete: fixed critical serialisation bug in #845 (ContinuousPocParams never persisted on-chain), added full pruning for three new collections, epoch settlement with EffectivePocWeight, and Merkle-proof challenge/response system. Closes GiP #821.
- PR #859 — Semantic cache + CacheQualityWeight: two-level cache (L1 exact-match, L2 cosine similarity), additive quality bonus at epoch settlement, governance-controlled params, 20 tests without GPU or live chain.

## Motivation

`tokenomics-v2/bitcoin-reward.md` explicitly named an open gap: *"No incentive for model diversity or utilization quality."* PR #859 is the first concrete implementation of that direction — but it only measures one axis: reuse.

The deeper question: can the protocol reward nodes for the quality of their computation, not just its volume? A node that earns more because its result was useful starts optimizing for outcomes, not throughput. That changes behavior across the entire network.

## Proposed solution

Extend `CacheQualityParams` toward a `QualityAxisRegistry` — a governance-controlled map where each axis has its own weight and submission contract:

- **Reuse** (already in PR #859) — implicit, internal to DAPI
- **Session continuity** — DAPI sees session depth without any integration
- **Explicit feedback** — single `feedback` tag on the next API request, same OpenAI-compatible contract
- **Verifiable outcome** — developer marks task resolved and submits via existing `MsgSubmitCacheQualitySummary` pattern

Quality signal delivery is already mostly available:
1. API — `inference_id` in every response, feedback as a tag on next request
2. SDK — wraps the call, collects implicit signals automatically
3. Widget — embeddable UI, zero code from developer
4. Implicit signals — DAPI observes session depth and semantic repetition natively
5. Webhook — node pushes event on inference close, app returns outcome
6. CLI / authz — `MsgSubmitCacheQualitySummary` already in `InferenceOperationKeyPerms` with full Grant→Exec→Revoke

`CacheQualityParams` + epoch settlement pattern introduced in #859 is generic enough to carry all of these without rebuilding the reward layer.

## Implementation roadmap

1. Merge PR #856 (continuous PoC) + PR #859 (cache quality foundation)
2. GiP discussion: define `QualityAxisRegistry` schema and governance params
3. Extend `MsgSubmitCacheQualitySummary` to carry multi-axis payload
4. Extend `quality_reporter.go` to aggregate per-axis counters per epoch
5. SDK / webhook delivery layer

## Open question

CacheQualityWeight in PR #859 already establishes the epoch settlement pattern for quality bonuses. Is there appetite in the community to extend this toward a full quality axis registry as the next GiP, or should the conversation start after #856 and #859 land?

---

## 💬 Комментарии (3)

### Комментарий 1 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-06 18:42 UTC*

## Update: measurement complete + vector proof

The original GiP describes the system architecture. This comment proves the vector 
works — meaning: developer behavior can shift network quality measurably, through 
the same axes this GiP defines.

---

### The core claim

Network quality is not fixed. It is a function of how developers structure their 
requests. The protocol can learn that structure and reinforce it.

That's not a hypothetical. Here's the measured path:

**Step 1: Network today (measured, not projected)**

L8 CV = 0.83 — latency swings 83% from mean, every epoch.
L9 = 94.33% — 2,624 inferences fail per epoch on average. Peak: 13,020 (epoch 175).
L6 = 0.0005 — M=571 random routing makes cache mathematically useless.
Composite score: 0.4832 / 1.0

This is the baseline. Random routing, no feedback, no structured patterns.

**Step 2: SDK changes the vector**

Tested 5 domains, 3 request variants each, all-MiniLM-L6-v2 (dim=384, no GPU):

| SDK method     | DX axis | What changes in L-axes |
|----------------|---------|------------------------|
| autoRegister() | DX0     | L9 +0.28pp (less 403)  |
| estimateTokens()| DX2+4  | L8 CV 0.83 → 0.74      |
| decomposeWorkflow() | DX7 | L2 ↑ + L6 activated    |

Without SDK: average pairwise similarity across participants = 0.49.
With SDK templates (DX7): 0.80. Delta: +62.1%.

One participant using structured prompts raises cache hit probability 
for every other participant in the same domain. This is a commons, 
not an individual optimization.

**Step 3: Governance steers the threshold**

SimilarityThresholdBps is already governance-controlled (PR #859 default: 9700).

| Phase | Threshold | Hit rate | What triggers next step |
|-------|-----------|----------|------------------------|
| now   | 9700      | 26.7%    | auth flows hit immediately |
| +3ep  | 9200      | 40.0%    | L2 hit rate confirmed on-chain |
| +5ep  | 8800      | 60.0%    | SDK template coverage proven |
| +8ep  | 8500      | 93.3%    | 4/5 task domains covered |
| +12ep | 8000      | 100.0%   | full coverage |

Each step: zero code changes, zero deployments, one governance vote.
Each step is reversible. The protocol is in control.

**Worst case: zero impact**

repeat_fraction=5%, stream=50%, M=571, threshold=0.97 unchanged:
hit_rate = 0.05 × (1/571) × 0.50 = 0.000044 ≈ 0
CacheQualityWeight = 0. Feature off by default.
Worst case = today. Zero regression.

---

### What this means for the protocol

GiP #860 is not about cache. Cache is Phase 0.

GiP #860 is about closing the feedback loop:
  Developer uses SDK → structured prompts → L6 activates → 
  QualityReporter records → GetQualityWeightedExecutor routes better → 
  better nodes win traffic → L8/L9 improve → SDK reports better outcomes → 
  governance lowers threshold → loop tightens.

The protocol currently has no such loop. Every inference is equally invisible 
to the network. That's the gap this GiP closes.

---

### What remains

One gap: testnet node with CacheQualityParams.Enabled=true for 1 epoch.
This closes live repeat_fraction measurement (real X-Cache headers, real hit/miss).
Everything else is either measured from live network or bounded by worst case.

Full spec with numbers: docs/specs/inference-quality-protocol.md in the PR #859 branch.

### Комментарий 2 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-06 19:44 UTC*

The final variation offers you the opportunity to test the quality for yourself at any level of client/host/GNK inference.

Depending on how you configure the SDK context and implement AXIOS, the final step is to engage with such understanding participants and discuss valid hypotheses to confirm them at the test production level. Fine-tuning the matrix and adjusting the calculations, given that the idea addresses performance issues and improves the user experience at all levels, is no longer as unattainable as it was at the time of the first thread. Overall, it's nice to have the opportunity to deliver this setting as a protocol option first. I hope someone finds it relevant.

PS:
The cursor has expired, so I'll study the related docs, processes, and protocol philosophy for now.

### Комментарий 3 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-08 13:32 UTC*

Update: Implementation proof is now in a separate repo. The agent at gonkalabs/gonka-agent uses the same protocol (semcache, X-Inference-Feedback, two workspaces). docs/testing.md records a real two-participant run (Proof 860): Participant A cold, Participant B partial hit 0.79, ~23% time saved. So the “participant interdependence” vector from this GiP is no longer hypothetical — it’s reproducible. When dev-chains or an experimental branch is available, this stack can be pointed at it without changing the design.

**↳ Ответ от [@Mayveskii](https://github.com/Mayveskii)** · *2026-03-11 15:43 UTC*

> ### Update: Binary Singularity — PQM > 1.0 proven (2026-03-11)
>
> sourced in https://github.com/gonka-ai/gonka/pull/859
>
> The "participant interdependence" vector from the last update is now scaled to a full experiment suite and production-ready deploy stack.
>
> **4 experiments on Bookworm (CPU-only, no GPU):**
>
> | Exp | Runs | PQM | Slots | Source | What proved |
> |-----|------|-----|-------|--------|-------------|
> | 1 | 256 | — | 4 | synthetic | PatternSlot + cosine matching works |
> | 2 | 9,216 | 0.988 | 4 | synthetic | Hub approved (epoch 196 baseline) |
> | 3 | 15,360 | **1.001** | 6 | 8 real developers | Multi-user semantics > GPU baseline |
> | 4 | 11,520 | **1.020** | 197 | raw developer workflow (676KB) | Raw data → binary singularity |
>
> **PQM > 1.0** = the binary layer produces better results than single cold GPU inference. The quality axis registry proposed in this GiP is now measurable end-to-end.
>
> **What's deployed:**
>
> - Full deploy stack: LITE / MEDIUM / HARD (K3s) / PRODUCTION — [deploy/binary-singularity/](https://github.com/Mayveskii/gonka/tree/feature/gip-semantic-cache-trust-layer/deploy/binary-singularity)
> - `gonka-agent` SDK with PatternSlot store + mesh sharing — [gonkalabs/gonka-agent](https://github.com/gonkalabs/gonka-agent/tree/dev/binary-singularity)
> - Quality middleware: `POST /quality/search` + `POST /quality/slots/share` — inter-participant slot exchange
> - int8-quantized CPU cosine search in mesh pool — ~5ms slot hit vs ~1280ms GPU mean
>
> **How axes from this GiP are now measured:**
>
> | Axis | GiP #860 design | Current implementation |
> |------|-----------------|----------------------|
> | L0 Compute stability | CV(participants) | PoC weight tracking |
> | L4 Usefulness | feedback tag | `X-Inference-Feedback` header in agent |
> | L6 Reuse | cache hit rate | PatternSlot store + mesh pool (0.27 at M=1 vs 0.0005 baseline) |
> | L8 Latency | CV(latency) | quality-middleware measures per request |
> | L9 Completion | success rate | agent tracks resolved/unresolved |
>
> **Network correlation (live data, epochs 161-191, 2,503,595 inferences):**
>
> - L6: 0.000473 → 0.27+ (571× with specialization)
> - L8: 1280ms mean → ~5ms slot hit (250×)
> - L9: 90.4% → 100% tracked in agent loop
> - Memory: 16 GB VRAM → 19-23 MB CPU RAM (700×)
> - GPU saves at 20% specialization: **940,698/epoch** (~$155,800/year full protocol)
>
> **The feedback loop this GiP described is now closed:**
>
> Developer uses agent → structured task → slot distilled → shared to mesh pool → other participant finds slot → LLM gets context → better answer → PQM grows → governance can lower threshold → loop tightens.
>
> This was the missing piece: not just cache, but a **collective semantic memory** that compounds with every participant.
>
> **Comprehensive guide for all user levels** (developers, researchers, legal/housing workflows, contributors): [GUIDE.md](https://github.com/Mayveskii/gonka/blob/feature/gip-semantic-cache-trust-layer/deploy/binary-singularity/GUIDE.md)
>
> One ask remains: enable `CacheQualityParams` on testnet for 1 epoch — closes the only gap (`repeat_fraction` as a measured number).
>
>
> @libermans 
>
> Sincerely, Mayevskii_A , thx 4 my best <3 

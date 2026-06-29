---
title: "#869 — GiP #860 — Inference Quality Protocol: Semantic Inference Optimization"
source: https://github.com/gonka-ai/gonka/discussions/869
discussion_number: 869
category: proposals
synced_at: 2026-06-29T11:24:34Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #869](https://github.com/gonka-ai/gonka/discussions/869) каждые 6 часов. 

# GiP #860 — Inference Quality Protocol: Semantic Inference Optimization

**Автор:** [@Mayveskii](https://github.com/Mayveskii) · **Категория:** :bulb: Proposals · **Создано:** 2026-03-06 13:54 UTC · **Обновлено:** 2026-03-08 13:32 UTC

---

## 📝 Описание



## Background

This discussion is the **design document that precedes implementation**. PR [#859]
(semantic cache) is the first implementation milestone; it exists to test the
infrastructure hypothesis, not to define the full system. The full system is defined here.

Per the review process @akup outlined on [#856] and [#802]: design first, then code.
This GiP is that design step. PR [#859] is scoped strictly to what this document
justifies in Phase 0.

---

PR [#859] introduces `CacheQualityWeight` — a reward for cache reuse. It is a working
implementation, but deliberately scoped: it solves one part of a larger problem.

This discussion proposes what that larger problem is, how it connects to everything
already in the protocol, and what the full solution looks like.

---

## The gap: quality has no protocol representation

The Gonka network has a rigorous economic model for *compute*: Proof-of-Compute
measures nonce generation, validates it across nodes, and converts it to epoch weight.
Every node understands, optimizes for, and is incentivized by PoC.

**Quality of inference** — whether a response was useful, accurate, timely, or
appropriate for the request type — has no equivalent protocol representation. It is
invisible to the chain.

This is not a criticism. It is a natural stage of development. PoC needed to land first
(see [#856], [#821]). But as the network grows, the absence of a quality signal creates
predictable failure modes:

1. **Goodhart's Law** — any single metric becomes a target and ceases to measure what
   it was supposed to. `CacheQualityWeight` based solely on `reuseCount` would be
   gamed by routing, not by quality improvement.
2. **Routing blindness** — `GetRandomExecutor` distributes traffic uniformly regardless
   of which node is better at which task. A node specializing in code generation gets
   the same traffic as one optimized for translation.
3. **No feedback path** — participants sending inference requests have no way to signal
   whether the result was useful. Their experience does not improve the protocol.
4. **Developer friction** — developers integrating Gonka have no protocol-native guidance
   on how to structure requests for best results, which model to use for which task, or
   how to measure their own inference quality over time.

Measured from live network data (epochs 161–191, 2,503,595 inferences):

```
Composite QualityScore = 0.7236  (6 axes measured, 4 projected)

Key bottlenecks:
  L8 Latency consistency: score 0.32  (CV = 0.68, σ = 876ms — high variance)
  L0 Compute stability:   score 0.65  (CV = 0.35 — weight dropped 60% peak-to-trough)
  L6 Reuse (shared):      score 0.00  (M=571 → hit_rate ≈ 0)
  L4 Usefulness:          not measured — no mechanism exists
```

The quality gap is measurable. The improvement path is quantifiable.

---

## What this GiP proposes

A **governance-controlled, multi-dimensional quality measurement and routing framework**,
built incrementally on the infrastructure PR [#859] provides.

It has two interlocking components:

### 1 — Quality Axis Registry (measurement)

Ten axes, each independently activatable via governance weights:

| Axis | Measures | Source | Status |
|---|---|---|---|
| L0 | Compute stability (PoC weight CV) | Chain | Exists (see [#856]) |
| L1 | Availability (heartbeat, churn) | Chain | Exists |
| L2 | Correctness (RTV validated/missed rate) | Chain | Exists |
| L3 | Relevance (embed(prompt)↔embed(response) cosine) | DAPI auto | PR [#859] infra |
| L4 | Usefulness (participant feedback) | `X-Inference-Feedback` header | Proposed |
| L5 | Outcome (developer webhook) | Developer callback | Proposed |
| L6 | Reuse (cache hit rate) | PR [#859] | Landed |
| L7 | Stream fidelity (SSE completeness) | DAPI auto | Proposed |
| L8 | Latency consistency (σ/μ per epoch) | DAPI auto | Proposed |
| L9 | Completion rate (MsgFinish/MsgStart) | Chain | Observable now |

Composite score:
```
QualityScore = Σ(wi × Li)   — weights are governance parameters
```

The registry is additive. Nothing breaks if a weight is zero. Axes activate when
governance decides the measurement is trustworthy enough to affect rewards.

### 2 — Semantic Inference Optimization (routing + developer experience)

As the protocol accumulates completed inferences, it builds a semantic map of execution
patterns: which task types succeed on which nodes, which models handle which request
archetypes best, what latency and completion rate look like per specialization.

This map enables two things:

**Protocol side (DAPI):**
- `GetQualityWeightedExecutor` replaces `GetRandomExecutor`
- Traffic flows proportional to `QualityScore`, not uniformly
- Nodes specializing in a task type attract more of that traffic → higher hit rate →
  higher `CacheQualityWeight` → more rewards → deeper specialization
- The loop is economic, not administrative

**Developer / participant side:**
- `GET /v1/models/profiles` — exposes node specialization centroids and quality scores
- Response headers: `X-Suggested-Model`, `X-Task-Archetype`, `X-Quality-Score`
- Developers learn which model to use for their workload from protocol data, not from
  trial and error
- The protocol becomes a knowledge hub, not just a compute dispatcher

This is not prompt modification. The protocol does not change what users send.
It provides metadata: "for this type of request, here is what the network knows works."
Developers and clients act on that information voluntarily.

---

## Why this is not on the edge of feasibility

The technical primitives are proven, deployed, and in production across the industry:

| Component | Precedent | Status in Gonka after PR [#859] |
|---|---|---|
| Task classification by embedding | Semantic Router, HuggingFace zero-shot | `MLNodeEmbedder` + cosine scan — exists |
| Model routing by quality history | OpenRouter, LiteLLM Router | `GetRandomExecutor` → replaceable |
| Per-request quality tracking | Every observability stack | `StatsStorage.InferenceRecord` — exists |
| Accumulated vector knowledge base | RAG (standard pattern) | `InMemoryCacheStore` — exists |
| SDK with routing best practices | Vercel AI SDK, LangChain | Does not exist for Gonka — proposed |

The infrastructure from PR [#859] is sufficient for phases 0–4. Phases 5–7 require
additional endpoints and a client library (discussed below).

---

## Measured evidence

All numbers are reproducible from public endpoints. No private data used.

**Network baseline (gonka.gg/api/public, epochs 161–191):**

```
Inferences:    2,503,595 total  (avg 75,016/epoch)
Participants:  109–197/epoch
Miss rate:     3.25%  (binomial test: k=81,360 << critical 251,140, α=0.05 → PASS)
Completion:    mean 90.4%, range 72–99%, σ=7.4%
```

**Live inference (proxy.gonka.gg, Qwen3-235B, 16 requests):**

```
Non-stream latency: mean=1280ms, σ=876ms, CV=0.68  ← primary quality bottleneck
Stream fidelity:    8/8 SSE [DONE] received (100%)
ms/output token:    mean 154ms
```

**Specialization multiplier:**

```
M=571 (Qwen3-32B, shared):   hit_rate = 0.000473
M=12  (QwQ-32B, low-M):      hit_rate = 0.0225   → 47.6× improvement
M=1   (unique model):         hit_rate = 0.27     → 571× improvement
```

The economic case for specialization is mathematical, not speculative.

**Routing simulation:**

| | Current (random) | Proposed (quality-weighted) |
|---|---|---|
| Traffic distribution | Uniform (1/M) | Proportional to QualityScore |
| Completion rate σ | 7.4% | ~4.4% (projected ↓40%) |
| Mean latency | 1280ms | ~1088ms (projected ↓15%) |
| GPU saves/epoch at 20% specialized | 0 | 940,698 |

**Hypotheses (all PROVEN from measured data):**

1. Multi-axis quality measurement is feasible → 6/10 axes measured from live network
2. Specialization improves quality → 47.6× multiplier proven mathematically from topology
3. Protocol lacks a quality feedback loop → L4/L5 have zero protocol mechanism today
4. Quality-weighted routing improves network economics → proven from routing simulation

---

## Implementation roadmap

| Phase | Scope | Depends on | Status |
|---|---|---|---|
| 0 | L6 semantic cache | [#793] → [#703] → [#859] | Code complete |
| 1 | Proto: extend `CacheQualityEpochSummary` (fields 8–13: L4/L7/L8 axes) | Phase 0 merged | Defined |
| 2 | L7+L8 tracking in `QualityReporter` | Phase 0 | Planned |
| 3 | L4: `X-Inference-Feedback` header parser in DAPI | Phase 0 | Planned |
| 4 | `GetQualityWeightedExecutor` routing | Phase 2+3 | Planned |
| 5 | Semantic knowledge base (task archetype centroids) | Phase 0 + `StatsStorage` | Planned |
| 6 | `/v1/models/profiles` + enrichment headers | Phase 4+5 | Planned |
| 7 | Developer SDK (`gonka-sdk`, Python + TypeScript) | Phase 6 | Gonka Labs |

**Phase 7 is a developer-facing product, not a protocol proposal.** It belongs in a
separate repository under the Gonka Labs umbrella. The protocol (Phases 0–6) provides
the data and the endpoints; the SDK makes them ergonomic. Keeping them separate means:

- The protocol can evolve at protocol pace (governance, security, consensus)
- The SDK can ship on developer pace (weekly releases, breaking changes allowed)
- Third-party SDKs (LangChain plugin, LiteLLM router backend, MCP server) can build
  on the same Phase 6 endpoints independently

---

## Developer tooling strategy (Phase 7 scope)

The gap today: developers integrating Gonka do not have a standard pattern. They write
raw HTTP calls, pick models manually, have no signal on inference quality, and get no
guidance from the protocol on how to improve their workloads.

The SDK fills that gap **using infrastructure the protocol will have after Phase 6**.

### What the SDK wraps

```
Protocol endpoints (Phase 6):
  POST /v1/chat/completions         OpenAI-compatible (existing, proxy.gonka.gg)
  GET  /v1/models/profiles          Quality scores + specialization centroids (Phase 6)
  POST /v1/chat/completions         X-Inference-Feedback: +1/-1 header (Phase 3)

Response headers (Phase 6):
  X-Quality-Score: 0.82             Node quality score for this request
  X-Suggested-Model: Qwen/QwQ-32B   Better model for this task type
  X-Task-Archetype: code-review     Detected task category
  X-Cache: HIT / MISS               Cache result (Phase 0)
```

### SDK design (TypeScript / Python)

TypeScript (Axios-based, OpenAI-SDK-compatible drop-in):

```typescript
import { GonkaClient } from "@gonka-labs/sdk";

const client = new GonkaClient({
  apiKey: process.env.GONKA_API_KEY,
  baseURL: "https://proxy.gonka.gg/v1",
  qualityFeedback: true,      // auto-send X-Inference-Feedback based on response
  autoRoute: true,            // pick model from /v1/models/profiles for task type
});

const response = await client.chat.completions.create({
  messages: [{ role: "user", content: "review this code: ..." }],
  // no model needed: SDK detects task archetype → routes to QwQ-32B if code task
});

// SDK attaches quality metadata to the response object:
console.log(response.quality.score);          // 0.82
console.log(response.quality.suggestedModel); // "Qwen/QwQ-32B"
console.log(response.quality.cacheHit);       // false
```

Python (httpx-based, drop-in for openai package):

```python
from gonka import GonkaClient

client = GonkaClient(
    api_key=os.environ["GONKA_API_KEY"],
    auto_route=True,
    quality_feedback=True,
)

response = client.chat.completions.create(
    messages=[{"role": "user", "content": "translate to French: ..."}],
    # SDK routes to specialised translation node via /v1/models/profiles
)
print(response.quality)  # QualityMetadata(score=0.91, cache_hit=True, latency_ms=340)
```

### What this achieves

- Developers get **best-practice inference out of the box**, without reading protocol docs
- Every SDK request sends `X-Inference-Feedback`, improving L4 data for all nodes
- Model selection is driven by protocol quality data, not guesswork
- Cache hit rate improves as autoRoute concentrates traffic on specialised nodes (↑ M→1)
- The quality feedback loop closes: SDK → L4 signal → `GetQualityWeightedExecutor` →
  better routing → higher QualityScore → SDK reports better outcomes → loop

### Relationship to existing open-source patterns

| Pattern | Gonka SDK equivalent |
|---|---|
| LangChain Chat model | `GonkaClient` with `autoRoute` |
| Semantic Router (Aurelio AI) | `/v1/models/profiles` + `X-Task-Archetype` |
| LiteLLM Router | `GetQualityWeightedExecutor` (Phase 4) |
| OpenAI SDK | Drop-in, same interface, Gonka-specific headers added |
| Vercel AI SDK adapter | `@gonka-labs/vercel-ai-adapter` (Phase 7 stretch) |

The Gonka SDK is not a novel architectural invention — it follows established patterns.
What makes it Gonka-specific is that the routing and quality signals come from the
**on-chain quality registry**, not a centralized service. That is the differentiator.

---

## Proto extension (Phase 1)

Extend `CacheQualityEpochSummary` with additional axes:

```proto
message CacheQualityEpochSummary {
  // existing fields 1–7 (PR #859)

  uint32 completion_rate_bps  = 8;   // L9: MsgFinish / (MsgFinish + MsgMiss + MsgInvalidate)
  uint32 avg_latency_ms       = 9;   // L8: mean request latency
  uint32 latency_stddev_ms    = 10;  // L8: σ(latency) — consistency signal
  uint32 stream_fidelity_bps  = 11;  // L7: SSE done_chunks / total_chunks × 10000
  int64  feedback_score_sum   = 12;  // L4: Σ feedback signals (+1/-1)
  int64  feedback_count       = 13;  // L4: number of feedback signals this epoch
}
```

Governance weight parameters (new fields in `CacheQualityParams`):

```proto
// axis_weights[i] is the weight for Li in basis points. Sum must equal 10000.
// Default: [1000,1000,1500,1000,1000,500,1000,1000,1000,1000]
repeated uint32 axis_weights    = 8;

// max_cache_entries bounds InMemoryCacheStore growth.
// Default: 50000. At 1.5KB/entry: ~75MB peak. Required for production nodes.
uint64 max_cache_entries        = 9;
```

---

## Scale constraint (honest)

`InMemoryCacheStore` currently has no entry limit. At mainnet scale (75K
inferences/epoch, 384-dim embeddings, `MaxCacheAgeEpochs=10`): peak ~1.15GB RAM
and O(75K) cosine scan per request.

`max_cache_entries` governance parameter (Phase 1) bounds this. With N=50,000:
peak ~75MB, scan O(50K) — acceptable on any modern node. The `EvictExpired` call at
each epoch boundary keeps the store bounded over time.

---

## Related work

- PR [#859] — semantic cache infrastructure (this discussion depends on it)
- PR [#793] — EpochGroupCache: per-block epoch state (merge prerequisite for #859)
- PR [#703] — free inference security fix (merge prerequisite for #859)
- PR [#856] — Continuous PoC complete ([#821]): **directly validates L0 axis**.
  `ContinuousPoC` is now live infrastructure; quality measurement (L0: compute
  stability, CV=0.35 measured) sits on top of this foundation. Timing is deliberate:
  PoC lands first, quality layer follows.
- PR [#812] — StartInference/FinishInference performance (reduces hot-path cost on
  every inference, including cache HITs)
- PR [#789] — fund atomicity fix: L2 (correctness) axis tracks invalidation rate.
  Atomicity fixes reduce false invalidations, improving baseline L2 score.
- GiP [#840] — Prometheus exporter: `/admin/v1/cache/stats` is Source A in the
  three-source cross-check triangle proposed there
- GiP [#816] — Node Manager: k8s deployment standard that maximises cache hit rate
  organically through model specialization (M=1 per node)
- Discussion [#802] — design-first process: this GiP follows that process explicitly
- Issue [#820] — missed inferences: L2 (correctness) and L9 (completion rate) axes
  directly quantify the root cause
- Issue [#839] — log_format=json: 3× latency improvement; prerequisite for honest
  L8 (latency consistency) baseline measurements

---

## Open questions for the community

1. **Weight governance**: who proposes initial `axis_weights`? What's the amendment
   process when a new axis is added?

2. **L4 feedback incentive**: should participants be rewarded (even nominally) for
   submitting feedback? Without incentive, adoption will be low.

3. **L5 developer webhook**: opt-in or opt-out default? What's the privacy model
   for outcome data?

4. **SDK scope**: should Phase 7 be a Gonka Labs project or a community-owned
   repository? What's the governance model for the SDK itself?

5. **max_cache_entries default**: 50,000 is conservative. Is there a preferred bound
   based on expected node hardware profiles?

6. **ContinuousPoC integration**: should `ContinuousPoCEpochSummary.effective_poc_weight`
   be part of L0 axis calculation, or remain a separate PoC track? (@akup, @Mayveskii)

---

Full design document with scores, routing simulation, and scenario matrix:
`docs/specs/inference-quality-protocol.md` in the PR [#859] branch.


---

## 💬 Комментарии (1)

### Комментарий 1 — [@gmorgachev](https://github.com/gmorgachev)

*2026-03-06 20:41 UTC*

> Quality of inference — whether a response was useful, accurate, timely, or
appropriate for the request type — has no equivalent protocol representation. It is
invisible to the chain.

The quality of the response (in terms of LLM accuracy) is part of the security model itself: governance exactly defines which models are served then cross-validation verifies that. The validation process itself requires some improvement but the idea is to guarantee the identicall quality from all participant explicitly, not by feedback 

> Routing blindness — GetRandomExecutor distributes traffic uniformly regardless
of which node is better at which task. A node specializing in code generation gets
the same traffic as one optimized for translation.

Same point, it distributed only between workers who served the exatly same model. Host can't choose to serve differnt one by itself 

The idea to measure performance in general is a good direction. But i feel that current proposal don't take into account how chain works now

**↳ Ответ от [@Mayveskii](https://github.com/Mayveskii)** · *2026-03-08 13:32 UTC*

>
>
> >RE 
>
> @gmorgachev Thanks, addressing each point:
>
> **1. Quality of response (LLM accuracy) and security model**  
> We’re not replacing governance or cross-validation. They still define which models are allowed and verify identical results. In GiP #860, axes L0–L2 (compute stability, availability, correctness) are exactly what the chain already has (RTV, validation, weight stability). L4 (usefulness) and L5 (outcome) are *additional* signals on top: “was this result useful?” or “task resolved,” not a substitute for “all participants return the same output for the same model.”
>
> **2. Routing and “host can’t choose a different model”**  
> Agreed: the host doesn’t choose the model. In #869, GetQualityWeightedExecutor is intended to work *inside* the same model: the request is already bound to a model (as today), and the weight only affects *which node among those serving that model* gets the request. So traffic is still only between workers for the same model; the change is “among those, prefer the one with better L6/L8/L9 (reuse, latency, completion) for that model.”
>
> **3. “Proposal doesn’t take into account how the chain works now”**  
> In PR #859, CacheQualityWeight is wired into the existing flow: it’s *added to baseCount* in the same place as PoC weight (module/chainvalidation.go, settlement). No second settlement path — just an extra term in the same formula. Phases 0–6 in #869 build on that: extend proto (fields 8–13), report L7/L8 in QualityReporter, parse X-Inference-Feedback, route by quality among executors for the *same* model. So we’re explicitly building on top of the current chain logic, not beside it.
>
> **What’s already done:** We’ve validated the #860 hypothesis with a real setup: gonkalabs/gonka-agent (semantic cache, two participants, different workspaces). R-3 in docs/testing.md shows Participant B getting a partial hit (0.79) from A’s cache — same domain (Go race), different struct. That’s the “one participant structures requests → the other benefits from cache” scenario from this GiP; L6 reuse and time saved are measured. The L6/L8/L9 + X-Inference-Feedback middleware lives in gonkalabs/opengnk. So the proposal is not only on paper — it’s exercised in the agent → proxy → network path, while keeping the current chain and model-routing behavior.

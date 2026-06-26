---
title: "#802 — Continuous PoC"
source: https://github.com/gonka-ai/gonka/discussions/802
discussion_number: 802
category: proposals
synced_at: 2026-06-26T09:52:55Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #802](https://github.com/gonka-ai/gonka/discussions/802) каждые 6 часов. 

# Continuous PoC

**Автор:** [@mtvnastya](https://github.com/mtvnastya) · **Категория:** :bulb: Proposals · **Создано:** 2026-02-25 05:12 UTC · **Обновлено:** 2026-03-26 17:37 UTC

---

## 📝 Описание

This proposal is closely related to proposal for [multi-model PoC](https://github.com/gonka-ai/gonka/discussions/800) and can be seen as it’s continuation.

# Problem 
If we want to serve small models - we need to do PoCs via small models as well (see proposal multi-model PoC).

But this opens us to an attack vector when a malicious host can deploy a small model quick enough to participate in both PoC and cPoC with new nodes that were not participating in users’ inference. This attack vector was the reason behind switching to PoCv2 inside vLLM and selecting a large model (Qwen3-235B-FP8) for it. 

Note: If someone still tries to cheat and doesn’t have 100% of their compute available at all times, in general, the network can catch such behaviour because of increasing miss rate - this works for large models. But in order to significantly utilize compute with deployed small models, the chain would have to serve an enormous amount of user inferences and overhead on recording their metadata would be more significant, which is a parallel engineering challenge the chain is solving now. Thus, for now,  it is practically impossible to catch any malicious behaviour of participants serving small models because their miss rate will never be high enough because of the underutilization of compute. This can be solved by proposal for [inference scaling](https://github.com/gonka-ai/gonka/discussions/801). 

# Proposal
Current implementation of POCv2 has quite an artificial limitation - the GPU executes only one type of computation at a time: either inference or nonce check. De-facto, it’s the exactly same computation internally and can be computed fully parallel if GPU allows (in the same batch, utilizing all engine’s optimizations like dynamic batching)

If we get rid of this limitation, there is no need to have different phases: POC and INFERENCE. POC can work in parallel with inference and verify all the hardware which is not utilized by real requests at the moment (maintaining utilization level not to slow-down user requests).

So, essentially if the host has 100 GPU but chain has requests to utilize only 0.5 of them, 99.5 will be verified by the POC procedure.

There is an open question how to properly “weight” how many nonces should be compensated by particular inferences with different input / output lengths. It’s quite important to make sure that the UX of real inferences doesn’t change (inference itself is not slower).

Such continuous POC would not introduce significant overhead as only lightweight commits are recorded on-chain. The real artifacts are stored locally and requested directly. The validation itself doesn’t have to cover 100% of the epoch block but can be randomized and trigger some-revalidation for malicious fragments.  

# Implementation
[to be discussed] 


---

## 💬 Комментарии (3)

### Комментарий 1 — [@gmorgachev](https://github.com/gmorgachev)

*2026-02-25 05:16 UTC*

Implementation of this idea would directly enable adding back small GPUs. 

### Комментарий 2 — [@Laboltus](https://github.com/Laboltus)

*2026-02-27 08:22 UTC*

24/7 100% utilization of GPUs will lead to high power consumption, servers overhead, performance issues etc., right ?

### Комментарий 3 — [@blizko](https://github.com/blizko)

*2026-03-03 09:25 UTC*

Whilst having mathematical beauty - this solution has a serious adverse effect of high energy consumption. This drives away from the philosophy of devoting most of the compute power to inference.
There is also a significant risk that during high inference load, the compute capacity for generating nonces might be very low, thus making the reconciliation of PoC compute vs inference extremely challenging on the long run.

The primary problem is a scenario where a malicious actor can bypass the cPoC and PoC by loading the model fast enough and generating enough nonces within the generation window.

Let’s consider some alternatives.
In regards to Proof of Compute:
-	Immediate cPoC generation start. In this case nonce generation starts on the trigger block - no grace period is allowed. In this case the malicious actor is forced to cover the load time of the model with higher amounts of compute (rough ratio - `1 / (window time – load time)`). E.g. - if model load time takes 50% of the generation window time, to achieve the same amount of weight it is required to have 2x of the original compute capacity.
-	Enhancement - Short PoC / cPoC generation window. If we assume that the overall generation window is close to model load time – it is near to impossible to achieve the confirmation ratio of 50% without having the compute capacity online.

In regards to overall network health (avoiding abuse of serving only small models):
-	Weight cap per MLNode for specific models. We introduce a maximum weight that can be achieved by an MLNode. In this scenario we might introduce a hard barrier for entry with specific GPUs, making it more efficient to be hosted on mid-range GPUs, and leave the capacity open for high-end models
-	Network enforced model selection. The initial design included the idea that validators can serve multiple models, and it is decided by the network which validators serve the exact model (demand induced dynamic changes). This mechanism can be used to ensure that only a range of MLNodes across the whole network are selected to serve the specific small model. This significantly lowers the chances that a selected validator will be interested in manipulating with allocated compute power.

**Note** – This also has an adverse effect that some validators might be excluded from the network due to absence of demand. However in case the model range exceeds the network capacity, that should not be an issue. Also - that is actually a self-regulation mechanism once the block subsidy is lower than inference processing revenue.
   



**↳ Ответ от [@sysmanalex](https://github.com/sysmanalex)** · *2026-03-03 17:40 UTC*

> Suggesting: 
> 1. reward distribution model RDM
> - **Reward distribution based on model consumption economics and daily revenue**
>
> Rewards are distributed proportionally to the actual compute consumption of different models (e.g., the number of inference requests, input/output tokens) and their contribution to network revenue per day from real consumers. 
>
> Distribution does not occur immediately, but rather after 24 hours, based on actual metrics (miss rates, utilization, revenue share). This incentivizes honest behavior, as fake workloads will not yield immediate benefits.
> This mechanism is essentially easy to organize and maintain. it guarantees a dynamic and fair market. 
> The rewards distributed are the same as the rewards paid out.
> QWEN3 5 nodes weight/proportion -  180k gnk paid 24h ok, 
> GLM 20 nodes weight/proportion -  285k gnk ok. simple, transparent, useful stats.
>
> Advantages: Reduces risks from small models (low income - low rewards), all data is already available
>
> 2. Hard assignment of HW GPUs to resource - based groups - small to small models, or amd to amd more effective models & etc.
>
> Description: Classify GPUs by power (VRAM, cores, flops, mem, disk & etc ) and lock them into groups: 
> small GPUs (e.g., <8GB VRAM) only run small models (<1B params), medium → medium models, large → large models. This prevents exploits where small GPUs fake-load large models just for PoC.
>
> Simpler PoC: Register GPU specs on node join (self-report + validation via benchmark nonce).
> require: To implement a network enforcer to dynamically assign models to groups based on demand.
> still require RDM.
>
> 3. a lot of hybrid models, imho doesn't make it more clear otherwise, all tricks for - complex/short PoC/cPoC  + generation windows + weight caps + grace - only overcomplicate all process & add in times more complex coding/checks.

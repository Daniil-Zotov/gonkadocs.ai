---
title: "#817 — Network reliability and performance coordination (slow nodes, DB growth, missed inference)"
source: https://github.com/gonka-ai/gonka/discussions/817
discussion_number: 817
category: general
synced_at: 2026-07-02T04:31:40Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #817](https://github.com/gonka-ai/gonka/discussions/817) каждые 6 часов. 

# Network reliability and performance coordination (slow nodes, DB growth, missed inference)

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Категория:** :speech_balloon: General · **Создано:** 2026-02-27 21:05 UTC · **Обновлено:** 2026-03-12 19:01 UTC

---

## 📝 Описание

**Goal:** collect signals, converge on root causes 

This discussion is for high-level coordination and evidence gathering. Implementation work is tracked in the linked epics (issues).

Topics:
1) Node slowdowns reported by multiple hosts over the last few days
2) `application.db` growth (pruning not effective)
3) Missed inference on some nodes  

Notes
- If you have partial data, post it anyway.  
- If you want to help implement, comment on the relevant issue 

---

## 💬 Комментарии (3)

### Комментарий 1 — [@icydark](https://github.com/icydark)

*2026-03-03 07:18 UTC*

### Signal 502 / missed requests on 4090 when handling large-token requests — proxy read timeout (900s)

**Environment**
GPU: RTX 4090 (48GB)

**What we're seeing**
We see some chat completion requests end in **502 Bad Gateway** and effectively count as missed inference. From our logs:
1. **vLLM** logs: `Aborted request chatcmpl-xxx`
2. **API proxy** logs: `Failed to connect to vLLM backend` → `httpx.ReadTimeout`
3. Client receives **502** for `POST /v1/chat/completions`

**Pattern we identified**
- The failing requests are **long-running**: long prompts (e.g. multi-document legal extraction) + high `max_tokens` (e.g. 5000), total time can exceed **15 minutes**.
- The proxy uses a **read timeout of 900 seconds (15 min)**. When the request runs that long, we hit that timeout, the stream breaks, vLLM aborts the request, and we return 502 → **missed request**.

**Log**
```
2026-02-27T05:35:45.999662386Z INFO 02-26 21:35:45 [logger.py:43] Received request chatcmpl-8e0cadf6a2e64563a1e5a8f914c96fdf: prompt: ... params: SamplingParams(n=1, presence_penalty=0.0, frequency_penalty=0.0, repetition_penalty=1.0, temperature=0.1, top_p=2026-02-27T05:35:45.999662386Z 0.8, top_k=20, min_p=0.0, seed=922553843, stop=[], stop_token_ids=[], bad_words=[], include_stop_str_in_output=False, ignore_eos=False, max_tokens=5000, min_tokens=0, logprobs=5, prompt_logprobs=None, skip_special_tokens=False, spaces_between_special_tokens=True, truncate_prompt_tokens=None, guided_decoding=None, extra_args=None, enforced_token_ids=None, prompt_token_ids: None, prompt_embeds shape: None, lora_request: None, prompt_adapter_request: None.
2026-02-27T05:35:46.000070586Z INFO 02-26 21:35:45 [async_llm_engine.py:212] Added request chatcmpl-8e0cadf6a2e64563a1e5a8f914c96fdf.
...
2026-02-27T05:50:45.969437878Z INFO 02-26 21:50:45 [async_llm_engine.py:224] Aborted request chatcmpl-8e0cadf6a2e64563a1e5a8f914c96fdf.
2026-02-27T05:50:45.970448508Z 2026-02-26 21:50:45,969 - api.proxy - ERROR - Failed to connect to vLLM backend: 
```

So on our 4090 nodes, **large-token / long-duration requests** are more likely to hit this proxy timeout and be reported as missed.

**Questions**
- Is this hardcoded 15‑min proxy read timeout a known limitation elsewhere? We’re considering increasing the proxy read timeout for our deployment to reduce these misses.
- Lower-spec nodes (e.g. 4090, 48GB) can complete PoC but have trouble serving larger / long-running inference requests (e.g. proxy timeout → missed requests). Will the network support these nodes going forward?

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-03-04 00:53 UTC*

Hi @icydark! Thanks!

1. yes, it makes sense to try increasing the proxy read timeout on your deployment.
2. regarding lower spec nodes - it is subject to governance decisions and may evolve over time.  

### Комментарий 3 — [@tcharchian](https://github.com/tcharchian)

*2026-03-12 19:01 UTC*

https://github.com/gonka-ai/gonka/pull/867 & https://github.com/gonka-ai/gonka/issues/819

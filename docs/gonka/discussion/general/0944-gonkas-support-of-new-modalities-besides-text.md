---
title: "#944 — Gonka's support of new modalities besides text"
source: https://github.com/gonka-ai/gonka/discussions/944
discussion_number: 944
category: general
synced_at: 2026-06-18T05:03:09Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #944](https://github.com/gonka-ai/gonka/discussions/944) каждые 6 часов. 

# Gonka's support of new modalities besides text

**Автор:** [@tamazgadaev](https://github.com/tamazgadaev) · **Категория:** :speech_balloon: General · **Создано:** 2026-03-25 09:47 UTC · **Обновлено:** 2026-06-15 12:35 UTC

---

## 📝 Описание

I'd like to start a discussion on how we develop gonka to support new modalities on the network, like speech-to-text, image understanding, video generation etc.

The core tasks for any new modality are:
- How to validate inference in this modality
- How to run PoC based on this modality
- How much load a new modality can create on the network including internet traffic, storage, blockchain load etc.

I'd suggest to use this discussion as free chat on this, possible ideas and aggregator of proposals. 

---

## 💬 Комментарии (2)

### Комментарий 1 — [@baygeldin](https://github.com/baygeldin)

*2026-05-01 21:49 UTC*

Hello! I'm exploring the possibility of supporting the **Wan2.2-T2V-A14B** text-to-video model on the Gonka network, and I'd like to discuss a few obstacles that came up.

**Why this model in particular:** it's arguably the best open-source text-to-video model to date that has a permissive license (Apache 2.0). LTX-2.3 is comparable in terms of performance, but has a much more restrictive custom license which might present additional unnecessary hurdles.

## Inference validation
Current SOTA video generation models are predominantly based on **diffusion transformers** (DiTs). Unlike autoregressive transformers used in LLMs, DiTs don't build the final result token-by-token. Instead, they start with random noise and repeatedly de-noise it until it resembles the final result. While autoregressive transformers predict the next token, DiTs predict the *difference/distance* between the noisy input and the slightly less noisy output.

Currently, to validate inference in Gonka, executors store logprobs for each generated token, and then validators "replay" the inference and compare logprobs. This wouldn't work very well for DiTs because the predictions are much heavier (we can't just sample the DiTs prediction). More importantly, though, it doesn't even make sense to compare these predictions because in SOTA models the result we get from running the DiT is not the final result.

Specifically, in Wan2.2, DiT operates on a latent/compressed representation of the video, and to get the actual video frames we need to pass that latent representation through a VAE decoder (which is essentially a convolutional neural network). Additionally, to get the final video file it needs to do some post-processing and encode the frames into a video container.

To validate inference honestly and protect against tampering we need to compare the final result (the actual video file which hash we store on-chain). Unfortunately, given the above, it's not straightforward, but here's what I propose:
- I think it should be possible to get rid of most of the nondeterminism by supplying the same random noise as input to DiT (maybe we can even generate it by seeding PRNG instead of storing the input noise as an artifact on executor machines).
- Due to inherent nondeterminism of GPUs the result will never be the same, but I believe it will be virtually non-distinguishable to a human eye (this needs to be checked, though).
- Then, the question becomes *"Given the executor's video file, and the validator's video file generated from the same noisy latent, how can we tell that they are **perceptually** the same?"*.

I'm not sure yet what's the best way to answer this question, but here are some ideas:
- We can try encoding the executor's video via VAE encoder (which is not used during inference at all) into the latent representation, then compare how close it is to the one we got during the replay on the validator's side. 
- Or, perhaps, we can compare the two videos frame-by-frame using similarity metrics such as SSIM or PSNR.

It's also worth mentioning that is [TEE proposal](https://github.com/gonka-ai/gonka/discussions/951) is implemented, then another option would be limiting text-to-video models to the trusted environments.

## Proof-of-Compute
PoC should be specific to the model because the idea is to prove the computational capacity to run the model. Thanks to [multi-model PoC](https://github.com/gonka-ai/gonka/discussions/800) it's now possible to have different models with their own PoCs, but the problem is that it's still based on the LLMs architecture and is tightly [integrated into vLLM](https://github.com/gonka-ai/gonka/blob/main/proposals/poc/README.md) (which totally makes sense, by the way).

First of all, we would need to adapt the transformer-based PoC to DiTs (I suspect it'd be very similar to how it's currently done in the Gonka's vLLM fork, but this needs to be checked). However, as we saw above, video generation models have a more complex pipeline, so simply structuring PoC after the DiT part of the video model architecture may not be enough. Unlike LLMs that basically have a single computationally significant step (repeated forward passes through the transformer-based network), video generation models also have additional encoders (in case of Wan2.2 it's a [small text encoder](https://huggingface.co/docs/transformers/model_doc/umt5) for the text prompt, and the VAE autoencoder) and post-processing steps. According to the [Wan2.1 paper](https://arxiv.org/pdf/2503.20314) (see `4.3.1 WORKLOAD ANALYSIS`) DiT accounts to 85% of computation during training, so it's safe to assume that during inference the situation is at the very least not worse (and likely even better, e.g. 95%+). So, the question is, do we even need to account for other parts such as VAE autoencoder? Or is the overhead so small that we could simply disregard this difference? I'm leaning towards the latter.

Another issue, of course, is the fact that ML nodes run on vLLM which simply doesn't support other modalities. It seems that the best option is to make use of the [vLLM-Omni](https://github.com/vllm-project/vllm-omni) project which is built on top of vLLM and [supports Wan2.2](https://docs.vllm.ai/projects/recipes/en/latest/Wan-AI/Wan2.2.html). But it still seems like a huge undertaking and I can't realistically estimate how much effort would it take to migrate ML nodes to this.

## Pricing policy
When it comes to LLMs, pricing is straightforward: we simply charge per token. This works well because the models are autoregressive and, thanks to KV caching, the computational effort grows more or less linearly with the sequence length.

With video generation, we don't have such a metric. The good news is that the final price of a single inference should be pretty much the same if the requested resolution, frame count, and the number of de-noising steps is the same (no matter the prompt). But unlike with autoregressive models, the relationship between these parameters and the needed computational effort is not linear.

---

**TL;DR:**
- Inference validation seems solvable, but needs some experimentation.
- Proof-of-Compute issue is a bit more vague, especially in how much effort it'd take.
- Pricing policy needs some consideration.

I'd very much like to hear your opinions on this.

**↳ Ответ от [@baygeldin](https://github.com/baygeldin)** · *2026-05-08 16:20 UTC*

> (expanded on this here: https://github.com/gonka-ai/gonka/discussions/1155)

### Комментарий 2 — [@fedor-konovalenko](https://github.com/fedor-konovalenko)

*2026-05-08 12:48 UTC*

Our team recently conducted research into the feasibility of inference and validation for image2text models; the results can be found here. 

https://github.com/gonka-ai/gonka/issues/1026

At the current stage, we have implemented a baseline validation approach similar to the inference validation method used in Gonka. The next logical step would be to adapt and extend this approach specifically for multimodal image-based workflows.

As a continuation of this research, our team could explore inference and validation strategies for the Qwen 3 speech models family, including the TTS model from [Qwen3-TTS Collection](https://huggingface.co/collections/Qwen/qwen3-tts) and the ASR model from [Qwen3-ASR Collection](https://huggingface.co/collections/Qwen/qwen3-asr).

For ASR models, the existing validation strategy based on Top-N log-probability comparison could likely be reused with minimal adaptation, since the output remains token-based and deterministic enough for confidence estimation and reproducibility checks.

TTS validation, however, would require separate research because the output is continuous audio rather than discrete tokens. Several validation directions could be investigated:

**Spectrogram-based validation:**
- Convert generated audio into Mel spectrograms or log-Mel spectrograms and compare them against reference outputs.
- Use similarity metrics such as cosine similarity, MSE, SSIM, or perceptual distance between spectrogram embeddings.
- Spectrograms could be stored in compressed NumPy (.npz) format or serialized tensors for efficient offline comparison and regression testing.

**Round-trip validation:** (additional inference step is needed, more expensive)
- Pass generated TTS audio through an ASR model and compare the reconstructed text against the original prompt.
- Metrics such as WER/CER could provide indirect validation of intelligibility and stability.

**Audio quality metrics:**
- Evaluate objective metrics such as [PESQ](https://lightning.ai/docs/torchmetrics/stable/audio/perceptual_evaluation_speech_quality.html), [STOI](https://lightning.ai/docs/torchmetrics/stable/audio/short_time_objective_intelligibility.html), [SI-SDR](https://lightning.ai/docs/torchmetrics/stable/audio/scale_invariant_signal_distortion_ratio.html), or [DNSMOS](https://lightning.ai/docs/torchmetrics/stable/audio/deep_noise_suppression_mean_opinion_score.html) where applicable.
- These metrics may help detect degradation caused by quantization, backend changes, or inference optimizations.

**↳ Ответ от [@ivan-smetannikov-serokell](https://github.com/ivan-smetannikov-serokell)** · *2026-06-11 15:31 UTC*

>  Hi @fedor-konovalenko, we've been looking at ASR (speech-to-text) for Gonka too, and just wrote up a proposal: https://github.com/gonka-ai/gonka/discussions/1335. You mentioned the Qwen3 speech family here, and from our pre-research it clearly overlaps with what you're doing due to the architectural specifics. Are you already working on ASR, or is it still open?

**↳ Ответ от [@fedor-konovalenko](https://github.com/fedor-konovalenko)** · *2026-06-11 20:54 UTC*

> Hi!
>
> No, we haven't started implementation yet; we're still discussing plans and setting priorities. I'd be happy to collaborate and work together. I read your proposal, it's very well thought out. We can indeed start with models that are compatible with the existing validation mechanism. We can then distribute tasks across ASR to avoid duplicating the same areas.
>
> @ivan-smetannikov-serokell 

**↳ Ответ от [@ivan-smetannikov-serokell](https://github.com/ivan-smetannikov-serokell)** · *2026-06-12 18:38 UTC*

> Nice, thanks for the confirmation! We'll sort a few things out on our side next week and get back to you to work out the plan together then.

**↳ Ответ от [@a-kuprin](https://github.com/a-kuprin)** · *2026-06-13 09:40 UTC*

> And what about PoC for these cases?

**↳ Ответ от [@ivan-smetannikov-serokell](https://github.com/ivan-smetannikov-serokell)** · *2026-06-15 12:35 UTC*

> No full design yet, just wanted to re-confirm that this task is still available. But we think PoC should mostly reuse the sprint: same seeded random embeddings, just run through the ASR/TTS model's layers, in theory it should work for autoregressive models. For Qwen3-ASR it is a bit simpler than Whisper (due to the heavy audio encoder), so we can start with it to test the waters and then move forward with others.

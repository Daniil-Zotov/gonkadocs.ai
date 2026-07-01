---
title: "#1155 — Add support for video generation models"
source: https://github.com/gonka-ai/gonka/discussions/1155
discussion_number: 1155
category: proposals
synced_at: 2026-07-01T10:15:32Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1155](https://github.com/gonka-ai/gonka/discussions/1155) каждые 6 часов. 

# Add support for video generation models

**Автор:** [@baygeldin](https://github.com/baygeldin) · **Категория:** :bulb: Proposals · **Создано:** 2026-05-08 16:18 UTC · **Обновлено:** 2026-05-19 13:00 UTC

---

## 📝 Описание

## Motivation
Open-weight video generation models have improved significantly over the past few years and have reached a level of quality that makes them viable for real-world video production workflows. Adding support for these models to the Gonka network has the potential to reduce production costs. Additionally, it would open a path toward supporting other modalities in the future.

I propose to start with supporting text-to-video models as the most general case. More specifically, with the **Wan2.2-T2V-A14B** model because it seems to be the best open-source text-to-video model to date that has a permissive license (Apache 2.0). LTX-2.3 is comparable in terms of performance, but has a much more restrictive custom license which might present additional unnecessary hurdles at this point.

## Challenges
Let's first outline the challenges we face due to the architectural differences between video generation models and LLMs.
### Inference validation
Current SOTA video generation models are predominantly **diffusion transformers** (DiTs). Unlike autoregressive models such as LLMs, DiTs don't build the final result token-by-token. Instead, they start with random noise and repeatedly denoise it until it resembles the final result. While autoregressive transformers predict the next token, DiTs predict the _difference/distance_ between the noisy input and the slightly less noisy output (this difference is then applied to the input before we move to the next denoising step).

Currently, to validate inference in Gonka, executors store logprobs for each generated token, and then validators "replay" the inference and compare logprobs. This wouldn't work very well for DiTs because the predictions are much heavier (usually the same shape as the input latent) and we can't just *sample* the DiTs prediction like we do with autoregressive models predictions.

More importantly, though, it doesn't make sense to compare the DiTs predictions directly because the result we get from running the DiT is not the final result of running the model. Specifically, in Wan2.2, the transformer operates on a latent/compressed representation of the video, and to get the actual video frames we need to pass that latent representation through a VAE decoder (which is essentially a convolutional neural network). Additionally, to get the final video file it needs to do some post-processing and encode the frames into a video container.

To validate inference honestly and protect against tampering we need to compare the final result of the generation (i.e. the actual video file which hash we store on-chain), but due to inherent nondeterminism of floating point math in GPUs we can't rely on outputs being bitwise-identical.

### Proof-of-Compute
Unlike LLMs that basically have a single computationally significant step (repeated forward passes through the transformer-based network), video generation models inference pipeline is a bit more complex. In case of Wan2.2, it also has a [small text encoder](https://huggingface.co/docs/transformers/model_doc/umt5) (for the text prompt), VAE autoencoder, and post-processing steps. 

I believe that these differences could be largely disregarded because by my estimate, DiT denoising steps still seem to account for **>95%** of compute and **>80%** of VRAM needed during inference. It makes little sense for a node to trick PoC by saving on text encoder and VAE weights because negatives (such as failed validations) would outweigh the benefits. Thus, I think that proving that a given node is able to run the denoising steps should be enough.

### Pricing policy
When it comes to LLMs, pricing is straightforward: we simply [charge per token](https://github.com/gonka-ai/gonka/blob/d8b8e9073d1a420d344d3ecc33ef23957f4142b1/inference-chain/x/inference/calculations/inference_state.go#L200). This works well because the models are autoregressive and, thanks to KV caching, each new token can reuse the cached keys and values from previous tokens (except during prefill). This makes generation cost grow roughly linearly with the number of output tokens. In practice, this lets us approximate the cost of a single inference as something like `(prompt_token_count + response_token_count) * price_per_token`. This wouldn't work for DiTs.

In case of DiTs, we can think of latent patches as our tokens. Latent patches are small chunks of the model's latent representation. Unlike autoregressive models, however, DiTs process all latent patches together at each denoising step rather than generating them one at a time while relying on KV caching. Because self-attention operates over all patches, the cost of a single forward pass grows roughly quadratically with the number of latent patches. Additionally, the cost is also linearly driven by the requested number of denoising steps. 

## High-Level Solution

### Perceptual similarity for inference validation
As we saw above, in diffusion models we operate on the latent/compressed representations. The strength of that compression is defined by the VAE [stride](https://github.com/Wan-Video/Wan2.2/blob/42bf4cfaa384bc21833865abc2f9e6c0e67233dc/wan/configs/wan_t2v_A14B.py#L17) and the number of latent channels. For Wan2.2-T2V-A14B the [stride](https://github.com/Wan-Video/Wan2.2/blob/42bf4cfaa384bc21833865abc2f9e6c0e67233dc/wan/configs/wan_t2v_A14B.py#L17) is `[4, 8, 8]` and the the [number of channels](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B-Diffusers/blob/main/vae/config.json#L55) is `16`. With CFG (Classifier-Free Guidance) enabled, we make [two forward passes](https://github.com/huggingface/diffusers/blob/a851ce1058d5a465d7951687235cdaeac1978de2/src/diffusers/pipelines/wan/pipeline_wan.py#L620) per denoising step. Thus, we can estimate that if we were to save artifacts after each forward pass, for a single 1280x720@16FPS video with the duration of 5s over 40 denoising steps, it'd take ~750MB of storage for a video that itself is only about ~5MB compressed. This is too much for a single inference.

For this reason, I propose not to store any artifacts except the final video file itself. Instead, let's focus on re-generating the video from the original prompt in a way that our result is close enough to the original executor's result, so that we could compare them algorithmically.

First of all, we need to get rid of all sources of nondeterminism during inference that are under our control:
- **Starting noise latent.**  This is a tensor containing random Gaussian noise from which the final video is generated with each forward pass. It's the main source of nondeterminism. Often, it's controlled by the PRNG `seed` in inference engines, so it's not necessary to store it as an artifact during inference if we ensure that we can deterministically generate it from the same seed on two different machines.
- **Runtime/hardware stack.**  Different implementations could result different activations even with the same starting noise latent, and these differences compound over denoising steps leading to different results. Thus, to get a result that we can confidently say is visibly very similar, we need to make sure that we pin the runtime for each inference (e.g. attention backend used, GPU architecture, etc). This means that if the executor used NVIDIA GPUs to produce the result, then the validator should also use NVIDIA GPUs.

I believe that if we can pin these two sources of nondeterminism, then the result of the inference during validation should be close enough to the original result that we can then compare the videos frame-by-frame using [similarity metrics](https://github.com/chaofengc/IQA-PyTorch). Particularly, [DISTS](https://arxiv.org/abs/2004.07728) (Deep Image Structure and Texture Similarity) seems like a good option as it claims to have "tolerance to texture resampling" and "relatively insensitive to geometric transformation". [LPIPS](https://richzhang.github.io/PerceptualSimilarity/) is another popular option, but it may be a bit outdated at this point. However, the appropriate metric could only be found through experimentation.

### Adapt PoC algorithm to DiTs in vLLM-Omni
Currently, PoC is tightly [integrated into vLLM](https://github.com/gonka-ai/gonka/blob/main/proposals/poc/README.md#vllm) which doesn't support diffusion models. The first task would be to **migrate ML nodes to [vLLM-Omni](https://github.com/vllm-project/vllm-omni)**. Since [vLLM-Omni](https://github.com/vllm-project/vllm-omni) is built on top of vLLM, porting the existing logic from Gonka's vLLM fork to Gonka's vLLM-Omni fork shouldn't be a problem.

The next step would be **adapt the existing PoC mechanism for DiTs**. At the core, DiTs are still transformers, so the same approach should work: instead of offloading the inference model, we can randomly "scramble" how the weights are applied in a way that could be reproduced later given the seed.

However, there's one important difference: Mixture-of-Experts tends to work a bit differently in the diffusion models. More specifically, in Wan2.2-T2V-A14B the MoE router is not learned. It has two experts (low-noise or high-noise) which it chooses deterministically based on the current denoising step. High-noise expert is used early in denoising (for overall layout and motion), and low-noise expert is used later in denoising (for refining details).

This means that no matter how we transform each layer, the initial forward pass would always use the high-noise expert. So, we won't prove that the node actually runs the full 27B model since the node could have loaded only the high-noise expert. Thus, PoC approach needs to account for this situation by implementing additional hooks into the MoE router, and choose the expert randomly based on the seed.

### Separate pricing model for DiTs
As discussed earlier, DiT inference differs from LLM inference in several important ways. These differences are significant enough that DiTs require a separate pricing model.

Currently, the price per token for text models is determined dynamically [based on the model's utilization](https://github.com/gonka-ai/gonka/blob/d8b8e9073d1a420d344d3ecc33ef23957f4142b1/inference-chain/x/inference/keeper/dynamic_pricing.go#L100). We can reuse the same logic for DiTs, but we first need to define a **unit of execution**. A reasonable unit would be a single forward pass through the model using the minimum supported configuration, meaning the settings that result in the lowest computational cost, such as the minimum supported resolution, FPS, and other relevant parameters.

Then the question becomes: _"How do we compute the number of units for a given inference request?"_ The good news is that, unlike with autoregressive models, where we do not know the final number of generated tokens before processing the request, DiT inference cost can be pretty much estimated upfront from the requested parameters.

More specifically, we can derive the inference cost from *the number of latent patches* and *the number of forward passes*. The latent patch count depends on the requested width, height, and frame count, together with model-specific parameters such as the VAE stride and latent patch size. The forward-pass count depends on the requested number of denoising steps and model's implementation.

Then the inference cost can look like this:
```
inference cost = 
  price_per_unit * 
  forward_pass_num * (
    alpha * latent_patch_num^2 +
    beta * latent_patch_num
  )
```

Here, `latent_patch_num^2` captures the quadratic cost of self-attention over latent patches, while `latent_patch_num` captures the roughly linear parts of the forward pass, such as MLP layers, normalization, embeddings, etc. The coefficients `alpha` and `beta` are model-specific. They depend on the model architecture such as the number of layers, attention heads, MLP size, etc. We can estimate them empirically for each model.

## Implementation Roadmap
- STAGE 1: Verify the inference validation hypothesis
    - Generate a sufficiently large dataset of videos using the same parameters on different machines, while pinning the runtime and the starting noise latent.
    - Run experiments with different similarity metrics to determine which one works best.
- STAGE 2: Migrate to vLLM-Omni
    - Port the custom PoC logic from the vLLM fork to the vLLM-Omni fork.
    - Migrate ML nodes to vLLM-Omni.
- STAGE 3: Support Wan2.2-T2V-A14B
    - Implement inference validation.
        - Ensure that nodes validate inference only against matching nodes.
        - If a node does not match the executor's runtime, it should delegate validation to another node.
    - Implement Proof-of-Compute by adapting the existing PoC logic for DiTs.
    - Implement the DiT-specific pricing model.

## Open questions

***How confident can we be that pinning the runtime and the starting noise latent would consistently produce videos similar enough to compare with perceptual similarity metrics?***

My assumption is that this should hold in practice, but we can only verify it through experiments: generating videos on different machines capable of running the model and comparing the results.

If this hypothesis proves unreliable though, we could use a fallback approach: saving additional intermediate artifacts during inference. These artifacts would not be the DiT predictions themselves, but the DiT inputs, meaning the noisy video latents. We also would not need to save them at every denoising step. Instead, the executor could save a small number of intermediate noisy latents at selected steps.

During validation, the validator would run inference up to one of those steps and compare its intermediate latent representation with the one saved by the executor. If the distance between the two latent representations is too large, validation fails. If the distance is small enough, the validator can continue generation from the executor-provided latent and repeat the process from the next saved checkpoint, eventually comparing the final generated video as usual.

***Could we simply limit DiT inference to Trusted Execution Environments?***

Inference validation is probably the trickiest part of supporting DiTs, so it is tempting to assume that if the [TEE proposal](https://github.com/gonka-ai/gonka/discussions/951) is implemented, we could simply restrict text-to-video inference to trusted execution environments. However, TEEs appear to have their own unresolved issues, as shown by [tee.fail](https://tee.fail/). Therefore, even if TEEs become part of Gonka in the future, we should treat them as a possible additional layer of protection rather than as the primary validation mechanism for DiT inference.

_**How does conditioning factor into the DiT pricing model?**_

In the case of Wan2.2-T2V-A14B, the only conditioning comes from the text prompt. Since the prompt length is capped, I do not think we need to account for it separately when estimating inference cost.

However, if Gonka supports other DiT models in the future, they may use heavier forms of conditioning, such as images, audio, or video. These inputs could meaningfully affect inference cost. If that happens, the pricing model would probably need to be extended to account for conditioning cost.

---

## 💬 Комментарии (1)

### Комментарий 1 — [@baygeldin](https://github.com/baygeldin)

*2026-05-19 13:00 UTC*

I'd like to expand on the proposal to help us estimate how much compute we'd need for **STAGE 1**.

# Experiment design for video inference validation

I propose using the ["DiFR: Inference Verification Despite Nondeterminism"](https://arxiv.org/abs/2511.20621) paper as the main reference for testing our inference-validation hypothesis for video generation.

## Why DiFR is a useful reference

DiFR studies a similar problem: how to verify that inference was performed according to a declared specification despite benign nondeterminism. The paper focuses on text models, but I think their methodology is directly relevant here.

The parallels with our proposed approach:
- *Token-DiFR* approach results in a scalar score calculated against a trusted reference, indicating how closely the inference matches that reference. Similarly, our perceptual similarity metric would be a scalar score calculated against a reference video generation.
- *Activation-DiFR* extension is similar to the checkpointing idea described in the "Open Questions" section of the proposal in a sense that it compares intermediate inference artifacts against the verifier's corresponding intermediate inference states.

The paper provides a useful methodology:
- It defines one *canonical reference specification*.
- It defines *benign deviations*, meaning "correct-but-noisy" configurations. They simulate *"benign numerical noise by generating outputs using setups that are algebraically equivalent to the reference configuration apart from the ordering of floating-point reductions"* (e.g. different GPU microarchitectures).
- It defines *incorrect/malicious misconfigurations*: real deviations from the specification, such as wrong weights, incorrect quantization, incorrect sampling seed, etc.
- The key question is *threshold selection*: can valid cross-machine pairs be separated cleanly from invalid or tampered pairs?
- It evaluates detection quality at a target *false positive rate of 1%*.

*NOTE:* I also find it interesting that the paper claims to outperform TOPLOC (*"Activation-DiFR reaches AUC near 0.999 at 7.25 bytes per token, while TOPLOC requires 32 bytes per token to match this accuracy"*) thanks to relying on the efficient compression via Johnson–Lindenstrauss lemma.

## Configurations

### Reference specification
I propose using the following canonical configuration:
- NVIDIA H100 (or H200)
- no tensor parallelism
- no quantization (BF16 dtype)
- Cache-DiT disabled
- CFG enabled
- 40 denoising steps
- fixed PRNG seed per prompt

Additionally, we should pin the following for all configurations:
- inference engine (vLLM-Omni)
- attention backend (FlashAttention)
- scheduler settings (we can use [default settings](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B-Diffusers/blob/main/scheduler/scheduler_config.json))
- model revision (exact [HuggingFace](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B-Diffusers) commit hash)
- video encoder settings

### Benign deviations
Let's use configurations similar to the DiFR paper:
- NVIDIA A100 without tensor parallelism
- NVIDIA H100 with 4-way tensor parallelism (TP-4)
- NVIDIA A100 with 4-way tensor parallelism (TP-4)
	- *NOTE:* this acts as the worst-case benign deviation because it combines the other benign deviations.
- *(optional)* AMD MI300X
	- *NOTE:* if the NVIDIA benign deviations are too easy to separate from malign deviations, we could also stress-test the approach on AMD. I would not expect this to work well because it changes too many things at once.

*NOTE:* CUDA version, driver version, PyTorch version, and vLLM-Omni version may also affect the output, but probably less than the deviations listed above. The DiFR paper does not isolate these differences either; it even tests across different inference engines. I would therefore not include software-stack version changes in the experiment.
### Malign deviations
For video generation, we can consider these deviations as malign:
- 39 denoising steps
- 30 denoising steps
- FP8 quantized model
	- *NOTE:* this may be tricky; see the note below.
- CFG disabled
	- *NOTE:* this reduces the number of forward passes by half.
- Cache-DiT enabled
	- *NOTE:* this is not necessarily malign by itself, since it is a VRAM/performance tradeoff, but it is useful to test whether we can distinguish it from the reference generation.
- different PRNG seed
	- *NOTE:* the different-seed case is not a realistic cheating strategy by itself, but it is useful as a baseline because it should produce a visibly different result.

**Note on the FP8 model:** Ideally, the entire experiment should use vLLM-Omni as the inference engine so that the work can be reused in later implementation stages. However, it is not yet clear whether vLLM-Omni can run the quantized Wan2.2-T2V-A14B variant reliably. Its vLLM-Omni documentation marks Wan2.2 as  ["not validated"](https://docs.vllm.ai/projects/vllm-omni/en/latest/user_guide/quantization/fp8/#diffusion-model-qwen-image-wan22).

If it cannot, there are two options:
1. Skip the FP8 deviation in the first round and add it once vLLM-Omni supports it.
2. Run only this deviation through a different inference engine, for example run [Wan2.2-T2V-A14B-Diffusers-FP8](https://huggingface.co/nvidia/Wan2.2-T2V-A14B-Diffusers-FP8) via TRT-LLM, and clearly label it as a confounded deviation because both quantization and inference engine changed.

The first option is cleaner scientifically. The second option is still useful as a practical stress test, but the result should not be interpreted as isolating the effect of quantization alone.

## Dataset size
In the DiFR paper, the authors collected approximately *1 million output tokens per configuration*, with *9 configurations per model*. They then split the tokens in each configuration into non-overlapping batches and calculated a batch-level statistic by aggregating Token-DiFR scores. For a batch size of 10,000 tokens, this gives *~900 examples per model*. For a batch size of 1,000 tokens, this gives *~9000 examples per model* accordingly.

For video generation, we do not need to vary token batch sizes in the same way, because each generation has roughly the same number of frames. But we can still use this as a rough reference point for how many examples to generate for the experiment.

For each prompt, we can generate one reference video and one video for each benign and malign configuration. With one canonical configuration, 3 benign deviations, and 6 malign deviations, this means 10 generations per prompt.

Using roughly 1,000 prompts/examples would therefore produce about 10,000 video files.

There is no need to generate high-resolution videos for this experiment. We should use the minimum supported format:
- 832x480 resolution
- 81 frames at 16 fps (~5 seconds)

This is about **14 hours** of generated video in total.

## Artifacts to save
For each generation, we should save:
- full configuration description
- full generation parameters
- final encoded video file
- selected intermediate latents

The intermediate latents should include at least:
- the initial noise latent
	- *NOTE:* this is a sanity check to confirm that the fixed seed actually produces the same initial noise latent across configurations. Otherwise, we may end up measuring divergence caused by different starting noise rather than by the configuration change itself.
- the latent immediately before the high-noise to low-noise expert switch
- the final latent before VAE decoding

These latent artifacts are for the experiment, not necessarily for production. They help us understand where divergence appears. If final-video perceptual comparison proves reliable, production validation can avoid storing latents. If it proves unreliable, these latent checkpoints become the fallback validation path.

The encoded video files themselves should require about 35GB of storage. The selected intermediate latents should require roughly ~125GB if stored as BF16/FP16 tensors, or ~250GB if stored as FP32 tensors. So, overall, we'd need about **200-300GB** of storage.

## Compute estimate
We need to run the following configurations:
- H100 canonical configuration + 6 malign misconfigurations (7,000 generations)
- 4xH100 benign configuration with TP-4 (1,000 generations)
- A100 benign configuration (1,000 generations)
- 4xA100 benign configuration with TP-4 (1,000 generations)

Using the [official Wan2.2 T2V-A14B benchmark](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B#computational-efficiency-on-different-gpus) as a rough estimate:
- 1xH100: 326.9s/video
- 4xH100: 91.7s/video
- 1xA100: 785.7s/video
- 4xA100: 215.2s/video

This gives:
- H100: `(7,000 * 326.9 + 1,000 * 91.7 * 4) / 3,600 = ~738 GPU-hours`
- A100: `(1,000 * 785.7 + 1,000 * 215.2 * 4) / 3,600 = ~457 GPU-hours`

So the total is about **1,200 GPU-hours** for generation alone. To leave room for retries, debugging, failed runs, and small configuration changes, we should probably budget about **1,500 GPU-hours**.

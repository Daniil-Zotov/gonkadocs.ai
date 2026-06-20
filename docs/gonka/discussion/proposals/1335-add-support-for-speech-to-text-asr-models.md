---
title: "#1335 — Add support for speech-to-text (ASR) models"
source: https://github.com/gonka-ai/gonka/discussions/1335
discussion_number: 1335
category: proposals
synced_at: 2026-06-20T09:43:11Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1335](https://github.com/gonka-ai/gonka/discussions/1335) каждые 6 часов. 

# Add support for speech-to-text (ASR) models

**Автор:** [@ivan-smetannikov-serokell](https://github.com/ivan-smetannikov-serokell) · **Категория:** :bulb: Proposals · **Создано:** 2026-06-11 15:22 UTC · **Обновлено:** 2026-06-11 15:22 UTC

---

## 📝 Описание


Hello. We're a team at [Serokell](https://serokell.io) and we'd like to take on the ASR (speech-to-text) integration. We're scoping this proposal to ASR specifically (TTS is a separate problem and we're leaving it aside here). Below: why ASR is a good fit and which models, where inference validation gets hard, PoC and network-load impact, and our proposed plan.

## Why ASR, and which models

ASR is a good first audio modality for Gonka for three reasons. First, as far as we know, no decentralized network offers incentivized ASR today, so the slot looks open, and transcription is an established commercial market. Second, it's additive on the hardware the network already runs: ASR models are light relative to the current LLMs, so a datacenter-class GPU serves transcription at high throughput, which makes ASR a new modality and revenue stream on hardware hosts already run. As a side benefit, a relatively homogeneous server-GPU fleet makes the cross-hardware logprob-stability question potentially *easier* since most honest replays happen on similar silicon. And if the network ever broadens to smaller models, ASR's light footprint is easier to handle for new hosts. Third, the output is a token sequence, which is the precondition for reusing Gonka's logprob-distance validation at all. 

That third point carries an architectural constraint the discussion should be explicit about. Modern ASR splits into three families:

- **Autoregressive encoder-decoder** (Whisper): a conv+transformer audio *encoder* consumes a log-Mel spectrogram, and a transformer *decoder* autoregressively emits text tokens via cross-attention. Per-token logprobs exist and teacher-forcing is well-defined. This family is **validation-compatible** with the current flow.
- **Audio-LLM** (Qwen3-ASR, Voxtral): an audio encoder + adapter projects audio into the embedding space of a stock decoder-only LLM, which then decodes text. The output side *is* an ordinary LLM decoder. This family is also **validation-compatible.**
- **CTC / RNN-T / TDT transducers** (NVIDIA Parakeet/Canary): frame-synchronous decoding over a blank-dominated alignment lattice, with no per-text-token distribution conditioned on prior text. These are the *fastest* models on the leaderboards (RTFx ~2,700–3,400, 10–100× the AR families), but they are **not** compatible with the current `enforced_tokens` teacher-forcing. Validating them would need a different metric (lattice/forced-alignment scoring), i.e. a separate research effort and out of scope, at least for now.

So the fastest ASR architecture is precisely the one Gonka cannot cheaply validate. Our recommended candidates for now are **Qwen3-ASR-1.7B** as the primary target (SOTA-open accuracy, ~1.6%/3.4% WER on LibriSpeech test-clean/test-other, Apache-2.0, supported by vLLM's transcription endpoint, and an LLM-style decoder that matches the existing validation machinery) and **Whisper-large-v3** as an open baseline (MIT, widely used, ~2.0%/3.6% WER) for cross-GPU threshold calibration that the wider community can independently reproduce. In theory, a single `enforced_tokens` port covers both, since both are autoregressive-decoder models. If filling a large GPU more fully is a priority, heavier audio-LLMs like Voxtral-Small-24B exist, though the accuracy leaders are small, so the better use of big hardware here is high-batch throughput.

## Validation

Most of the work, and the one open technical unknown, is in this section.

**Only the serving layer exists today.** The Gonka vLLM fork already ships a `speech_to_text/` module implementing `/v1/audio/transcriptions`, but that is *upstream* vLLM code. So you can *serve* a transcript but what's missing is everything that turns serving into a Gonka *network* modality: running a model *and* proving it was run honestly, routing paid requests to it, and rewarding the work:

- **Validation**: the whole point. Gonka verifies inference by replaying it with `enforced_tokens` teacher-forcing and comparing logprob distributions, but that infrastructure (`vllm/validation.py`, the sampler overrides in `vllm/v1/sample/`, the `logprobs_mode` switch) is wired into the `chat_completion/` path only. It has not been ported to `speech_to_text/serving.py`. So today you can serve a transcript but cannot *prove* the executor actually ran the model, and a modality you can't validate can't be trustless.
- **DAPI**: there's no audio request path (no route, payload handling, or settlement wiring for audio), so a developer can't submit a paid, validated audio request at all.
- **On-chain**: no `ModelType` (a category enum, LLM vs VLM vs ASR, marking which serving/validation path a model uses; the model-name field already exists separately), no model registration, no audio pricing convention.

Because the `speech_to_text/` serving module and the `enforced_tokens` building blocks (on the chat path) already exist, the serving side is in place and the work is adding Gonka's validation on top.

Gonka's logprob validation security rests on a property we observe in practice: for the deployed LLMs/VLMs, the per-token logprob distribution from honest hardware is reproducible within a tight, calibrated tolerance, while a node that skipped the compute can't reproduce it. ASR makes that reproducibility harder to guarantee, and the problem is on the input side: the audio input first runs through a hardware-sensitive floating-point pipeline before any logprob is produced.

A text LLM's input is token IDs: discrete, exactly reproducible. ASR's input is raw audio that passes through a float-heavy front-end that text models don't have: decode/resample -> mel-spectrogram -> convolutional stem -> transformer audio encoder -> cross-attention into the decoder. Every stage is floating-point and architecture-sensitive (cuDNN convolutions and reductions are not bit-identical across GPU generations or batch shapes). `enforced_tokens` pins the *decoder token path* but does nothing to the *encoder*. So the leftover difference the validator's L1 distance measures for ASR is:

> decoder float differences + encoder/front-end float differences carried in through cross-attention.

For text, that second term is structurally zero (a text model has no encoder and no float preprocessing of its input, so nothing before the decoder can differ), which is why the LLM result is "settled." For ASR it's present and **unmeasured**. There is a direct precedent: this is the *same class* of problem the VLM work has shown to be tractable: a VLM has a visual encoder with the same character, and the #1026 / PR #1150 benchmarks report ~99% fraud detection. Two things also work in our favor: cross-attention averages over many encoder positions, which shrinks small encoder differences, and in the audio-LLM design the encoder output passes through the full LLM stack and is re-normalized at every layer. These are reasons to expect the honest cross-GPU spread to be small, but they are arguments from how the model works, and the number still has to be measured. Measuring the honest cross-GPU logprob spread (and confirming it stays below what a cheap fake achieves) decides whether the whole approach is viable, and it's the first thing we'd do.

**Input canonicalization problem.** Audio has no canonical byte form: the same sound as WAV vs MP3 vs different sample rates yields different bytes and different mel features. Two honest nodes that decode/resample differently will feed the model different audio and disagree, creating exactly the difference the validator is meant to read as fraud. So the protocol must mandate a canonical input *before* hashing and before the model: decode to a fixed format (e.g. 16 kHz mono PCM) with a **pinned resampling algorithm** and **pinned mel parameters**, hash the canonical PCM (not the submitted container), and distribute that artifact to executor and validator alike. Text inputs never needed this step.

**One concrete Whisper complication.** Whisper splits long audio at silence boundaries; different hardware can land on different split points due to FP rounding in silence detection, which changes the chunk boundaries and breaks teacher-forcing. Fix: store explicit chunk timestamps in the payload so the validator replays with identical boundaries instead of re-running silence detection.

**Our approach: extend the existing logprob validation to audio.** We keep Gonka's current proof-of-compute method: `CompareLogits`, the SPRT calibration pipeline, and the per-model `validation_threshold` all apply unchanged. There are two pieces of work here:

1. **A code change**: porting the `enforced_tokens` teacher-forcing to the encoder-decoder path. This mirrors the existing chat-path implementation and is well-scoped.
2. **An empirical study to set the `validation_threshold`.** The threshold has to be measured empirically. We run both candidate models across several GPU types, transcribe a speech dataset under teacher-forcing, collect the per-token logprob distributions, measure how far honest hardware diverges (the *honest band*), generate fraud scenarios (smaller/quantized/wrong model) to get a *fraud band*, and run SPRT calibration to find a threshold that separates the two, if one exists. This is the larger of the two tasks and carries most of the risk; it is what Phase 1 below covers.

If that study shows the honest logprob band is *narrow but nonzero*, the fallback is a hybrid: a looser threshold backed by occasional full re-execution.

## Proof of Compute

PoC needs no new infrastructure: the multi-model PoC infrastructure (`PoCModelConfig`) is already modality-agnostic.

**Phase 1 (no new infrastructure):** ASR hosts run the existing PoC sprint, exactly as VLM hosts do today. ASR-specific capability is proven through inference validation. This gets ASR on-chain without any new PoC work.

**Phase 2 (separate GIP, later):** an audio-specific sprint that mirrors today's token-generation sprint: in a fixed time window a host transcribes as much reference audio as it can, and the throughput is measured and validated the same way the current sprint is (as we understand the current PoC), so a host can't just self-report it. The reference audio has to be unpredictable (e.g. derived from a recent block hash and rotated each epoch) so it can't be pre-transcribed and cached. `PoCModelConfig.seq_len` can be repurposed for the clip length. The weight formula also has to account for ASR's throughput shape: the encoder is a fixed cost per 30-second window while the decoder scales with transcript length. This stays an open Phase-2 design question.

## Blockchain and network load

**On-chain: essentially unchanged.** We do not put audio on the chain, only the existing hashes/commitments. No `Inference` proto change is needed if we use a synthetic token count: `prompt_token_count = ceil(duration_seconds × 50)`. Pricing and the bandwidth-limiter work unchanged with that convention, and escrow follows the existing devshard model: the developer escrows up front, runs inferences against devshard hosts as needed, then settles and is refunded the remainder. Audio rides that same flow once it's priced by duration. No `model.proto` change is strictly required either: a model can be marked as ASR by convention (a `--task transcription` flag in `model_args` plus the audio content-type on the stored payload), which is how the validator would know to replay over the audio path instead of the chat path. As far as we can tell, this is how VLM is handled today. A `ModelType` enum in `model.proto` would be the cleaner, explicit way to mark it (and would label VLM properly at the same time), at the cost of a proto change and a state migration, but optional.

**Off-chain: the load grows.** Audio payloads are much heavier than text, so both storage and traffic increase. We'd store audio in a content-addressed object store (the hybrid backend in `managed_storage.go` already supports this); at audio sizes, inline Postgres BYTEA would bloat the tables. Validators fetch audio bytes only for the inferences they actually validate. At typical validation sample rates (~5–10%) the per-epoch volume stays manageable; the per-payload size increase is the main thing to plan for.

**DAPI is the most complex infrastructure change.** Audio uses `multipart/form-data` (a binary upload) where chat uses `application/json`, so it needs a new `post_audio_handler.go`; the JSON-oriented `ModifyRequestBody()` doesn't cover multipart. MLNode's proxy already forwards every `/v1/*` path verbatim, so **no changes are needed there**. The devshard path needs the same treatment at similar scope: the chain and devshard validators share one runtime (`shared_runtime.go`), so the audio validation branch is written once for both, and the devshard otherwise just needs the new model and its duration-based pricing, following the current flow.

## Proposed plan

We'd like to put a team on this and take it from research through integration. A tentative plan:

1. **Research and de-risk first.** Run the cross-GPU logprob-stability experiment that decides whether the logprob approach works for ASR: run Qwen3-ASR-1.7B and Whisper-large-v3 across the fleet's GPU types under teacher-forcing, measure how far honest runs diverge versus what a cheaper/wrong model produces, and check that a single threshold separates them. Settle the validation threshold, the input-canonicalization contract, and the final model choice. This is the main deciding experiment, it needs no fork or protocol changes, and we'd publish the results before committing to the rest.
2. **Implement the design based on findings.** Adding tests and documentation as we go: port `enforced_tokens` to the transcription path in the vLLM fork, add the DAPI audio handler and the ASR validation branch, and wire audio payload storage.
3. **Write integration tests** (testermint), covering happy and unhappy paths, including hosts that try to cheat validation (faked or cheaper-model transcripts).
4. **Document the handoff** to the community and the Gonka team, and submit the model registration and any governance proposal.
5. **[Optional]** Provide ongoing support and maintenance for the ASR modality.

We'd start with step 1 independently and share the results before going further. If the Machine Intelligence Lab team (@fedor-konovalenko) has active ASR plans, we'd welcome coordinating on where the work splits. Feedback on the approach, the candidate models, and the validation gate is especially welcome.

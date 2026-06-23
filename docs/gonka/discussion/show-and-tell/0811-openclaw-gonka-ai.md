---
title: "#811 — 🦞 OpenClaw + Gonka AI"
source: https://github.com/gonka-ai/gonka/discussions/811
discussion_number: 811
category: show-and-tell
synced_at: 2026-06-23T10:03:54Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #811](https://github.com/gonka-ai/gonka/discussions/811) каждые 6 часов. 

# 🦞 OpenClaw + Gonka AI

**Автор:** [@votkon](https://github.com/votkon) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-02-26 20:03 UTC · **Обновлено:** 2026-04-01 09:02 UTC

---

## 📝 Описание

I've put together a guide for connecting **OpenClaw** to **Gonka AI's decentralized GPU network** through the Mingles gateway.

## What This Enables

OpenClaw users can now run their AI agents on Gonka's distributed compute infrastructure instead of relying on centralized providers. Your personal assistant gets:

- ✅ Access to Gonka's tool-enabled Qwen3-235B model
- ✅ Decentralized inference across the network's GPU nodes
- ✅ Pay-as-you-go pricing with GNK tokens
- ✅ Full OpenAI API compatibility (drop-in replacement)

## Key Features

- Free 0.1 GNK trial credit to get started
- Simple setup through OpenClaw's configuration wizard
- Tool calling support for complex workflows

## Quick Setup

1. Get API key from https://gonka-gateway.mingles.ai/
2. Configure OpenClaw with custom gateway
3. Point to `https://gonka-gateway.mingles.ai/v1`
4. Start chatting!

**Full Tutorial:** https://gonkatalk.org/t/connect-openclaw-to-gonka-ai-decentralized-compute/47

---

This is one of the first integrations bringing Gonka's decentralized compute to end-user AI applications. Would love to hear feedback from the community or see other creative use cases!

---

## 💬 Комментарии (4)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-02-26 21:10 UTC*

Quick question about the free 0.1 GNK trial credit and what happens after. My understanding (please correct me if I’m wrong) is:

- This is mostly a Mingles-side question, and users can top up their balance directly from their own wallet, especially if they connect via Keplr.
- nference requests currently cost almost 0, so the 0.1 GNK trial credit should deplete very slowly.
- This is still more of a proof of concept, and the network currently enforces limits on transport agents (Mingles in this case). So if Mingles brings in a lot of users, requests per minute may be rate-limited until future network upgrades improve this.

Is all of the above accurate?

**↳ Ответ от [@votkon](https://github.com/votkon)** · *2026-02-26 21:14 UTC*

> yes, that's correct.
> Also you can get a free trial balance by signing up with you gmail account as well.

**↳ Ответ от [@aleks1k](https://github.com/aleks1k)** · *2026-02-26 21:16 UTC*

> yes, but  quick clarification: Mingles Gateway isn't a TA; there are currently only three of them, and all are managed by the gnka team. Gateway acts as a client and pays for inference from its internal wallet.

### Комментарий 2 — [@Dankosik](https://github.com/Dankosik)

*2026-03-06 23:07 UTC*

There is also a GonkaGate integration path for OpenClaw now: [guide here](https://gonkagate.com/en/docs/guides/openclaw-integration). It is an OpenAI-compatible custom provider (https://api.gonkagate.com/v1) with tool/function-calling emulation on the GonkaGate side, USD/prepaid billing, and $10 free credits at signup. In other words, this is not a GNK wallet/top-up flow; it is a standard API-key integration.

### Комментарий 3 — [@jingchang0623-crypto](https://github.com/jingchang0623-crypto)

*2026-03-19 12:07 UTC*

## 🦞 去中心化计算 + AI Agent = 完美组合

感谢这个集成指南！这是 OpenClaw 生态的重要进展。

### 为什么这很重要

**去中心化的价值**：
- 隐私保护：数据不出中心化服务商
- 抗审查：不依赖单一供应商
- 成本优化：按需付费，市场竞争

**Gonka + OpenClaw 的协同**：
```
OpenClaw (Gateway) 
    ↓
Mingles/GonkaGate (API Gateway)
    ↓
Gonka Network (分布式 GPU)
```

### 妙趣观察

我们在 [妙趣AI](https://miaoquai.com) 上看到：
- 用户对 LLM 成本敏感
- 隐私是核心需求
- 多供应商冗余是刚需

### 建议

1. **成本计算器**：帮助用户对比不同供应商的性价比
2. **自动故障转移**：主供应商挂了自动切换到 Gonka
3. **工具调用延迟报告**：对比中心化 vs 去中心化的性能

期待看到更多 OpenClaw + Gonka 的用例！🦞

---
*来自妙趣AI - AI工具导航与资讯平台*

### Комментарий 4 — [@gonkalabs](https://github.com/gonkalabs)

*2026-04-01 09:02 UTC*

Hi everyone - great thread. Community paths like the [Mingles gateway](https://gonka-gateway.mingles.ai/) (see the original post above) and [GonkaGate’s OpenClaw integration](https://gonkagate.com/en/docs/guides/openclaw-integration) make it easy to use **OpenClaw** with Gonka via a hosted OpenAI-compatible API and billing.

At **Gonka Labs** we wanted a **fully self-hosted** option: your keys stay on your machine, you pay inference with **GNK** on-chain (e.g. [gonka.gg/faucet](https://gonka.gg/faucet) for testing), and you still get a drop-in **OpenAI-compatible** endpoint for agents.

So we shipped **GonkaClaw** - a single shell script that:

1. Clones and runs **[openGNK](https://github.com/gonkalabs/opengnk)** (Docker) - same idea as in [OpenGNK – Show and tell (#890)](https://github.com/gonka-ai/gonka/discussions/890): local proxy, signed requests, discovery + multi-node retry, native tool calling where supported.  
2. Creates a **Gonka wallet** (`inferenced`-style flow, non-interactive keyring).  
3. Installs and **onboards OpenClaw** against `http://localhost:8080/v1` with **Qwen3 235B** as the default model, including patching client-side limits so the UI matches real network caps (large context window, completion token limits per what nodes accept).

<img width="846" height="528" alt="Снимок экрана 2026-04-01 в 12 00 13" src="https://github.com/user-attachments/assets/ff9dabf6-5b19-40c9-a600-8a21a5f64842" />


<details>
<summary><b>more indepth about how it works</b></summary>

- **1. openGNK (local Docker)**
  - Exposes a normal OpenAI-compatible surface: GET /v1/models, POST /v1/chat/completions (stream + non-stream), plus the bundled web UI at /.
  - **Discovery:** at startup the proxy calls  
    `GET {GONKA_SOURCE_URL}/v1/epochs/current/participants`  
    and parses `active_participants.participants[]`, keeping only hosts whose `index` is on the Transfer Agent allowlist (same whitelist concept as in the core proxy — only those nodes accept signed proxy traffic).
  - **Signing:** every upstream request is signed with secp256k1 using the same scheme as the official Gonka OpenAI clients (payload hash → timestamp → transfer address → deterministic ECDSA / low-S, etc.). Keys never leave the machine running the container.
  - **Routing:** after discovery, chat and model list traffic go to the discovered `inference_url` endpoints (not to the discovery URL). Retries rotate/failover across healthy nodes according to `GONKA_RETRY_STRATEGY` / `GONKA_MAX_RETRIES`.
  - **Tools:** we default to native tool calling (`NATIVE_TOOL_CALLS=true`, `SIMULATE_TOOL_CALLS=false`) for current Gonka nodes that support it; the proxy still normalizes message content (e.g. OpenAI “array of parts” → plain string) where the upstream expects it.

- **2. Wallet bootstrap (script-side)**
  - Downloads a pinned `inferenced` build (platform-specific zip from Gonka releases), creates a key with `keys add --keyring-backend test` (no OS keychain prompts), exports unarmored hex with `keys export … --unarmored-hex --unsafe -y`.
  - Registers the participant with  
    `POST {NODE_URL}/v1/participants`  
    `{"pub_key":"<base64>","address":"gonka1…"}`  
    so the address is known to the network before you fund and infer.
  - Writes `GONKA_PRIVATE_KEY` / `GONKA_ADDRESS` / `GONKA_SOURCE_URL` (and related flags) into `opengnk/.env` for Compose.

- **3. OpenClaw onboarding**
  - `openclaw onboard --non-interactive` with `--auth-choice custom-api-key`, `--custom-base-url http://localhost:<port>/v1`, `--custom-compatibility openai`, `--install-daemon`, plus skips for health/skills/channels where appropriate so CI-style runs don’t block on pairing.
  - After onboarding, a small Python patch updates `~/.openclaw/openclaw.json` so the custom model entry isn’t stuck at OpenClaw’s conservative defaults: we set `contextWindow` to match what the hosted catalog reports for this model (~240k), and `maxTokens` for completions to what vLLM on Gonka nodes actually accept (today that’s capped around 10k output tokens — if the client asks above that, the upstream returns 400 `max_completion_tokens exceeds limit`). That avoids confusing UI vs reality.

</details>

> It installs a NEW INSTANCE of openclaw.

**Try it:**

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/gonkalabs/gonkaclaw/main/setup.sh)
```

**Links**

- Repo: [github.com/gonkalabs/gonkaclaw](https://github.com/gonkalabs/gonkaclaw)  
- Landing page: [gonkalabs.com/gonkaclaw](https://gonkalabs.com/gonkaclaw)  
- Underlying proxy: [github.com/gonkalabs/opengnk](https://github.com/gonkalabs/opengnk) - and our hosted sibling [proxy.gonka.gg](https://proxy.gonka.gg) if you prefer not to run Docker locally.

This sits alongside the integrations already mentioned here: **hosted gateways** (API key / trial credits) vs **GonkaClaw** (wallet + local proxy + OpenClaw in one command). Feedback and PRs welcome on the repo.


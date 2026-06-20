---
title: "#890 — OpenGNK - A Local OpenAI-Compatible Proxy for Gonka"
source: https://github.com/gonka-ai/gonka/discussions/890
discussion_number: 890
category: show-and-tell
synced_at: 2026-06-20T09:43:20Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #890](https://github.com/gonka-ai/gonka/discussions/890) каждые 6 часов. 

# OpenGNK - A Local OpenAI-Compatible Proxy for Gonka

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-03-15 20:10 UTC · **Обновлено:** 2026-03-15 20:13 UTC

---

## 📝 Описание

When we were building and testing [proxy.gonka.gg](https://proxy.gonka.gg) - our cloud API endpoint for Gonka inference - we noticed a pattern in the community: developers also wanted to sign inference request and transmit them to the Network from local environment, keep their private keys on their own machines, and plug Gonka directly into their existing tooling without any intermediary (cloud proxy). They were asking for a self-hosted version of what we had built for ourselves.

Meet **opengnk** - a lightweight, Docker-based proxy that exposes the Gonka decentralised AI network as a fully standard **OpenAI-compatible API**, running entirely on your own machine.

**Currently, statistics are:**

- 2k views in a month

  258 installs

![telegram-cloud-photo-size-2-5312177661398423022-y](https://github.com/user-attachments/assets/9e277473-d4d8-44c6-845e-5537ca9e53bd)



***

### Why this exists

As we all know, the Gonka network is a decentralised inference network. Nodes run GPU hardware, accept signed inference requests, and return completions. Every application in the world that does AI - from LangChain agents to Cursor to your own Python scripts - speaks the OpenAI protocol. The gap between "I have a Gonka account" and "I can use Gonka in my app" was real friction (especially with TransferAgent whitelists - potential need for multiple nodes to send requests to, etc). We just saw a lot of questions about how to use inference, and tried to solve the arising "problem". Also, we have a faucet (gonka.gg/faucet) thus enabling users to test inference from local environment for free.

opengnk eliminates gap entirely. You point any OpenAI-compatible client at `http://localhost:8080/v1` and it just works. No SDK changes. No custom integration code. No vendor lock-in.

***

### What it does

**OpenAI-compatible REST API**

The proxy exposes `/v1/models` and `/v1/chat/completions` - both streaming and non-streaming - with the exact same request and response shapes as the OpenAI API. Any library or tool that supports a custom `base_url` works out of the box.

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",
)

response = client.chat.completions.create(
    model="Qwen/Qwen3-235B-A22B-Instruct-2507-FP8",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

That is the entire integration. The same snippet works with TypeScript, curl, LangChain, LlamaIndex, or anything else that speaks OpenAI.

**Transparent request signing**

Every request to a Gonka node must be signed with your secp256k1 private key. opengnk handles this entirely in the background - your keys stay on your machine, and every upstream request is signed with ECDSA before it leaves the proxy. You never touch the signing logic yourself.

**Automatic endpoint discovery**

The Gonka network has many participant nodes. opengnk automatically fetches the active participant list from a genesis node, filters it to healthy, whitelisted Transfer Agent nodes, and routes your requests there. If a node is unhealthy or rejects the request, the proxy handles it. You never pick nodes manually.

**Multi-wallet round-robin**

A single wallet may fall under rate limits. OpenGNK supports multiple wallets configured as a comma-separated list, and round-robins requests across them automatically. This multiplies your effective throughput proportionally to the number of wallets:

```env
GONKA_WALLETS=privkey1:gonka1addr1,privkey2:gonka1addr2,privkey3:gonka1addr3
```

Each request cycles to the next wallet. The proxy logs which wallet was used so you can verify the distribution.

**Built-in web chat UI**

There is a full chat interface at `http://localhost:8080` - no separate installation needed. It is useful for testing, exploring models, and demonstrating the proxy to others. It also shows the privacy sanitization diff panel (more on that below).

***

### Tool / function calling

Tool calling is one of the most important features for agentic AI workflows, and Gonka nodes had varying levels of native support for it (prior to recent update). opengnk handles both cases - when native TC is supported and when not.

**Native mode** (for nodes deployed with `--enable-auto-tool-choice`or similar) .env of the opengnk shall be:

```env
NATIVE_TOOL_CALLS=true
```

The proxy forwards your `tools` and `tool_calls` fields unchanged, and automatically flattens OpenAI-style array content (`[{"type":"text","text":"..."}]`) to plain strings that Gonka nodes require. All message types are normalized - including `role: "tool"` messages - so the upstream never receives a mixed content format.

**Simulation mode** (fallback for nodes without native support) can be turned on with .env config:

```env
SIMULATE_TOOL_CALLS=true
```

This is the more interesting one. When a node does not support native tool calling, the proxy:

1. Strips the `tools` and `tool_choice` fields from the request (which the upstream would reject)
2. Injects a system prompt that describes the available tools and instructs the model to respond with structured JSON
3. Parses the model's JSON output
4. Converts it back into the standard OpenAI `tool_calls` response format - `finish_reason: "tool_calls"`, `content: null`, structured `tool_calls` array

Your application sees a perfectly standard OpenAI response and handles the tool-call round-trip as usual. The full cycle - ask → tool call → tool result → final answer - works exactly as it does with OpenAI, in both modes.

***

### Privacy sanitization

> Community requested in TG Chats

This is the feature we are proud of from a technical standpoint.

The proxy can automatically strip sensitive data from your messages before they leave your machine, and restore the original values in the response. The upstream LLM operates entirely on placeholder tokens - it never sees your real data.

**What gets redacted:**

- API keys and tokens (`sk-`, `pk-`, `ghp_`, `Bearer`, etc.)
- Email addresses and phone numbers
- Full person names (English and Russian)
- Credit card numbers and IBANs
- Private keys and credentials of any format

**How it works:**

1. Your message arrives at the proxy
2. Classifiers scan the text and replace sensitive values with stable placeholders (`«TOKEN_000001»`, `«TOKEN_000002»`, ...)
3. The same token is reused if the same value appears multiple times - so the LLM can reason consistently about it without ever knowing what it is
4. The redacted message is forwarded to the upstream node
5. When the response comes back, placeholders are swapped back to the originals before your app sees them

The web UI shows a side-by-side diff of what you typed versus what was sent, with sensitive values highlighted.

**Two classifier layers run in parallel:**

The **NER sidecar** is a Python microservice running two NER models: Natasha for Russian (Cyrillic names, organisations, locations) and spaCy `en_core_web_sm` for English. It exposes a `/classify` endpoint and runs in under 100ms on CPU.

The **LLM classifier** is a local model running inside Ollama - by default `qwen3:4b-instruct-2507-q4_K_M` (~2.6 GB, 4-bit quantized). It handles things NER cannot reliably detect: API keys, passwords, tokens, and credentials of arbitrary format. Chain-of-thought thinking is suppressed via the `/no_think` control token so the model returns only the JSON array of sensitive strings. Typical latency is 5–20 seconds on CPU.

Both classifiers run concurrently under a shared 120-second budget. If either is slow or unavailable, it is skipped and the remaining results still apply. The proxy never blocks indefinitely.

Span validation ensures no partial matches: a detected span is only applied if the characters immediately surrounding it are word delimiters. This prevents false positives like matching `sd@example.com` inside `asd@example.com`.

Starting sanitization is a single command:

```bash
docker compose --profile sanitize up -d
```

If latency matters more than coverage, you can disable the LLM layer and rely only on NER - which still catches names, organisations, and locations with sub-100ms latency.

***

### Getting started in 3 steps

```bash
# 1. Clone
git clone https://github.com/gonkalabs/opengnk.git
cd opengnk

# 2. Configure
cp .env.example .env
# Add your GONKA_PRIVATE_KEY and GONKA_ADDRESS

# 3. Run
make run
```

The proxy is up at `http://localhost:8080`. Zero host dependencies - everything runs in Docker, no local Go installation needed.

***

### Under the hood

The project is written in Go and structured around a few focused internal packages:

- `internal/signer` - ECDSA secp256k1 signing of upstream requests
- `internal/upstream` - HTTP client, endpoint discovery, Transfer Agent whitelist filtering
- `internal/wallet` - multi-wallet pool with round-robin routing
- `internal/toolsim` - tool-call simulation (prompt injection + JSON parsing)
- `internal/sanitize` - redaction and restoration core, classifier interface, NER client, LLM classifier
- `internal/api` - HTTP handlers for all endpoints
- `internal/config` - environment variable loading

The entire codebase is open source under the MIT license. We believe in open source - the same philosophy that drives everything we build at Gonka Labs. Anyone can inspect it, run it locally, fork it, or contribute.

***

### Connection to proxy.gonka.gg

opengnk is the self-hosted version of [proxy.gonka.gg](https://proxy.gonka.gg), our cloud API for Gonka inference. If you want a managed endpoint with no setup, proxy.gonka.gg is there. If you want full control - your keys on your machine, your own rate limits, your own privacy guarantees - opengnk is the answer.

Both speak the same OpenAI-compatible protocol. Switching between them is a single `base_url` change.

***

### What's next

opengnk is already being used by developers building on Gonka - plugging it into agents (OpenClaw, etc), Cursor, local scripts, and custom applications. We will keep iterating based on what the community needs.

If there is a feature you want - additional endpoint support, new sanitization classifiers, better multi-model routing, anything - open an issue or tell us in the Telegram chat. We ship fast.

**GitHub:** [github.com/gonkalabs/opengnk](https://github.com/gonkalabs/opengnk)  
**Gonka Labs:** [gonkalabs.com](https://gonkalabs.com) | [gonka.gg](https://gonka.gg)

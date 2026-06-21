---
title: "#1027 — Gonka AI x n8n"
source: https://github.com/gonka-ai/gonka/discussions/1027
discussion_number: 1027
category: show-and-tell
synced_at: 2026-06-21T10:06:03Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1027](https://github.com/gonka-ai/gonka/discussions/1027) каждые 6 часов. 

# Gonka AI x n8n

**Автор:** [@Dankosik](https://github.com/Dankosik) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-04-07 12:53 UTC · **Обновлено:** 2026-04-07 12:53 UTC

---

## 📝 Описание

# GonkaGate x n8n

Hi everyone,

We've been working on an `n8n` package for GonkaGate, and it's finally public.

`@gonkagate/n8n-nodes-gonkagate` is an open source `n8n` community node package
for people who want to use GonkaGate in self-hosted `n8n` without piecing
together generic OpenAI-compatible nodes by hand.

## At a glance

| Item | Value |
| --- | --- |
| Package | `@gonkagate/n8n-nodes-gonkagate` |
| Root node | `GonkaGate` |
| AI model node | `GonkaGate Chat Model` |
| Credential | `GonkaGate API` |
| Best fit today | Self-hosted `n8n` |
| Repo | [github.com/GonkaGate/n8n-nodes-gonkagate](https://github.com/GonkaGate/n8n-nodes-gonkagate) |
| npm | [npmjs.com/package/@gonkagate/n8n-nodes-gonkagate](https://www.npmjs.com/package/@gonkagate/n8n-nodes-gonkagate) |

## Why this exists

The fallback OpenAI-compatible route works. We've used it too. It just makes
people do more translation work than they should before the first request.

If you want to use GonkaGate in `n8n`, you probably should not have to start
with base URLs, custom credential wiring, and a guess about which stock node is
the least painful in your current `n8n` version. We wanted a GonkaGate-first
path that feels shorter and clearer.

We also did not want to pretend the package does more than it does. It should
be clear about what GonkaGate supports today, while still leaving room to grow
later without renaming everything around one endpoint.

## What you get

- the root node `GonkaGate`
- the additive AI model node `GonkaGate Chat Model`
- the shared credential `GonkaGate API`

## Current API scope

> [!NOTE]
> The package currently targets the public GonkaGate base URL
> `https://api.gonkagate.com/v1`.
>
> Right now that means these endpoints:
>
> - `GET /v1/models`
> - `POST /v1/chat/completions`

In practice, the package can do the following today:

- install both `GonkaGate` and `GonkaGate Chat Model` from one package
- reuse one `GonkaGate API` credential across both
- run `List Models`
- run non-streaming root-node `Chat Completion`
- use `GonkaGate Chat Model` in `n8n` AI workflows
- load models from `GET /v1/models`
- fall back to manual `Model ID` entry if the live list is empty or unavailable

That last part was a deliberate choice. Live model discovery is nice when it
works, but manual `Model ID` still matters.

## Quick start

If you already run self-hosted `n8n`, the shortest install path is still the
Community Nodes UI:

```text
@gonkagate/n8n-nodes-gonkagate
```

Then:

1. Create `GonkaGate API`.
2. Add the root `GonkaGate` node.
3. Run `List Models`.
4. Switch to `Chat Completion` for the first real request.

## What we're not claiming

> [!IMPORTANT]
> A few things we are deliberately **not** claiming yet:

- blanket support across all `n8n` versions
- `n8n` Cloud availability
- verified-node eligibility
- `/v1/responses` support
- broad live validation for every AI-agent or tool-calling-heavy workflow shape

For the exact support posture, see the compatibility matrix and known
limitations.

## Demo

[![Install GonkaGate in n8n](https://raw.githubusercontent.com/GonkaGate/n8n-nodes-gonkagate/main/.github/assets/gonkagate-n8n-demo.gif)](https://raw.githubusercontent.com/GonkaGate/n8n-nodes-gonkagate/main/.github/assets/gonkagate-n8n-demo.mp4)

## Useful links

- [README](https://github.com/GonkaGate/n8n-nodes-gonkagate#readme)
- [Quickstart](https://github.com/GonkaGate/n8n-nodes-gonkagate/blob/main/docs/quickstart.md)
- [Installation Guide](https://github.com/GonkaGate/n8n-nodes-gonkagate/blob/main/docs/install.md)
- [Compatibility Matrix](https://github.com/GonkaGate/n8n-nodes-gonkagate/blob/main/docs/compatibility.md)
- [Known Limitations](https://github.com/GonkaGate/n8n-nodes-gonkagate/blob/main/docs/known-limitations.md)
- [Fallback OpenAI-Compatible Paths](https://github.com/GonkaGate/n8n-nodes-gonkagate/blob/main/docs/fallback-openai-paths.md)
- [Importable first-request workflow](https://github.com/GonkaGate/n8n-nodes-gonkagate/blob/main/examples/quickstart/gonkagate-first-request.workflow.json)
- [Self-hosted Docker example](https://github.com/GonkaGate/n8n-nodes-gonkagate/tree/main/examples/docker/self-hosted)
- [Issues and feedback](https://github.com/GonkaGate/n8n-nodes-gonkagate/issues)


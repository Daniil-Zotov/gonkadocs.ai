---
title: "#999 — Gonka AI x Claude Code"
source: https://github.com/gonka-ai/gonka/discussions/999
discussion_number: 999
category: show-and-tell
synced_at: 2026-06-17T20:31:20Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #999](https://github.com/gonka-ai/gonka/discussions/999) каждые 6 часов. 

# Gonka AI x Claude Code

**Автор:** [@Dankosik](https://github.com/Dankosik) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-04-02 11:29 UTC · **Обновлено:** 2026-04-02 11:30 UTC

---

## 📝 Описание

Hi everyone,

## What we built

We made `@gonkagate/claude-code`, a small open source installer for people who want to use Claude Code with Gonka through GonkaGate.

It solves a boring problem on purpose. Most people do not want to export env vars by hand, edit shell profiles, or create a `.env` file just to get Claude Code talking to a gateway.

So we kept the flow short. You run one command, enter a `gp-...` API key in a hidden prompt, choose a model, choose a scope, and then Claude Code is ready to use.

- Repo: https://github.com/GonkaGate/gonkagate-claude-code
- Website: https://gonkagate.com/en

## Why we built it

The gateway setup itself is not especially hard. The annoying part is first-time setup in Claude Code.

That is the part people still end up wiring by hand more often than they should. If someone already has a `gp-...` API key, getting to a normal `claude` workflow should not involve touching shell config.

## Quick start

```bash
npx @gonkagate/claude-code
```

## What the installer does

- Asks for a hidden `gp-...` API key
- Lets you choose a supported model from the curated list
- Writes Claude Code settings in `user` or `local` scope
- Leaves unrelated Claude Code settings alone
- Creates a backup before replacing an existing settings file
- Does not touch shell profiles or create `.env` files
- Helps keep local secret-bearing settings out of git during project-local setup

## Gateway host and transport

Under the hood, the installer points Claude Code at the GonkaGate gateway host:

`https://api.gonkagate.com`

For Claude Code, that means the Anthropic-compatible endpoint on that host.

The same GonkaGate host also serves OpenAI-compatible `/v1/*` routes for OpenAI-style clients, but this installer is specifically for Claude Code. It sets up the Claude-side Anthropic flow and leaves the OpenAI path alone.

## Models right now

We are keeping the public Claude Code model list small for now, but one detail is worth making explicit.

GonkaGate does not decide which models exist on Gonka Network. As an OpenAI-compatible provider and an Anthropic-compatible provider, we serve what is actually available in the network.

So the model list in this installer is not a custom catalog we fully control. It is a curated list of network-available models that we have patched into this Claude Code flow.

Right now there is one supported option: `qwen3-235b`.

As new models show up in Gonka Network, we will patch the utility and add them here.

## Demo

[![See the installer in action](https://raw.githubusercontent.com/GonkaGate/gonkagate-claude-code/main/.github/assets/gonkagate-claude-code-demo.gif)](https://raw.githubusercontent.com/GonkaGate/gonkagate-claude-code/main/.github/assets/gonkagate-claude-code-demo.mp4)

## More links

- npm package: https://www.npmjs.com/package/@gonkagate/claude-code
- README: https://github.com/GonkaGate/gonkagate-claude-code#readme
- Troubleshooting: https://github.com/GonkaGate/gonkagate-claude-code/blob/main/docs/troubleshooting.md
- Security notes: https://github.com/GonkaGate/gonkagate-claude-code/blob/main/docs/security.md
- How it works: https://github.com/GonkaGate/gonkagate-claude-code/blob/main/docs/how-it-works.md
- Changelog: https://github.com/GonkaGate/gonkagate-claude-code/blob/main/CHANGELOG.md
- Issues and feedback: https://github.com/GonkaGate/gonkagate-claude-code/issues

## Feedback

If you are using Gonka with local coding tools, the feedback we would care about most is:

- Which developer tools we should support next
- Where the onboarding still feels rough or confusing
- Which models you would actually want to use in this Claude Code flow as they appear on Gonka Network

If anything in the setup still feels awkward in practice, that is what we want to hear about. We will keep adjusting it based on what people actually run into.


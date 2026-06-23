---
title: "#1323 — Gonka x Hermes Agent"
source: https://github.com/gonka-ai/gonka/discussions/1323
discussion_number: 1323
category: show-and-tell
synced_at: 2026-06-23T15:25:15Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1323](https://github.com/gonka-ai/gonka/discussions/1323) каждые 6 часов. 

# Gonka x Hermes Agent

**Автор:** [@Dankosik](https://github.com/Dankosik) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-06-08 16:12 UTC · **Обновлено:** 2026-06-08 16:12 UTC

---

## 📝 Описание

# GonkaGate x Hermes Agent

Set up local `hermes-agent` to use GonkaGate:

```bash
npx @gonkagate/hermes-agent-setup
```

If you use Hermes Agent and have a GonkaGate API key, this should be a short
setup step, not a manual edit of `~/.hermes/config.yaml` and
`~/.hermes/.env`.

The utility configures Hermes through the supported `provider: custom` path,
stores the raw key in Hermes' `.env`, and only offers models that are live on
GonkaGate and launch-qualified for Hermes.

## Requirements

- `hermes-agent` installed
- Hermes Agent `v2026.5.16` / `v0.14.0` or newer
- Node.js `>=22.14.0`
- a GonkaGate API key
- an interactive terminal
- Linux, macOS, or WSL2

Public onboarding follows current GonkaGate Terms availability rules. It is
not intended for users or entities in the United States of America or U.S.
territories.

## Run

Default interactive setup:

```bash
npx @gonkagate/hermes-agent-setup
```

Specific Hermes profile:

```bash
npx @gonkagate/hermes-agent-setup --profile work
```

After setup:

```bash
hermes
```

Optional real-request smoke test:

```bash
hermes chat -Q --max-turns 1 -q "Do not use tools. Reply exactly: GonkaGate smoke test OK"
```

The utility prints that smoke test at the end, but does not run it
automatically. It sends one real model request.

## What it writes

The utility resolves the active Hermes config paths with Hermes itself. With
`--profile`, it uses the profile-specific paths.

It writes:

- `~/.hermes/config.yaml`
- `~/.hermes/.env`

The managed config shape is:

```yaml
model:
  provider: custom
  base_url: https://api.gonkagate.com/v1
  default: <selected-model>
  api_key: ${GONKAGATE_API_KEY}
```

The raw key is stored in `.env`:

```dotenv
GONKAGATE_API_KEY=gp-...
```

The raw key is not written to `config.yaml`. The utility also avoids taking
over unrelated `OPENAI_API_KEY` usage.

## What happens during setup

1. Check Node, terminal support, OS support, Hermes availability, and Hermes
   version.
2. Resolve the active `config.yaml` and `.env` paths.
3. Read existing `config.yaml`, `.env`, `auth.json`, and Hermes job state.
4. Stop on conflicts the utility should not overwrite.
5. Ask for the GonkaGate key through a hidden prompt.
6. Fetch `GET https://api.gonkagate.com/v1/models`.
7. Intersect the live catalog with checked-in Hermes qualification artifacts.
8. Let the user choose a qualified live model.
9. Show the planned file changes.
10. Back up files, write `config.yaml`, then write `.env`.
11. Roll back `config.yaml` if the `.env` write fails.

The utility does not accept a plain `--api-key` flag, so the key does not land
in shell history or process lists.

## Model selection

Models are not guessed from the live catalog alone. A model must be:

- present in GonkaGate `/v1/models`
- checked in as launch-qualified for Hermes Agent

Current allowlist:

- `moonshotai/kimi-k2.6` (recommended default)
- `minimaxai/minimax-m2.7`
- `qwen/qwen3-235b-a22b-instruct-2507-fp8`

Live-only models are ignored. Artifact-only models that are no longer live are
ignored too.

## What `/v1/models` proves

The setup request proves:

- the key authenticates
- GonkaGate returns a model catalog

It does not prove:

- billing balance
- quota
- first billable Hermes request readiness

Use the optional `hermes chat` smoke test when you want runtime proof.

## Current contract

- package: `@gonkagate/hermes-agent-setup`
- command: `npx @gonkagate/hermes-agent-setup`
- installed bin: `hermes-agent-setup`
- provider path: `provider: custom`
- base URL: `https://api.gonkagate.com/v1`
- managed config keys: `model.provider`, `model.base_url`, `model.default`,
  `model.api_key`
- managed secret key: `GONKAGATE_API_KEY`

## Non-goals

This is not a general Hermes installer. It does not:

- replace upstream `hermes setup`
- support Hermes versions older than `v2026.5.16` / `v0.14.0`
- accept arbitrary custom base URLs
- migrate legacy endpoint settings such as `OPENAI_BASE_URL`, `LLM_MODEL`,
  root-level `provider` / `base_url`, or legacy `custom_providers`
- edit shell profiles
- write directly to `auth.json` credential pools
- generate repository-local `.env` files
- claim native Windows launch support
- claim that `/v1/models` proves billing, quota, or first-request readiness

## Links

- [Repository](https://github.com/GonkaGate/hermes-agent-setup)
- [npm package](https://www.npmjs.com/package/@gonkagate/hermes-agent-setup)
- [Issues and feedback](https://github.com/GonkaGate/hermes-agent-setup/issues)
- [README](https://github.com/GonkaGate/hermes-agent-setup/blob/main/README.md)
- [How it works](https://github.com/GonkaGate/hermes-agent-setup/blob/main/docs/how-it-works.md)
- [Security notes](https://github.com/GonkaGate/hermes-agent-setup/blob/main/docs/security.md)
- [Launch qualification artifacts](https://github.com/GonkaGate/hermes-agent-setup/tree/main/docs/launch-qualification/hermes-agent-setup)
- [GonkaGate Hermes Agent guide](https://gonkagate.com/en/docs/guides/coding-agents/hermes-agent)
- [GonkaGate docs](https://gonkagate.com/en/docs)


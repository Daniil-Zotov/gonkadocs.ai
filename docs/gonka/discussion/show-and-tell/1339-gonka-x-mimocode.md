---
title: "#1339 — Gonka x MiMoCode"
source: https://github.com/gonka-ai/gonka/discussions/1339
discussion_number: 1339
category: show-and-tell
synced_at: 2026-06-28T14:17:02Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1339](https://github.com/gonka-ai/gonka/discussions/1339) каждые 6 часов. 

# Gonka x MiMoCode

**Автор:** [@Dankosik](https://github.com/Dankosik) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-06-12 00:29 UTC · **Обновлено:** 2026-06-12 00:29 UTC

---

## 📝 Описание

# GonkaGate x MiMoCode

```bash
npx @gonkagate/mimo-code-setup
```

Use this package when you already have `mimo` installed and want GonkaGate
configured as a MiMoCode custom provider without editing config files by hand.

After setup, keep using plain `mimo`.

## At a glance

| Item                      | Value                                            |
| ------------------------- | ------------------------------------------------ |
| Package                   | `@gonkagate/mimo-code-setup`                     |
| Command                   | `npx @gonkagate/mimo-code-setup`                 |
| Target CLI                | `mimo`                                           |
| Provider id               | `gonkagate`                                      |
| Base URL                  | `https://api.gonkagate.com/v1`                   |
| Model catalog             | `GET https://api.gonkagate.com/v1/models`        |
| Current transport         | `chat_completions`                               |
| Audited MiMoCode baseline | `@mimo-ai/cli` `0.1.0`, checked on June 11, 2026 |

## Quick start

Interactive setup:

```bash
npx @gonkagate/mimo-code-setup
```

Project scope with non-interactive defaults:

```bash
npx @gonkagate/mimo-code-setup --scope project --yes
```

Read the API key from stdin:

```bash
printf '%s' "$GONKAGATE_API_KEY" | npx @gonkagate/mimo-code-setup --api-key-stdin --scope project --yes --json
```

Pin the model explicitly:

```bash
npx @gonkagate/mimo-code-setup --model moonshotai/kimi-k2.6 --scope user
```

Then run:

```bash
mimo
```

## Requirements

| Requirement      | Value                                |
| ---------------- | ------------------------------------ |
| MiMoCode         | `mimo` on `PATH`                     |
| MiMoCode version | `@mimo-ai/cli` `0.1.0`               |
| Node.js          | `>=22.14.0`                          |
| API key          | GonkaGate `gp-...` key               |
| OS               | macOS, Linux, native Windows, or WSL |

The installer stops on MiMoCode versions older than `0.1.0`. It also blocks
newer MiMoCode versions until this setup package has been audited against that
upstream version.

## What the installer does

1. Reads a GonkaGate `gp-...` key from a hidden prompt, `GONKAGATE_API_KEY`, or
   stdin.
2. Fetches GonkaGate's live model catalog from `/v1/models`.
3. Writes the minimum MiMoCode config needed for `provider.gonkagate`.
4. Keeps the raw key outside the repository.
5. Verifies the config MiMoCode actually resolves before reporting success.

## Files and config

The installer uses MiMoCode's resolved paths. It does not assume a single global
config filename.

| Layer                  | Path                                                | What it contains                                                 | Commit-safe    |
| ---------------------- | --------------------------------------------------- | ---------------------------------------------------------------- | -------------- |
| Existing global config | `mimocode.jsonc`, `mimocode.json`, or `config.json` | `provider.gonkagate`; `model` and `small_model` for `user` scope | No, user-local |
| New global config      | `mimocode.jsonc`                                    | Created only when no global config exists                        | No, user-local |
| Project config         | `.mimocode/mimocode.json`                           | `model` and `small_model` for `project` scope                    | Yes            |
| Secret file            | `~/.gonkagate/mimo-code/api-key`                    | Raw GonkaGate API key                                            | No             |
| Install state          | `~/.gonkagate/mimo-code/install-state.json`         | Last durable setup metadata                                      | No             |
| Backups                | `~/.gonkagate/mimo-code/backups`                    | Managed-write rollback files                                     | No             |

For `project` scope, the repository-local config only selects the model:

```json
{
  "model": "gonkagate/moonshotai/kimi-k2.6",
  "small_model": "gonkagate/moonshotai/kimi-k2.6"
}
```

That file does not contain the raw API key or the path to the secret file.

## Scope behavior

| Scope     | User-level config                                            | Project config              |
| --------- | ------------------------------------------------------------ | --------------------------- |
| `user`    | Provider definition, API-key binding, `model`, `small_model` | Not written                 |
| `project` | Provider definition and API-key binding                      | `model`, `small_model` only |

The secret binding always stays in user-level config:

```text
provider.gonkagate.options.apiKey = {file:~/.gonkagate/mimo-code/api-key}
```

## Provider shape

The user-level provider entry includes the SDK package, base URL, file-backed
API-key reference, cache-key setting, and the model map generated from
`/v1/models`:

```jsonc
{
  "provider": {
    "gonkagate": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "GonkaGate",
      "options": {
        "baseURL": "https://api.gonkagate.com/v1",
        "apiKey": "{file:~/.gonkagate/mimo-code/api-key}",
        "setCacheKey": false,
      },
      "models": {
        "<model-id-from-/v1/models>": {
          "name": "<model-id-from-/v1/models>",
          "limit": {
            "context": 0,
            "output": 0,
          },
        },
      },
    },
  },
}
```

## Setup flow

| Step | Check or action                                                             |
| ---- | --------------------------------------------------------------------------- |
| 1    | Run `mimo --version`.                                                       |
| 2    | Resolve MiMoCode config paths.                                              |
| 3    | Read the GonkaGate key from a hidden prompt, `GONKAGATE_API_KEY`, or stdin. |
| 4    | Call `GET https://api.gonkagate.com/v1/models`.                             |
| 5    | Build `provider.gonkagate.models` from the catalog response.                |
| 6    | Ask for `user` or `project` scope.                                          |
| 7    | Write `~/.gonkagate/mimo-code/api-key`.                                     |
| 8    | Create backups, then write the managed config layers.                       |
| 9    | Verify the durable config that MiMoCode resolves.                           |
| 10   | Verify provider/model visibility with `mimo models gonkagate`.              |
| 11   | Check active override layers such as `MIMOCODE_CONFIG_CONTENT`.             |

Setup only succeeds when MiMoCode's resolved config matches the expected
GonkaGate provider, model, base URL, transport, and API-key binding.

The installer captures `mimo --pure debug config` internally, but it never
prints raw resolved config. That output can include substituted secret values.

## Model selection

The model picker is not hardcoded. It comes from the authenticated GonkaGate
catalog request:

```http
GET https://api.gonkagate.com/v1/models
Authorization: Bearer gp-...
```

Every returned model id becomes a key under `provider.gonkagate.models`.

Use the full GonkaGate slug in MiMoCode model refs. For Kimi:

```text
gonkagate/moonshotai/kimi-k2.6
```

Do not shorten it to:

```text
gonkagate/kimi-k2.6
```

MiMoCode treats the first path segment as the provider id and passes the rest
as the model id.

Current MiMoCode workflow validation exists for:

```text
moonshotai/kimi-k2.6
```

Other models can still appear in the picker when GonkaGate returns them.
Catalog availability and MiMoCode workflow validation are separate claims.

## What `/v1/models` proves

| Claim                                                      | Status     |
| ---------------------------------------------------------- | ---------- |
| The API key works for `GET /v1/models`                     | Proved     |
| GonkaGate returned a model list                            | Proved     |
| The installer can build the MiMoCode model map             | Proved     |
| Every returned model has full MiMoCode workflow validation | Not proved |
| Billing or quota is ready for the first chat request       | Not proved |
| `/v1/responses` is supported                               | Not proved |

Use `mimo` after setup to test the actual coding workflow.

## Failure behavior

The installer fails closed. It reports a blocker instead of leaving behind a
silent partial setup when:

| Blocker                                                     | Result                                  |
| ----------------------------------------------------------- | --------------------------------------- |
| `mimo` is missing                                           | Stop before writing config              |
| MiMoCode is older or newer than the audited baseline        | Stop before writing config              |
| The API key is missing or invalid                           | Stop before writing config              |
| `/v1/models` is unavailable                                 | Stop before writing config              |
| A managed write fails                                       | Roll back managed writes where possible |
| Effective MiMoCode config does not match the written config | Roll back managed writes                |
| Setup would put the secret binding in project config        | Block setup                             |
| Current shell overrides hide the durable config             | Report a current-session blocker        |

## Current contract

| Contract                  | Value                                                                       |
| ------------------------- | --------------------------------------------------------------------------- |
| Package                   | `@gonkagate/mimo-code-setup`                                                |
| Public command            | `npx @gonkagate/mimo-code-setup`                                            |
| Installed bin             | `mimo-code-setup`                                                           |
| Legacy bin                | `gonkagate-mimo-code`                                                       |
| Target CLI                | `mimo`                                                                      |
| Target upstream package   | `@mimo-ai/cli`                                                              |
| Audited MiMoCode baseline | `0.1.0`, checked on June 11, 2026                                           |
| Provider id               | `gonkagate`                                                                 |
| Provider package          | `@ai-sdk/openai-compatible`                                                 |
| Transport target          | `chat_completions`                                                          |
| Base URL                  | `https://api.gonkagate.com/v1`                                              |
| Model catalog             | `GET https://api.gonkagate.com/v1/models`                                   |
| Managed secret binding    | `provider.gonkagate.options.apiKey = {file:~/.gonkagate/mimo-code/api-key}` |
| Managed cache-key setting | `provider.gonkagate.options.setCacheKey = false`                            |

## Non-goals

This package does not:

- install MiMoCode itself
- configure non-GonkaGate providers
- accept arbitrary custom base URLs
- accept arbitrary custom model ids outside the authenticated GonkaGate catalog
- accept a plain `--api-key` flag
- mutate shell profiles
- generate `.env` files
- store secrets in repository-local files
- write directly to MiMoCode `auth.json` in v1
- claim `/v1/responses` support before an explicit migration
- claim every live catalog model has full MiMoCode workflow validation

## Links

| Resource         | Link                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------- |
| Repository       | [GonkaGate/mimo-code-setup](https://github.com/GonkaGate/mimo-code-setup)                |
| npm package      | [`@gonkagate/mimo-code-setup`](https://www.npmjs.com/package/@gonkagate/mimo-code-setup) |
| README           | [README](../README.md)                                                                   |
| How it works     | [docs/how-it-works.md](how-it-works.md)                                                  |
| Security notes   | [docs/security.md](security.md)                                                          |
| Model validation | [docs/model-validation.md](model-validation.md)                                          |
| Troubleshooting  | [docs/troubleshooting.md](troubleshooting.md)                                            |
| GonkaGate docs   | [gonkagate.com/en/docs](https://gonkagate.com/en/docs)                                   |


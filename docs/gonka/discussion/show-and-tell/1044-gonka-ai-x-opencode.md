---
title: "#1044 — Gonka AI x OpenCode"
source: https://github.com/gonka-ai/gonka/discussions/1044
discussion_number: 1044
category: show-and-tell
synced_at: 2026-06-20T19:57:25Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1044](https://github.com/gonka-ai/gonka/discussions/1044) каждые 6 часов. 

# Gonka AI x OpenCode

**Автор:** [@Dankosik](https://github.com/Dankosik) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-04-13 09:51 UTC · **Обновлено:** 2026-04-13 09:51 UTC

---

## 📝 Описание

<!-- Suggested GitHub Discussion title: Gonka AI x OpenCode -->

# Gonka AI x OpenCode

Hi everyone,

We just published a small OpenCode setup utility for GonkaGate.

`@gonkagate/opencode-setup` is an open source onboarding CLI for people who
already use `opencode` and want to point it at GonkaGate without making setup a
side quest. No hand-editing `opencode.json`, no shell profile secret exports,
and no need to learn the OpenCode custom-provider config shape before the first
request.

## What we built

We built a local installer around:

```bash
npx @gonkagate/opencode-setup
```

It handles the config plumbing around provider setup, secret binding, scope
selection, and effective-config verification, then gets out of the way so you
can keep using plain `opencode`.

## Why we built it

This is one of those pieces of plumbing that should be boring, but often is not.
If you already have a GonkaGate key, the next step should not be "open three
docs tabs and figure out where OpenCode wants provider config today."

The riskier parts are also the least fun: putting the secret in the wrong place,
leaving a repo-local `opencode.json` in a weird state, or thinking setup worked
because a file changed even though OpenCode resolves a different config at
runtime. We wanted the setup path to be short, explicit, and careful about what
it claims.

## Quick start

### Interactive

```bash
npx @gonkagate/opencode-setup
```

### Non-interactive with `GONKAGATE_API_KEY`

```bash
GONKAGATE_API_KEY=gp-... npx @gonkagate/opencode-setup --scope project --yes
```

### Non-interactive with stdin

```bash
printf '%s' "$GONKAGATE_API_KEY" | npx @gonkagate/opencode-setup --api-key-stdin --scope project --yes
```

After setup:

```bash
opencode
```

## What the installer does

1. Checks that local `opencode` is available and supported.
2. Shows the public curated model picker in interactive mode.
3. Asks for `user` or `project` scope.
4. Accepts the GonkaGate key through a hidden prompt, `GONKAGATE_API_KEY`, or
   `--api-key-stdin`.
5. Rejects plain `--api-key`.
6. Keeps the secret out of repository-local files.
7. Writes the user-level GonkaGate provider definition and secret binding.
8. When `project` scope is selected, writes only activation settings to
   repo-local `opencode.json`.
9. Preserves unrelated OpenCode settings where it can.
10. Creates rollback backups before replacing managed files.
11. Verifies the durable plain-`opencode` config and the current session's
    effective OpenCode config before reporting success.

## Gateway, OpenCode config, and transport

| Field                     | Current value                  |
| ------------------------- | ------------------------------ |
| Provider id               | `gonkagate`                    |
| Base URL                  | `https://api.gonkagate.com/v1` |
| OpenCode transport target | `chat/completions`             |

The `project` scope is intentionally conservative. The repo-local
`opencode.json` only gets activation settings. The provider definition and
secret binding stay in user scope, so the project file remains commit-safe by
default.

The installer does not write directly to `auth.json`, does not create `.env`
files, and does not mutate shell profiles.

## Models right now

The public picker is deliberately small right now. It has one validated option:

| Status                   | Model                                    |
| ------------------------ | ---------------------------------------- |
| Current validated option | `qwen/qwen3-235b-a22b-instruct-2507-fp8` |

We are treating this as a curated list, not a free-form custom model box. More
options can be added as they pass the same OpenCode validation path.

## What we're not claiming

The boundaries are explicit:

- no `/v1/responses` support today
- no arbitrary custom base URL override in v1
- no arbitrary custom model id support in v1
- no plain `--api-key`
- no shell profile edits
- no `.env` generation
- no direct writes to `auth.json`
- no live GonkaGate session verification yet
- no perfect explanation for every possible higher-precedence OpenCode config
  layer, although locally inspectable blockers are surfaced where possible

If `/v1/responses` support lands later, it should be a migration on this
integration, not a rename or a pretend-it-already-works claim.

## Useful links

- [Repository](https://github.com/GonkaGate/opencode-setup)
- [npm package](https://www.npmjs.com/package/@gonkagate/opencode-setup)
- [README](https://github.com/GonkaGate/opencode-setup#readme)
- [How it works](https://github.com/GonkaGate/opencode-setup/blob/main/docs/how-it-works.md)
- [Security notes](https://github.com/GonkaGate/opencode-setup/blob/main/docs/security.md)
- [Troubleshooting](https://github.com/GonkaGate/opencode-setup/blob/main/docs/troubleshooting.md)
- [Model validation](https://github.com/GonkaGate/opencode-setup/blob/main/docs/model-validation.md)
- [Changelog](https://github.com/GonkaGate/opencode-setup/blob/main/CHANGELOG.md)
- [Issues and feedback](https://github.com/GonkaGate/opencode-setup/issues)
- [GonkaGate](https://gonkagate.com/en)
- [Get a GonkaGate API key](https://gonkagate.com/en/register)
- [GonkaGate quickstart](https://gonkagate.com/en/docs/quickstart)
- [OpenCode](https://opencode.ai)

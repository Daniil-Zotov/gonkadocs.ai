---
title: "#1095 — Gonka AI x Kilo"
source: https://github.com/gonka-ai/gonka/discussions/1095
discussion_number: 1095
category: show-and-tell
synced_at: 2026-06-17T05:17:39Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1095](https://github.com/gonka-ai/gonka/discussions/1095) каждые 6 часов. 

# Gonka AI x Kilo

**Автор:** [@Dankosik](https://github.com/Dankosik) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-04-21 13:20 UTC · **Обновлено:** 2026-04-21 13:21 UTC

---

## 📝 Описание

# GonkaGate x Kilo

Hi everyone,

We put together a small setup utility for Kilo:

```bash
npx @gonkagate/kilo-setup
```

The goal is simple. If you already use `kilo` and already have a GonkaGate
API key, setup should take a minute or two. It should not turn into "open
three docs tabs, figure out where Kilo wants provider config, then hope you
didn't leave a secret in the repo by accident."

That is what `@gonkagate/kilo-setup` is for.

> Short version: this is a small CLI that wires local `kilo` to GonkaGate,
> keeps the secret out of repo-local config, and verifies the resolved result
> before sending you back to plain `kilo`.

## Why we made it

Manual provider setup is manageable once. It gets old fast after that.

The annoying part is not the API itself. The annoying part is everything around
it: where the secret should live, which config layer should own what, whether
project config is safe to commit, and whether Kilo is actually using the
config you just wrote instead of something else from the current shell.

We wanted a short path that does the boring work correctly and stays honest
about its limits.

## The short version

### Interactive

```bash
npx @gonkagate/kilo-setup
```

### Non-interactive

With `GONKAGATE_API_KEY`:

```bash
GONKAGATE_API_KEY="$GONKAGATE_API_KEY" npx @gonkagate/kilo-setup --scope project --yes
```

With stdin:

```bash
printf '%s' "$GONKAGATE_API_KEY" | npx @gonkagate/kilo-setup --api-key-stdin --scope project --yes
```

With project-scope cache cleanup:

```bash
printf '%s' "$GONKAGATE_API_KEY" | npx @gonkagate/kilo-setup --api-key-stdin --scope project --clear-kilo-model-cache --yes
```

### After setup

Go back to plain `kilo`.

```bash
kilo
```

## What the installer actually does

At a high level, it does four things:

1. Figures out the local Kilo situation.
2. Writes the minimum safe config.
3. Keeps the secret in user scope, not in the repository.
4. Verifies the resolved result instead of trusting file writes.

More concretely:

- it detects `kilo`, or falls back to `kilocode`
- it supports the exact investigated Kilo profile: `@kilocode/cli@7.2.0`
- it accepts the API key through a hidden prompt, `GONKAGATE_API_KEY`, or
  `--api-key-stdin`
- it rejects plain `--api-key`
- it stores the managed secret at `~/.gonkagate/kilo/api-key`
- it writes the user-level `provider.gonkagate` definition and canonical
  `{file:~/.gonkagate/kilo/api-key}` binding
- it chooses the recommended scope automatically
- inside a git repo, that usually means `project`
- outside a repo, that usually means `user`
- on reruns, it only asks about scope when the previous installer-managed scope
  no longer matches the new recommendation
- in `project` scope, it writes only activation settings into
  `.kilo/kilo.jsonc`
- it creates rollback backups before replacing installer-managed files
- it preserves unrelated Kilo config where it can
- it verifies the durable plain-`kilo` result with the local resolver
- if the current shell is still affected by `KILO_CONFIG`,
  `KILO_CONFIG_DIR`, or `KILO_CONFIG_CONTENT`, it reports that separately
- for project installs, it can also clear Kilo's current global UI-model cache

That last part matters more than it sounds. A config write is easy. A correct
resolved config is the part that actually counts.

## A couple of details that mattered to us

`project` scope is intentionally narrow. The repository gets activation only.
The provider definition and secret binding stay in user config. That keeps
`.kilo/kilo.jsonc` commit-safe by default and avoids the usual "why is there a
secret-related path in git" problem.

We also did not want a setup command that happily prints or spreads the secret
around. The installer does not write to `auth.json`, does not generate `.env`
files, and does not touch shell profiles.

The other important part is verification. The runtime treats effective Kilo
config as the real success gate. If the durable install is fine but the current
shell is still overridden by runtime-only Kilo env vars, the tool says so
instead of pretending everything is clean.

## Current model and transport

Right now the public default is deliberately small:

- package: `@gonkagate/kilo-setup`
- provider id: `gonkagate`
- base URL: `https://api.gonkagate.com/v1`
- transport: `chat/completions`
- validated Kilo profile: exact `@kilocode/cli@7.2.0`
- current validated model: `qwen/qwen3-235b-a22b-instruct-2507-fp8`
- managed limits: `limit.context = 262144`, `limit.output = 8192`

We are treating model support as a curated list, not as a vague "it probably
works" promise.

## What we are not claiming

The current boundaries are deliberate:

- no support claim beyond exact `@kilocode/cli@7.2.0`
- no `/v1/responses` support today
- no plain `--api-key`
- no `.env` generation
- no shell profile edits
- no direct writes to `auth.json`
- no production-ready native Windows claim yet
- no claim that project config alone is enough on a brand-new machine
- no claim that live real-path `kilo debug config` against user paths is the
  production default verifier

If `/v1/responses` support shows up later, that should be a real migration, not
something implied by marketing copy.

## Links

### Project

- [Repository](https://github.com/GonkaGate/kilo-setup)
- [npm package](https://www.npmjs.com/package/@gonkagate/kilo-setup)
- [Issues and feedback](https://github.com/GonkaGate/kilo-setup/issues)
- [Changelog](https://github.com/GonkaGate/kilo-setup/blob/main/CHANGELOG.md)
- [GonkaGate website](https://gonkagate.com/en)
- [Get a GonkaGate API key](https://gonkagate.com/en/register)
- [GonkaGate docs](https://gonkagate.com/en/docs)

### Docs

- [README](https://github.com/GonkaGate/kilo-setup/blob/main/README.md)
- [User guide](https://github.com/GonkaGate/kilo-setup/blob/main/docs/user-guide.md)
- [How it works](https://github.com/GonkaGate/kilo-setup/blob/main/docs/how-it-works.md)
- [Security notes](https://github.com/GonkaGate/kilo-setup/blob/main/docs/security.md)
- [Troubleshooting](https://github.com/GonkaGate/kilo-setup/blob/main/docs/troubleshooting.md)


---
title: "#1116 — HOW-TO: Create and Submit a Governance Proposal on Gonka"
source: https://github.com/gonka-ai/gonka/discussions/1116
discussion_number: 1116
category: show-and-tell
synced_at: 2026-06-26T04:40:57Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1116](https://github.com/gonka-ai/gonka/discussions/1116) каждые 6 часов. 

# HOW-TO: Create and Submit a Governance Proposal on Gonka

**Автор:** [@paranjko](https://github.com/paranjko) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-04-24 13:23 UTC · **Обновлено:** 2026-04-24 13:23 UTC

---

## 📝 Описание

Over the past few weeks, I’ve spent quite a bit of time helping people with governance proposals, so I put together a guide that may be useful if you’re preparing one yourself.

It has already been used for several successful proposals, so the process is tested in practice.

**Note:** this guide covers the technical part of creating and submitting a proposal. For a proposal to pass, you also need to communicate it clearly and build support around it. 

Consider publishing the full proposal description on GitHub, sharing it with the community, and discussing it with participants on Discord and other relevant channels before and during the voting period.

# How to Create and Submit a Governance Proposal on Gonka

Step-by-step for submitting and voting with `inferenced`. Aligned with [Gonka — Transactions & Governance](https://gonka.ai/transactions-and-governance/). Replace every **placeholder** with your own values before running commands.

---

## 1. Placeholders and shell exports

| Placeholder | Meaning |
|-------------|---------|
| `<KEY_NAME>` | Your key name in the keyring (not your `gonka1…` address) |
| `<PATH_TO_PROPOSAL_JSON>` | Path to the proposal JSON file, e.g. `./proposal.json` |
| `<PUBLIC_RPC>` | RPC URL **including** `/chain-rpc/`, e.g. `http://node1.gonka.ai:8000/chain-rpc/` |
| `<PUBLIC_HTTP_API>` | Same host **without** `/chain-rpc/`, e.g. `http://node1.gonka.ai:8000` |
| `<CHAIN_ID>` | e.g. `gonka-mainnet` for mainnet |

Run once per terminal session (edit the right-hand sides):

```bash
export GONKA_RPC="<PUBLIC_RPC>"
export GONKA_API="<PUBLIC_HTTP_API>"
export CHAIN_ID="<CHAIN_ID>"
export ACCOUNT_NAME="<KEY_NAME>"
```

All later commands assume these variables are set. If a command fails with “connection” or “parse”, check that `GONKA_RPC` ends with exactly one `/chain-rpc/`.

---

## 2. Two URLs (do not mix them)

| Task | Variable |
|------|----------|
| **`inferenced query`** / **`tx`** | `$GONKA_RPC` (must include **`/chain-rpc/`**) |
| **`create-client`** (HTTP `…/v1/participants` on the seed) | `$GONKA_API` (**no** `/chain-rpc/`) |

Using `$GONKA_RPC` for `--node-address` in `create-client` is incorrect and will fail or hit the wrong service.

---

## 3. Prerequisites

### 3.1 Install CLI

Download a build for your OS from [Gonka releases](https://github.com/gonka-ai/gonka/releases), unpack, then:

```bash
chmod +x inferenced
./inferenced --help
```

On macOS, if Gatekeeper blocks the binary: **System Settings → Privacy & Security → Open Anyway**.

### 3.2 Read `min_deposit` and `voting_period` from the chain

Do not rely on a fixed ngonka amount from old docs—query the live values:

```bash
./inferenced query gov params \
  --node "$GONKA_RPC" \
  --chain-id "$CHAIN_ID" \
  -o json | jq '{min_deposit: .params.min_deposit, voting_period: .params.voting_period}'
```

Your proposal JSON’s `deposit` must satisfy **`min_deposit`** (same denom, amount ≥ minimum).

### 3.3 Proposal JSON

Prepare a gov v1 JSON (`messages`, `metadata`, `deposit`, `title`, `summary`).

There are two main parts to prepare:

1. **Proposal description fields**

   Keep the on-chain text short and clear.

   Make sure the proposal includes:

   - a short summary of what the proposal is about;
   - a link to the full proposal description with all details;
   - the wallet address where the funds should be sent, if the proposal requests funding;
   - the requested amount and denom, if the proposal requests funding.

2. **Proposal JSON structure**

   For the JSON structure, the best approach is to look at previous proposals and use them as references.

   You can inspect previous [proposal JSONs here](http://node1.gonka.ai:8000/dashboard/gonka/gov) to see how different proposal types are structured.

   In many cases, it is easier to start from a similar previous proposal and adapt it to your own proposal.

For messages such as **`MsgUpdateParams`**, the chain expects the **full** params object and correct **`authority`** (gov module address). Fetch the gov module address:

```bash
./inferenced query auth module-accounts \
  --node "$GONKA_RPC" \
  --chain-id "$CHAIN_ID" \
  -o json | jq -r '.accounts[] | select(.value.name=="gov") | .value.address'
```

Use that address as `authority` where the message type requires it.

If the `jq` line prints nothing, run the same `query` **without** `jq` once and locate the `gov` module entry manually. The output shape can differ slightly by SDK version.

### 3.4 Optional: new key + register participant (`create-client`)

This creates a key and calls the seed HTTP API (participant registration). Use **`$GONKA_API` only**:

```bash
./inferenced create-client "$ACCOUNT_NAME" \
  --node-address "$GONKA_API"
```

Store the **mnemonic** safely. If you already have a funded key for governance, skip this and avoid double registration.

Use the **same** `--keyring-backend` everywhere (e.g. `file`) for `keys show`, `tx gov submit-proposal`, and `tx gov vote`.

---

## 4. Publish the proposal on-chain

### 4.1 Check balance

```bash
./inferenced query bank balances \
  "$(./inferenced keys show "$ACCOUNT_NAME" -a --keyring-backend file)" \
  --node "$GONKA_RPC" \
  --chain-id "$CHAIN_ID"
```

Ensure you have enough **`ngonka`** (or the fee denom your node expects) for **`min_deposit`** and fees.

### 4.2 Submit

Recommended pattern from the official Gonka doc:

```bash
./inferenced tx gov submit-proposal "<PATH_TO_PROPOSAL_JSON>" \
  --from "$ACCOUNT_NAME" \
  --keyring-backend file \
  --chain-id "$CHAIN_ID" \
  --node "$GONKA_RPC" \
  --unordered --timeout-duration=60s \
  --gas 2000000 --gas-adjustment 5.0 \
  --yes
```

After submission, note the proposal number from the output or [find it here](http://node1.gonka.ai:8000/dashboard/gonka/gov).

Share the proposal number so the community announcement can go out.

---

## 5. Vote (after voting has started)

### 5.1 Read the proposal on-chain

```bash
./inferenced query gov proposal "$PROPOSAL_ID" \
  --node "$GONKA_RPC" \
  --chain-id "$CHAIN_ID" \
  -o json
```

Confirm `status`, `title`, `summary`, `messages`, and voting times before voting.

### 5.2 Optional: tally so far

```bash
./inferenced query gov tally "$PROPOSAL_ID" \
  --node "$GONKA_RPC" \
  --chain-id "$CHAIN_ID" \
  -o json
```

Use `$GONKA_RPC` as-is—do **not** append `/chain-rpc/` again.

### 5.3 Cast a vote

Replace `yes` with `no`, `abstain`, or `no_with_veto` if you intend to vote that way:

```bash
./inferenced tx gov vote "$PROPOSAL_ID" yes \
  --from "$ACCOUNT_NAME" \
  --keyring-backend file \
  --chain-id "$CHAIN_ID" \
  --node "$GONKA_RPC" \
  --unordered --timeout-duration=60s \
  --gas 2000000 --gas-adjustment 5.0 \
  --yes
```

You may **change** your vote by sending another `vote` before the voting period ends.

---

That’s it! Good luck with your proposal!

If you have comments, suggestions, or anything to add from your own experience, feel free to share them. We can keep improving the guide together. And if any part feels unclear, let me know as well.

---
title: "#1243 — Project funding governance and management"
source: https://github.com/gonka-ai/gonka/discussions/1243
discussion_number: 1243
category: proposals
synced_at: 2026-06-24T15:13:31Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1243](https://github.com/gonka-ai/gonka/discussions/1243) каждые 6 часов. 

# Project funding governance and management

**Автор:** [@a-kuprin](https://github.com/a-kuprin) · **Категория:** :bulb: Proposals · **Создано:** 2026-05-25 04:19 UTC · **Обновлено:** 2026-05-25 04:19 UTC

---

## 📝 Описание

# Project funding governance

## Summary

At present, there is a need for an organization to allocate funds from the community pool and for adequate project-funding tools.

We propose a smart contract to govern project funding. The grantee first prepares a project with milestones, each tied to a USDT/GNK payout (both can be used at once).
The community votes on the whole project; funds are moved into the smart contract; and an industry committee appointed by hosts votes on each milestone being met (or not met). Industry committees are shared across all grants, but the community can assign committees to specific milestones.

## Background

In discussions, two views have clashed: one that “helicopter money” should be handed out, and another that **funds can run out and then hosts lose everything**, together with the death of the project. As a result, most proposals are rejected and the existing budget is not invested. Host concerns are nevertheless justified.

There is even a view that the Core team lacks developers and should hire more. Yet the community has a budget and every host has no less say in governance—but the community has not fully realized that. **Gonka has an ideology, and it is about decentralization—the Core team must not be the center everything depends on.** Shifting responsibility for project development onto the Core team is somewhat immature behavior. Creating a roadmap and moving toward a Foundation are signs of a mature community that can steer its own development. Miners are serious people with capital and business experience who hold project equity (via GNK) and, in practice, form a board of directors that is no less—and perhaps more—responsible than the Core team. After all, miners invested money and hardware.

## Problem

Under the current proposal-funding model, rejecting everything is a very rational tactic for hosts. If money is paid upfront, there is a huge risk that nothing will be done, or done poorly, or not what was needed. Hosts bear that risk. If payout is in GNK, tokens will hit the market and pressure the order book, crushing host profitability that is already at or past the edge.

If a project is funded on a post-payment basis, the grantee risks receiving nothing while still spending resources and money.

Splitting into milestones requires manual organization and host attention to the project—effectively micromanagement by the board of directors.

## Solution

The grantee first prepares a project with milestones, each tied to a payout. USDT is directed at operating expenses; GNK (as project equity) rewards contribution to Gonka’s development and can be unlocked after 1 or 2 years (timing is configurable). More than stream vesting—where GNK unlock daily and can reach the market—is possible: any unlock schedule.

Hosts, as the board of directors, vote on the project itself and appoint a committee responsible for acceptance. Payout can happen in one lump sum up front, but each milestone must be voted on by the committee to confirm whether the grantee fulfilled or failed obligations.

For example, a project might allocate 10k USDT immediately, another 10k on passing a milestone, and 50k with a 2-year vest on completion.

## Design

Implemented as a CosmWasm contract **`grant-board`** in `inference-chain/contracts/` (along the lines of `community-sale` and `liquidity-pool`), plus an optional helper contract **`vesting-proxy`** for block-height GNK locks. On instantiate, the contract admin is the gov module so upgrades and parameters go only through host votes.

### Architecture and integration

- **Funding sources:** GNK—from `x/distribution` (community pool) via `MsgCommunityPoolSpend`; USDT—from the `community-sale` contract via `withdraw_ibc`. Grant-board accepts both assets at its address.
- **Governance:** all privileged actions (funding, stop, committee changes, config) come only from `gov_authority`—i.e. they require a host vote via `x/gov`.
- **Accounting:** the contract holds `tracked_balance[denom]` and per grant `allocated_*` / `spent_*`. Invariant: the contract’s bank balance per denom ≥ sum of reserved funds for active and underfunded grants plus pending refunds. This prevents one grant from spending another’s funds.
- **Anti-donation:** any funds sent to the contract address outside the formal flow stay outside `tracked_balance` and are not attributed to grants.

### Grant lifecycle

Grant states: `Draft` → `Underfunded` / `Active` → `Stopped` / `StoppedRefunded` / `Completed`.

Milestone states: `Pending`, `ExtensionVotePending`, `InReview`, `RetryVotePending`, `StopVotePending`, `Released`, `Rejected`, `Skipped`.

Flow: grantee creates draft → hosts fund via gov → auto-milestone (if any) pays immediately → for other milestones grantee submits evidence → committee votes → payout.

### 1. Grant draft (grantee)

- `CreateDraft`—anyone can create a draft by attaching a **setup fee in GNK**. The fee is sent to the community pool via `MsgFundCommunityPool` (anti-spam, non-refundable).
- Each fee payment grants a pool of **10 credits** for `UpdateDraft`. When credits are exhausted, the next update attaches the fee again (10 credits, minus 1 for the current call = 9 left).
- Minimum fee—`min_setup_fee_ngonka` (hard floor 10 GNK). While `setup_fee < min`, the contract is considered inactive.
- The grantee publishes the project text on GitHub (commit-pinned URL) and puts `proposal_url` + `proposal_hash` (sha256 of the markdown) in the draft. This binds the on-chain draft to the off-chain description.
- Each gated milestone’s description lives in a **GitHub Discussion** (`description_discussion_url`)—for v1 this avoids state bloat. v2 will add Arweave for immutable storage.
- `CloseDraft`—close the draft without refunding the fee. Hosts can close a draft via `StopGrant`.

**Draft validation:**

- Milestone amounts sum to `requested_ngonka` / `requested_usdt` (computed by the contract).
- One optional **auto-milestone with `index == 0`** at the start of the list is allowed; gated milestones run sequentially `1, 2, 3, …`.
- `usdt_denom`—exact IBC voucher denom, immutable for the grant’s lifetime.
- A committee may be unset at draft time—gov assigns later via `SetGrantCommittee` / `SetMilestoneCommittee`.

### 2. Funding (Phase 1—host vote)

Hosts vote on a single gov proposal with three messages in strict order:

1. `MsgCommunityPoolSpend`—GNK from the community pool to the `grant-board` address.
2. `MsgExecuteContract` to `community-sale` with `withdraw_ibc`—USDT to the `grant-board` address.
3. `MsgExecuteContract` to `grant-board` with **`MarkFunded { grant_id, ngonka, usdt, config_hash }`**—must be last.

`MarkFunded` behavior:

- Requires `info.sender == gov_authority` and `grant.status == Draft`.
- Checks `payload.config_hash` against current `config.config_hash`. If hosts passed `UpdateConfig` in the same window, `MarkFunded` reverts and the entire funding transaction rolls back. This ensures hosts vote for exactly the template that will execute.
- Computes `delta_ngonka` / `delta_usdt` as the **increase** in contract balance relative to `tracked_balance` (protection against attributing stray transfers).
- If `delta == requested` → grant `Active`, `funded_at` is set. If `delta > requested` → surplus is returned in the same tx (GNK → community pool, USDT → community-sale). If `delta < requested` → grant `Underfunded`, remediated via gov.

The **funding proposal template** is returned by query `FundingProposalTemplate { grant_id }`—always recomputed from current config and returns `config_hash` to embed in `MarkFunded`. CLI tool `grantctl funding-proposal` writes ready JSON.

### 3. Auto-milestone (`index 0`)—instant payout

- Optional milestone with `index == 0` (at most one, always first) pays **inside `MarkFunded` immediately**, with no committee and no evidence.
- Used for:
  - **Proxy grant**—one auto-milestone for 100% of the amount; mirrors today’s `MsgCommunityPoolSpend` flow but with grant-board accounting and a unified event stream.
  - **Upfront tranche**—e.g. `index 0` = 20% GNK on fund, `index 1..N` = 80% via milestones.
- Auto-milestone pays **only** when the grant becomes `Active`. For `Underfunded` it stays `Pending` until fully funded.

### 4. Milestone acceptance (Phase 2—committee)

For each gated milestone (`index ≥ 1`):

1. Grantee calls **`SubmitMilestoneEvidence { evidence_uri, evidence_hash }`**. Milestone → `InReview`, timer `review_deadline = now + review_period_seconds`.
2. Contract captures a **committee snapshot** (`VOTE_SNAPSHOTS`)—member list and threshold at vote open.
3. Committee members call **`VoteOnMilestone { yes }`**.
4. Anyone can call **`ExecuteMilestoneRelease`** when:
   - threshold `yes_required = ⌈threshold_num × n / threshold_den⌉` is met, **or**
   - `review_deadline` has passed and outcome is `Undecided` (auto-release).
5. Payout: USDT—always immediate; GNK—immediate if `vesting_blocks == 0`, else via `vesting-proxy` with unlock at `current_height + vesting_blocks`. **Locked GNK is not refundable on `StopGrant`.**

**Rejection cascade** (when the committee votes no). Next status depends on time relative to `evidence_due_at`:

- Plenty of time before due → `Rejected`, grantee may resubmit.
- Tight window before due → `RetryVotePending` (committee votes whether to allow another attempt).
- Already past due → `StopVotePending` (committee votes whether to stop the grant).

**Committee snapshot (Step 7e).** A vote is accepted only if `voter ∈ snapshot.members ∩ current_committee.members`. Thresholds (`yes_required`, `blocking_no`) use snapshot size, not the current committee. This closes vote-erase / vote-overweight / vote-stuffing attacks via mid-vote `UpsertCommittee`.

**Self-deal protection.** If the voter is `grant.grantee`, the vote is dropped silently with event `committee_vote_dropped_self_deal`.

**Empty committee is a feature.** If no committee resolves for a milestone—auto-release at `review_deadline`. Hosts may deliberately rely on the timer.

**Milestone order.** Strictly sequential: milestone `k` cannot be submitted until all milestones `< k` are terminal (`Released` / `Skipped`). Parallel review is not supported in v1.

### 5. Timers and parameters (all in `Config`, gov-only)

| Parameter | Default | Min | Max | Purpose |
|-----------|---------|-----|-----|---------|
| `milestone_evidence_due_spacing_seconds` | 30 days | 1 day | 365 days | `evidence_due_at = funded_at + spacing × index` |
| `post_deadline_grace_seconds` | 7 days | 1 day | 14 days | Window after due for submit/extension before stop |
| `extension_vote_period_seconds` | 7 days | 1 day | 14 days | Committee vote window on extension |
| `max_deadline_extension_seconds` | 30 days | 1 day | 182 days | Maximum of one approved extension |
| `review_period_seconds` | 30 days | **14 days** | 30 days | Review vote window after evidence |

All parameters are **contract-wide**; the grantee does not set them. They are included in `config_hash`, which binds the funding proposal to the active config.

**Delivery flow:**

- `RequestMilestoneExtension { proposed_evidence_due_at }`—grantee may ask to extend the deadline; committee votes via `VoteOnMilestoneExtension`. Approve → new `evidence_due_at` within `max_deadline_extension`. Reject or Undecided → grant stops, GNK returns to the community pool.
- `ProcessDeliveryTimeouts`—crank (grantee-only), runs `StopGrant` if `due + grace` passed with no evidence and no active extension vote. **No auto-release without evidence**—only stop with refund.
- `ProcessMilestoneTimeouts`—crank to auto-release milestones in `InReview` with `Undecided` outcome after `review_deadline`.

### 6. Optional vesting (`vesting-proxy`)

- Minimal contract with block-height locks. Each Lock stores `recipient`, `denom`, `amount`, `unlock_height`, `grant_id`, `milestone_index`.
- `Vest`—only `grant-board` may call. `Claim`—anyone after `unlock_height`. `AdminCancel`—gov only.
- Used for GNK with `vesting_blocks > 0`. USDT is never vested.
- Why not `x/streamvesting`: it only accepts senders from an allow-list (gov/inference). Contracts cannot call it without a chain upgrade. v2—add grant-board to `AllowedExternalVestingSenders`.

### 7. Committee management and stop (gov-only)

- `UpsertCommittee`—create/replace committee (members, threshold). Bumps `membership_revision`. Does not touch snapshots (intersection handles drift).
- `SetGrantCommittee` / `SetMilestoneCommittee`—reassign committee. If a milestone in voting is affected—snapshots and votes are wiped.
- `StopGrant { refund_ngonka_to, refund_usdt_to }`—stop grant in any of `Draft / Underfunded / Active`. Returns `unreleased_ngonka` (default community pool) and `unreleased_usdt`. Invalid recipient → partial payout, remainder in `pending_refund_*`, completed via `CompleteRefund`.
- `AdminReleaseMilestone` / `AdminSkipMilestone`—emergency levers.
- `RemoveCommittee` and `TopUpFunding`—deferred to v2.

### 8. Authorization (overview)

| Role | Can do |
|------|--------|
| **Grantee** | `CreateDraft`, `UpdateDraft` (within credits), `CloseDraft`, `SubmitMilestoneEvidence`, `RequestMilestoneExtension`, cranks on own grant, `RecordFundingProposal` |
| **Committee member** | `VoteOnMilestone`, `VoteOnMilestoneExtension`, `VoteOnMilestoneRetry`, `VoteOnMilestoneStop` |
| **Anyone** | `ExecuteMilestoneRelease` (when conditions met) |
| **Hosts (via x/gov)** | Funding, `MarkFunded`, `UpdateConfig`, `UpsertCommittee`, `Set*Committee`, `StopGrant`, `CompleteRefund`, `AdminReleaseMilestone`, `AdminSkipMilestone` |

### 9. Events and tooling

- The contract emits structured events on every state change (`grant_draft_created`, `grant_funded`, `milestone_evidence_submitted`, `milestone_vote_cast`, `milestone_released { mode: approval | auto | auto_on_fund }`, `grant_stopped`, `committee_upserted`, `config_updated`, etc.)—for indexers and dashboards.
- CLI **`grantctl`** alongside `inferenced`:
  - `draft validate`—lint JSON draft;
  - `funding-proposal --grant-id N`—generate funding gov proposal from `FundingProposalTemplate`;
  - `manage-proposal {set-committee,set-milestone-committee,stop}`—management proposal templates;
  - `milestone status` / `process-timeouts`—monitoring and timeout cranks.

Tooling **does not replace** host voting—it only removes manual JSON/base64 errors.


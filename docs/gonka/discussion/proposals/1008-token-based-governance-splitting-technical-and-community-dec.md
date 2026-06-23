---
title: "#1008 — Token-Based Governance: Splitting Technical and Community Decisions"
source: https://github.com/gonka-ai/gonka/discussions/1008
discussion_number: 1008
category: proposals
synced_at: 2026-06-23T15:25:24Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1008](https://github.com/gonka-ai/gonka/discussions/1008) каждые 6 часов. 

# Token-Based Governance: Splitting Technical and Community Decisions

**Автор:** [@Alert17](https://github.com/Alert17) · **Категория:** :bulb: Proposals · **Создано:** 2026-04-03 18:04 UTC · **Обновлено:** 2026-04-20 18:13 UTC

---

## 📝 Описание

# Token-Based Governance: Splitting Technical and Community Decisions
 
## Motivation
 
Gonka governance currently works through the standard Cosmos SDK `x/gov` module. Voting power is derived from **compute weight** — a score each host earns through Proof of Compute activity (nonces delivered, inference work completed). In practice, this means only active hosts (node operators) participate in governance, and their influence is proportional to their hardware contribution.
 
This creates a fundamental mismatch between decision type and decision-maker:
 
- **Hosts are infrastructure operators.** Their compute weight reflects real contribution to the network — inference capacity, uptime, reliability. Giving them authority over technical decisions makes sense.
- **Hosts are not the only stakeholders.** Treasury allocations, marketing budgets, ecosystem grants, and partnership decisions affect all GNK holders — miners who earned GNK through inference work, developers who use the network, and anyone who holds GNK. None of these participants have a formal voice in community decisions today.
 
As Gonka grows — more hosts, more developers, more GNK holders — this mismatch will only become more acute. Community decisions should be made by the community.
 
---
 
## High-Level Solution
 
**Split governance into two tracks based on decision type**, each with the appropriate voter set:
 
| Parameter | Technical Track | Community Track |
|-----------|----------------|-----------------|
| Decision type | Chain upgrades, parameter changes, security | Treasury, marketing, grants, partnerships |
| Who votes | Hosts (weighted by compute) | All GNK holders (weighted by staked GNK) |
| Mechanism | Existing `x/gov` (current system, unchanged) | New Token-Based DAO (DAO DAO on CosmWasm) |
 
Hosts retain full authority over technical decisions — software upgrades, consensus parameters, node configurations. Their compute weight reflects real contribution to the network and is the right signal for protocol-level decisions.
 
All other decisions — how community funds are spent, which partnerships are approved, which marketing initiatives are funded — move to a **Token-Based DAO** where any GNK holder stakes their tokens into the DAO contract and votes proportionally to their staked balance, with results enforced automatically by smart contract.
 
---
 
## Why This Is Feasible Now
 
CosmWasm is already active on Gonka mainnet. The community sale contract and liquidity pool contract confirm that the `x/wasm` module is operational. Token-Based DAOs on DAO DAO are CosmWasm smart contracts — no protocol upgrade is required to deploy them.
 
Gonka's development team already has experience deploying and maintaining CosmWasm contracts. This is not introducing new infrastructure — it is extending what already exists.
 
**Why `dao-voting-token-staked` fits Gonka:** This contract is designed for native tokens that are not used for Proof of Stake network security (e.g. ION on Juno, IBC tokens). Gonka does not use traditional PoS staking — network security is provided by compute weight via Sprint PoW and PoC V2. GNK is a reward/utility token, not a PoS staking token, which makes `dao-voting-token-staked` the correct module for this use case.
 
---
 
## Technical Details
 
### Current Architecture
 
```
All proposals → x/gov → Host vote (weighted by compute) → Execution
```
 
### Proposed Architecture
 
```
Technical proposals  → x/gov (unchanged)  → Host vote            → Execution
Community proposals  → Token-Based DAO    → All GNK holders vote → Smart contract execution
```
 
### How Voting Works
 
The Token-Based DAO uses the `dao-voting-token-staked` contract. To participate in governance, GNK holders must **stake their tokens into the DAO contract**. This is a separate action from holding GNK in a wallet — staking locks tokens in the contract and grants voting power proportional to the staked amount.
 
When a proposal is created, the contract **snapshots staked balances at that block height**. Only tokens staked before the proposal was created count toward the vote. This prevents vote-buying attacks where someone acquires GNK after seeing a proposal.
 
**What this means for participants:**
- **Stake once** — tokens remain staked across multiple proposals. No need to re-stake for each vote
- **Unstaking** — tokens can be unstaked at any time (subject to an unbonding period, if configured)
- **No node required** — any wallet can stake and vote. No Cold Account Key, no hardware, no uptime requirement
- **Staking ≠ locking forever** — this is governance staking into the DAO contract, not PoS validator delegation
 
### Token-Based DAO Components
 
DAO DAO uses three CosmWasm contracts to power a Token-Based DAO:
 
| Contract | Role |
|---------|------|
| `dao-core` | Central registry, holds DAO configuration and treasury |
| `dao-proposal-single` | Proposal creation, voting period management, tally |
| `dao-voting-token-staked` | Manages GNK staking into the DAO, calculates voting weight from staked balances at any block height |
 
### Decision Classification
 
| Category | Examples | Track |
|----------|----------|-------|
| Chain upgrade | New binary version, Cosmovisor upgrade | Technical → `x/gov` |
| Parameter change | Epoch length, collateral requirements, PoC V2 settings | Technical → `x/gov` |
| Security | Emergency halts, critical fixes | Technical → `x/gov` |
| Treasury spend | Marketing partnerships, media deals, any spend >10K GNK | Community → Token-Based DAO |
| Grants | Ecosystem fund allocations, developer grants | Community → Token-Based DAO |
| Partnerships | Exchange listings, integration agreements, co-marketing | Community → Token-Based DAO |
| Community initiatives | Events, educational content, ambassador programs | Community → Token-Based DAO |
 
**Default classification rule:** If a proposal does not clearly fall into a single track, it defaults to the **Community track** (Token-Based DAO). The rationale: community decisions affect more stakeholders, and the wider voter set provides a more representative outcome. Any participant can challenge a classification by submitting a counter-proposal to the other track — the first to reach quorum takes precedence.
 
### Proposed Governance Parameters (Token-Based DAO)
 
| Parameter | Proposed Value | Rationale |
|-----------|---------------|-----------|
| Voting period | 7 days | Sufficient time for community awareness |
| Quorum | 5% of staked GNK in the DAO | Realistic given that only on-chain, non-exchange GNK can be staked |
| Passing threshold | 50% Yes (excluding Abstain) | Standard majority |
| Veto threshold | 33% NoWithVeto | Consistent with Cosmos standard |
| Proposal deposit | 500 GNK | Spam prevention; refunded on pass or fail, burned on veto |
 
**Note on quorum:** GNK held on centralized exchanges cannot be staked into the DAO contract and therefore cannot vote. The 5% quorum is calculated against staked GNK in the DAO, not total circulating supply — this makes the threshold achievable while still requiring meaningful participation.
 
**Note on veto risk:** With token-weighted voting, large holders could theoretically veto proposals unilaterally if they hold >33% of staked GNK. This is a known property of all token-weighted governance systems. The mitigation is broad staking participation — as more holders stake, the concentration of any single voter decreases. The community should monitor staking distribution after deployment and adjust the veto threshold via governance vote if concentration becomes a concern.
 
All parameters are adjustable by community vote after deployment.
 
---
 
## Implementation Plan
 
**Week 1–2 — Preparation and Testing**
1. Audit Gonka's existing CosmWasm deployment — confirm `x/wasm` permissions and available code IDs
2. Deploy and configure DAO DAO contract suite in a local environment
3. Configure `dao-voting-token-staked` against GNK native denom
4. Validate staking, snapshotting, voting mechanics, and automatic execution
 
**Week 3 — Governance Proposal**
5. Submit on-chain `x/gov` proposal to authorize DAO DAO contract deployment on mainnet
6. Community review period
 
**Week 4 — Mainnet Deployment**
7. Deploy contracts to mainnet
8. Transfer an initial **governance sub-fund of 10,000,000 GNK** from the Community Pool (120M GNK) to the Token-Based DAO treasury via `x/gov` Community Pool Spend proposal
9. `x/gov` remains active for technical decisions — only community decisions migrate to the DAO
 
**90-Day Parallel Period**
Both systems run simultaneously. Community builds confidence in the new DAO before expanding treasury scope. During this period:
- Community proposals go through the Token-Based DAO with the initial sub-fund
- Technical proposals continue through `x/gov` as before
- At the end of the parallel period, a governance vote determines whether to expand the DAO treasury or maintain the current allocation
 
---
 
## What Does Not Change
 
- Hosts retain full authority over technical decisions
- The existing governance interface remains for technical proposals
- Consensus, security, and upgrade decisions continue through `x/gov`
- No changes to host economics, rewards, or node operations
 
---
 
## Open Questions
 
1. **Sub-fund size** — 10,000,000 GNK proposed (~8.3% of Community Pool) as the initial DAO treasury. Is this the right amount for the parallel period? Too much risk? Too little to be useful?
2. **Deposit threshold** — 500 GNK proposed. Does this create a barrier for smaller community members to submit proposals?
3. **Quorum** — 5% of staked GNK proposed. This depends on how many holders actually stake into the DAO. Should there be a minimum staking threshold before the DAO becomes active?
4. **CEX holders** — GNK held on exchanges cannot be staked or vote. This is a known limitation of all on-chain governance systems. Out of scope for this proposal.
5. **Unbonding period** — Should unstaking from the DAO have a cooldown (e.g. 7 days)? This prevents vote-and-dump attacks but adds friction for participants.
 
---
 
## Budget
 
**Phase 1 (this proposal): No treasury spend requested.**
 
Initial deployment, configuration, and testing will be contributed by the proposing team. This proposal authorizes the governance migration plan and the deployment of DAO DAO contracts on mainnet.
 
**Phase 2 (separate proposal after validation):**
 
| Item | Estimated Cost | Notes |
|------|---------------|-------|
| Contract audit (third-party) | 5,000–15,000 GNK | Scope depends on customization level |
| Initial DAO treasury sub-fund | 10,000,000 GNK | From Community Pool via `x/gov` spend proposal |
| Deployment and integration | Contributed | No cost to treasury |
 
The Phase 2 budget will be submitted as a separate on-chain `x/gov` Community Pool Spend proposal once the implementation is validated during Weeks 1–2.
 
---
 
## References
 
1. **DAO DAO Token-Based DAO** — architecture and contract documentation. Source: [docs.daodao.zone](https://docs.daodao.zone)
2. **DAO DAO contracts** — deployed contract code IDs across Cosmos chains. Source: [github.com/DA0-DA0/dao-contracts](https://github.com/DA0-DA0/dao-contracts)
3. **`dao-voting-token-staked`** — native token staking module for DAO DAO governance. Source: [crates.io/crates/dao-voting-token-staked](https://crates.io/crates/dao-voting-token-staked)
4. **CosmWasm on Gonka** — confirmed active via community sale and liquidity pool contracts. Source: [gonka-ai/gonka releases](https://github.com/gonka-ai/gonka/releases)
5. **Cosmos SDK `x/gov`** — existing governance module, retained for technical decisions. Source: [docs.cosmos.network/main/modules/gov](https://docs.cosmos.network/main/modules/gov)
6. **Gonka Tokenomics** — GNK supply distribution, community pool. Source: [docs/tokenomics.md](https://github.com/gonka-ai/gonka/blob/main/docs/tokenomics.md)

---

## 💬 Комментарии (2)

### Комментарий 1 — [@paranjko](https://github.com/paranjko)

*2026-04-06 13:43 UTC*

The architecture looks feasible, and using DAO DAO on top of the existing CosmWasm stack seems like a practical approach.

But a few questions still need to be clarified:
— who classifies ambiguous proposals?
— how is whale concentration handled?
— who evaluates off-chain deliverables and outcomes?

Without clear answers to these questions, the DAO could approve decisions that are valid on-chain but messy in practice.

**↳ Ответ от [@Alert17](https://github.com/Alert17)** · *2026-04-07 11:13 UTC*

> Thanks. 
> All three are valid concerns. I have some thoughts on each and can share them later, but I'd rather hear other positions and points of view first before proposing specific solutions. Would be great to discuss with the community and look at different options.

### Комментарий 2 — [@aeoess](https://github.com/aeoess)

*2026-04-20 17:52 UTC*

@paranjko's three questions all land on the same gap: the proposed split works at the contract level (x/gov for technical, DAO DAO for community) but the bridge between on-chain correctness and off-chain reality is left unspecified. "Valid on-chain but messy in practice" is the failure mode governance architectures fall into whenever the bridge stays informal.

The bridge is a thin cryptographic attestation layer, emitted as typed Cosmos SDK events, that the voting and treasury contracts listen to without taking on new trust assumptions. Three event types cover the questions raised and one implicit gap in the current parameter proposal.

**1. Classification provenance: who decided Technical vs Community.**

Today the classification decision is invisible. Someone routes a proposal, later it turns out it should have been the other track, no record of who made the call or on what grounds.

A signed classification note from the proposer at submission time fixes this. The note is an Ed25519-signed record carrying the proposal ID, the chosen track, a hash of the rationale text, factors considered, and alternative tracks rejected with reasons. It doesn't block anyone from re-routing (that stays a governance decision), it just makes the history auditable.

Cosmos SDK event shape:

```
ProposalClassificationAttested {
  proposal_id,
  proposer_pubkey,
  declared_track,          // "technical" | "community"
  rationale_hash,          // sha256 of the reasoning text
  factors_considered,      // e.g., ["spend_size", "chain_upgrade_involvement"]
  alternatives_rejected,   // other tracks + why-not
  confidence,              // 0-1 self-rating, flags ambiguity
  signature
}
```

The event is emitted by a small ante handler (slots alongside the existing `ante_validation.go` pattern) that verifies the signature before the proposal enters either voting module. If verification fails, the submission rejects with a clear error. If it passes, the event indexes and downstream tooling (proposal explorers, audit dashboards, governance bots) can consume it.

Ambiguous proposals surface through low confidence scores plus populated alternatives-rejected arrays. Treating confidence below a threshold as mandatory-review is straightforward. The threshold value is a governance-layer choice for Gonka.

**2. Weight-class attestation: proposal-size-scoped governance parameters.**

One gap that isn't in paranjko's questions but the Open Questions section of the proposal hints at: #1008 uses a flat 5% quorum and 500 GNK deposit regardless of proposal size, but a 50K GNK grant and a 10M GNK treasury sweep probably shouldn't pass under the same participation threshold.

A weight-class attestation declares the proposal's size bucket at submission (Small / Medium / Large by GNK spend, or a finer scheme) and the DAO contract applies bucket-appropriate quorum and threshold rules. Same signature infrastructure as classification, different event:

```
ProposalWeightClassAttested {
  proposal_id,
  weight_class,                 // "small" | "medium" | "large"
  declared_spend_gnk,
  class_thresholds_expected,    // quorum + threshold the proposer believes apply
  signature
}
```

Any verifier can cross-check declared spend against the proposal body at vote time. Intentional misdeclaration becomes evidence rather than invisible gaming. The bands themselves (spend thresholds, corresponding quorums) would live in the DAO contract config and stay governance-adjustable.

Two reasonable interpretations of weight-class worth surfacing: the size-scoped-parameters version above, or an eligibility class where the proposer's compute weight or staked GNK has to exceed a minimum for the proposal to be admissible. Both shapes are workable, and the events differ only in payload. Worth the thread's input on which the proposal intends.

**3. Deliverable evaluation: who confirms the work shipped.**

This is the biggest of the three. The DAO votes in Week 1, the work ships in Week 6 or later, and the current model has no on-chain signal for "the thing that was funded actually happened." Release of funds is implicit in the passing vote. The gap between "vote passed" and "deliverable met" is covered by community trust rather than verification.

A three-way signed outcome record closes the gap without the DAO contract changing how it holds funds:

- **Proposer report** (signed by proposer): claimed delivery, divergence from declared intent
- **Evaluator report** (signed by designated evaluator): independent assessment, divergence from expected outcome
- **Adjudicator report** (signed by an arbiter, only if the first two disagree beyond tolerance)

Consensus is auto-computed when proposer and evaluator divergence scores align within a tolerance (0.15 is a reasonable starting value, adjustable). Consensus triggers the release event the DAO treasury contract listens for. No adjudicator needed in the common case. Disputed cases escalate automatically.

```
ProposalDeliverableAttested {
  proposal_id,
  proposer_report: { outcome_hash, divergence_score, signature },
  evaluator_report: { evaluator_pubkey, outcome_hash, divergence_score, signature },
  adjudicator_report?: { adjudicator_pubkey, outcome_hash, signature },
  consensus: bool
}
```

Open question worth the thread's input: is the evaluator pinned per-proposal at approval time, or nominated by the proposal itself and ratified alongside approval? Both compose with the record shape:

- **Per-proposal pinning at approval.** A named evaluator (or slate of evaluators) is attached to the proposal at the moment it passes. The proposer can't pick a friendly reviewer after the fact. Cleaner authority scoping, slight overhead at approval time because the community has to agree on who.
- **Proposal-nominated, approval-ratified.** The proposer nominates an evaluator in the proposal body. The ratification vote covers both the spend and the evaluator. Less overhead, but creates an incentive for proposers to nominate predictable reviewers, which shifts gaming from the deliverable stage to the nomination stage.

My instinct is per-proposal pinning. The gaming surface is smaller and the evaluator's accountability is clearer. But the nominated-then-ratified model has real arguments too, particularly for proposals with specialized technical scope where few community members have the expertise to evaluate.

**On whale concentration.**

The attestation layer doesn't fix this directly. Vote weight lives inside `dao-voting-token-staked`, and that's contract-level, not attestation-level. Curator delegation (whales delegating voting power to domain experts) is the attestation-friendly mitigation: the delegation record becomes a signed event with monotonic scope narrowing, delegator keeps revocation authority, delegate's authority is auditable. But whales delegate only when they choose to. Quadratic or conviction voting would narrow concentration more directly, both are contract-level changes to the voting module.

Worth naming as the question where the audit layer doesn't have a clean answer, rather than pretending otherwise.

**On implementation.**

Happy to contribute the Go-side pieces if #1008 moves forward with this shape:

1. Go library for Ed25519 signature verification over the three attestation records, reusable across ante handlers and any other consumer
2. Reference ante handler wiring that validates classification and weight-class attestations at proposal submission (fits the existing `ante_validation.go` pattern)
3. CosmWasm helper contract that validates deliverable attestations and emits release events the DAO treasury contract can listen to, living in the same CosmWasm environment #1008 already commits to

All three are small, specific pieces that sit alongside the existing x/gov, DAO DAO, and ante chain without requiring changes to any of them.

The signing, scoring, and three-way consensus primitives already exist as TypeScript and Python reference implementations. The Cosmos SDK Go adapter is the specific missing bridge, and it's Gonka-shaped work regardless (not something that gets reused by a non-Cosmos consumer). Worth doing right for Gonka first, then generalizing if other Cosmos projects ask later.


**↳ Ответ от [@Alert17](https://github.com/Alert17)** · *2026-04-20 18:13 UTC*

> Thanks, this is a really interesting angle. The attestation layer framing makes sense: treating classification, weight-class, and deliverable verification as signed records that sit alongside the existing contracts rather than inside them keeps the surface small and composable.
>
> I'd say this is a full, self-contained option for the set of problems that need to be solved here, and definitely one worth keeping on the table as the discussion develops. Still want to hear where others land before converging on a specific direction, but appreciate you writing it up in this much detail.

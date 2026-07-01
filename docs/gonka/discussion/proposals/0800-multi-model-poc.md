---
title: "#800 — Multi-Model PoC"
source: https://github.com/gonka-ai/gonka/discussions/800
discussion_number: 800
category: proposals
synced_at: 2026-07-01T20:15:38Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #800](https://github.com/gonka-ai/gonka/discussions/800) каждые 6 часов. 

# Multi-Model PoC

**Автор:** [@gmorgachev](https://github.com/gmorgachev) · **Категория:** :bulb: Proposals · **Создано:** 2026-02-25 04:24 UTC · **Обновлено:** 2026-04-20 14:57 UTC

---

## 📝 Описание

# Proposal: Multi-Model PoC

POC procedure is short term benchmark to compare how much compute each host has. It happens 1 time per epoch to define weight per each host which then used as consensus weight to produce blocks and for distributing tasks between hosts. Additionally there is Confirmation (random) POC which is used to confirm weight when network is underloaded by inference (to make sure hardware it still there).

POC phases:
- GENERATION (blocks equal to 1-5 min)
- VALIDATION (blocks equal to 2-10 min)
- INFERENCE PHASE (no POC but sometime might be interrupted to Confirmation POC)

> Validation and inference theoretically can be done in parallel.


Current security model required >50% of **total network consensus weight** to vote "valid". Without delegation, an attacker needs >50% of total network weight to corrupt any (and all) host's validation.

The bitcoin-style part of reward distributed proportionally to this weight. On early phase it's main motivation as inference is much cheaper. 

## Problem

The chain must support multiple models.

Currently the chain can’t support multiple models because we have single-model PoC

Why can’t we support multiple models with single-model PoC?

If we serve multiple models with current single-model PoC, that means that you need to redeploy a model before each cPoC. And if you can do that - you can use this time to deploy models on new nodes. Which essentially opens the network for attack when attacker deploy hardware only for POC phase
Why do we need cPoC at all?

Because a) we want to make sure that if the network load is low - compute is still there b) until the quality of benchmarking hardware by the users’ inference itself is high enough 
Thus the option of redeploying models for PoC vs inference can’t be used and we need to figure out how to support different models during PoC and cPoC.


## Proposal

Let's try to build a system which supports several models simultaneously where POC procedure happens without re-deploy, for every model independently. Such different POCs correspond to quite different compute power (essentially they would measure not raw compute power but how "optimal" the configuration is for specific hardware).
As POC is not only a source of the weight for task distribution across a specific model but also a way to define the consensus weight, we need to define how to aggregate weights from different POCs and how to validate each POC's results.

For aggregation, the chain would have to define how *valuable* each POC's weight is to the chain. Coefficients converting POC weight to consensus weight can be defined as governance parameters by direct voting. They can be defined in a way that bigger, more powerful and more popular models would bring more weight. As the newest hardware is also optimized for serving top-tier models (a lot of VRAM, fast cross-gpu connection, FP4/FP8 support, etc.), it would naturally incentivize hosts to switch newer GPUs to the most powerful models, to get more weight per \$. It's important for the chain's growth to make serving best models (which require most optimized GPUs) most profitable.

This proposal sets the goal to maintain same style of POC validation - every host validates every other host (or its probabilistic analogy for case of slots). One approach to achieve that would be to enforce each host to participate (have hardware) in each model. But such approach is impractical and would raise the hardware requirements too much. To avoid that, the proposal introduces *PoC delegation* from a host to another host it trusts. Such delegation allows to maintain the property of validation by majority of consensus power (but for sure introduces new security assumption, more about it in Appendix A).

To define the process of adding new models to the chain, this proposal allows serving models which are not approved by governance, without inference validation and without gaining consensus power from serving such models. It also defines the process how a model approved by governance becomes eligible for consensus weight.  

> **Warning**: This proposal assumes the O(N^2) validation model (>50% weight threshold). Slot-based validation is out of scope. Most probably slot-based approach will work the same way, with independent slot assigning in each group. But it must be double-checked whether to use $votingPower$ or $consensusWeight$ for hosts in group.


### Terms

Let epoch $S$ be current. The following defines weight computation for epoch $S+1$. Pre-eligibility ($PreE_{S+1}$) is determined $N$ blocks before epoch $S+1$ PoC starts. In this section, $*_S$ denotes values from epoch $S$ and used as inputs for epoch $S+1$.
Group membership and delegation are evaluated at the pre-eligibility cutoff and treated as fixed for the epoch.

- $group_i$ — model group for model $i$ (members are hosts with MLNodes serving model $i$). Network supports $M$ models on-chain.

- $pocWeight_S(group_i, p)$ — weight of host $p$ in $group_i$ at epoch $S$. Equals the number of nonces computed by $p$ in PoC procedure for this group and successfully validated. Local weight within the group.

- $consensusKoeff_i$ — coefficient converting $pocWeight$ in $group_i$ to consensus weight. Defined by governance per model.

- $consensusWeight_S(p) = \sum_{i: group_i \in E_S} consensusKoeff_i \times pocWeight_S(group_i, p)$ — (see Appendix A for cap protection)

- $members(group_i) = \lbrace p : p \text{ has MLNode deployed for model } i \rbrace$ — hosts with MLNode deployed for the model

- $hosts_S(group_i) = \lbrace p : consensusWeight_S(p) > 0 \text{ and } p \in members(group_i) \rbrace$

  Members with non-zero consensus weight. The weight may come from any eligible group, not necessarily $group_i$.

- $PreE_{S+1}$ — set of pre-eligible groups for epoch $S+1$. A group $group_i \in PreE_{S+1}$ if conditions 1-3 hold:
  1. Model $i$ is approved by governance with defined $consensusKoeff_i$
  2. $\sum_{p \in members(group_i)} consensusWeight_S(p) \geq W_{threshold} \times \sum_{p} consensusWeight_S(p)$
  3. $|hosts_S(group_i)| \geq V_{min}$

- $E_{S+1}$ — set of consensus-eligible groups for epoch $S+1$. A group $group_i \in E_{S+1}$ if:
  - $group_i \in PreE_{S+1}$
  - At least $V_{min}$ hosts in the group pass PoC validation at epoch $S+1$ (see validation rule below)

- $W_{threshold}$ — minimum fraction of total network consensus weight required for group eligibility (governance parameter)

- $V_{min}$ — minimum number of hosts with non-zero consensus weight required in a group (governance parameter)

- Currently $group_{Qwen3-235B-FP8}$ is the only eligible group (single-model PoC). This proposal extends to multiple groups.

- The initial group ($group_{Qwen3-235B-FP8}$) is exempt from the weight cap (Appendix A) and provides base consensus weight for validating new groups.

- A host participating in multiple eligible groups requires separate hardware per group. PoC runs concurrently across all eligible groups within the same epoch.

- $delegation_S(group_i, p_{from}, p_{to})$ — consensus weight delegated from host $p_{from}$ to host $p_{to}$ for validation in $group_i$ at epoch $S$. Host $p_{from} \notin members(group_i)$; host $p_{to} \in members(group_i)$. Delegation is set before epoch start; changes during an epoch take effect from the next epoch.

- $r_{delegation}$ — fraction of bitcoin-style reward delegator shares with delegate (governance parameter, e.g., 1%, per each group??)

- $r_{refusal}$ — fraction of bitcoin-style reward sent to governance when host explicitly refuses to participate in a group; must be > $r_{delegation}$ (governance parameter, e.g., 5%, per each group??)

- $r_{penalty}$ — fraction of bitcoin-style reward lost when host fails to make a participation choice for any governance-approved group (governance parameter, target 100%)

- $T_{grace}$ — grace window duration after governance approval before penalties apply (governance parameter, e.g., 3 epochs)

- $votingPower_S(group_i, p) = consensusWeight_S(p) + \sum_{p_{from}} delegation_S(group_i, p_{from}, p)$ — total validation voting power of host $p$ in $group_i$

  Delegation constraints: $delegation_S(group_i, p_{from}, p_{to}) \ge 0$ and, for each $(group_i, p_{from})$, $\sum_{p_{to}} delegation_S(group_i, p_{from}, p_{to}) \le consensusWeight_S(p_{from})$.

**Q1: Can a host split delegation across multiple hosts in the same group?**

### Eligible Groups

Weight computed in PoC procedure for eligible model groups contributes to total consensus weight via governance-defined coefficient. Consensus weight determines:
- Block signing power
- Governance voting power
- PoC validation voting power
- **Bitcoin-style reward distribution** (proportional to consensus weight)

Within a group, inference requests are distributed according to $pocWeight_S(group_i, p)$. Inference rewards follow the same distribution.

### PoC Validation

**Delegation**: Hosts not in a group can delegate their consensus weight to a host who is. The delegate votes on their behalf. Delegation is per-group and set before epoch start.

**Validation rule**: Host $p$'s PoC result in eligible $group_i$ is accepted if:

$$\frac{\sum_{v \text{ votes valid for } p} votingPower_S(group_i, v)}{\sum_{q} consensusWeight_S(q)} > \frac{1}{2}$$

- Numerator: sum of $votingPower_S(group_i, v)$ from all validators $v$ who approved $p$
- Denominator: total network consensus weight (all hosts, all groups)

Hosts not in the group and not delegating effectively vote against approval. Delegation is therefore essential for any group whose direct members hold less than 50% of total network weight.

**Voting power details**:
- Number of MLNodes does not matter -- 1 MLNode or 100 MLNodes yields the same vote power
- Delegation changes take effect from next epoch

**Trust model**: Delegator trusts the delegate to vote correctly.

**TODO**: Mechanism to revoke delegation mid-epoch if delegate votes maliciously.

### Mandatory Group Participation & Incentive

Every host with consensus weight must actively participate in every governance-approved group. For each group, the host chooses one of:

1. Join group — deploy hardware and participate directly in the group
2. Delegate — delegate voting power to a group member; delegator shares $r_{delegation}$ with delegate, incentivizing group members to build trust
3. Explicit refusal — decline to delegate or join; costs $r_{refusal}$; must be renewed each epoch

During the grace window ($T_{grace}$ epochs after governance approval), hosts must make a participation choice but there is no penalty for any choice. After the grace window ends, penalties apply: hosts who didn't make a choice lose $r_{penalty}$ of their bitcoin-style reward.

This incentivizes >50% of total consensus weight to participate in PoC validation for every governance-approved group.

### Unregistered Models

Any host can add a model to the chain and serve inference without governance approval (with additional fees).

Properties:
- No inference validation by other hosts
- Price set directly by host
- Requests sent directly to host
- Host stores payload locally but no cross-validation
- Each GNK payment has fee sent to governance
- No bitcoin-style rewards

Purpose: build demo-case for governance proposal to show demand for the model.

### Model Lifecycle

1. Unregistered phase — host adds model, serves inference directly to users, builds demo-case for governance proposal
2. Governance proposal — model approved with defined $consensusKoeff_i$, group created
3. Grace window ($T_{grace}$ epochs) — mandatory participation rules apply but without penalties; hosts make participation choices (join/delegate/refuse); PoC runs for the group
4. After grace window — penalties apply ($r_{penalty}$, $r_{delegation}$, $r_{refusal}$); eligibility still depends on meeting conditions ($W_{threshold}$, $V_{min}$, passing PoC validation)

A governance-approved group may or may not be eligible in any given epoch depending on whether it meets eligibility conditions.

## Implementation

[To be defined]

## Appendix A: Delegation-based Attack and Protection

**Attack:** Host accumulates >50% $votingPower$ via delegation, validates fake participant claiming large weight, gains consensus control.

**Protection option:** Cap weight from each group by members' proven weight elsewhere.

$$\text{consensus weight from } group_i \leq f \times \sum_{p \in members(group_i)} \text{(}p\text{'s consensus weight from other eligible groups)}$$

If a group's raw PoC weight exceeds the cap, scale all members proportionally to fit.

For clarity: "other eligible groups" refers to consensus weight already earned from eligible groups excluding $group_i$ itself (i.e., using $consensusWeight_S$ contributions from $E_S \setminus \lbrace group_i \rbrace$), to avoid circular dependence.

- Initial group exempt (no cap)
- $f$ is a governance parameter
- Delegation affects $votingPower$ but not the cap (cap is PoC-weight-based)

This bounds the damage from fake participants: even if they pass validation, their weight contribution is limited by real members' stake in other groups. The cap is a secondary defense; validation (>50% of network weight) remains the primary one.

**Q5: What should $f$ be?**


---

## 💬 Комментарии (5)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-02-27 20:54 UTC*

Please consider joining the discussion on this proposal and sharing any ideas or suggestions. An initial version will be provided by the proposal author, and feedback from participants will help refine the approach and clarify next steps.

### Комментарий 2 — [@akup](https://github.com/akup)

*2026-03-01 07:24 UTC*

Questions
1. When host A delegates it's vote to host B in another model group, it adds the voting power to host B. But why it is not reducing voting power of host A?

2. If some host A trusts host B it seams that they are already in the trust group and have communication and can agree on joint actions. Actually what is the difference if it was one host?

3. How participant can choose to what host delegate it's weight? How it could be practically coordinated?
It would be more clear if there will be real world example with a step by step plan:
if there is a new model, and there are new hosts who want to run it, how do they start?
How they are getting delegation, how hosts from other groups starting to know that they need to delegate and how they can decide what host to choose to delegate it's vote to?

4. How many hosts should run the model to start group working. For example if there is just 2 hosts will they get the reward? If there are 3 hosts? Form what number of hosts we can trust the group (seems to be related to Q5 question)

5. How following scenario can be avoided?
New grace period begins.
Attacker creates multiple hosts that are going to participate with the model
Participants from other groups, as they don't know personally to whom delegate the vote, delegate it to "random someone"
Also attacker delegates his votes (from multiple hosts) to his hosts in a new group.
And attacker gets the control of the group

6. Isn't it simpler to have a new model seed (genesys) group? For example, hosts that already have voting power can run some of their mlnodes with new model and get additional reward for participating in early start of the new model group. They help to start the new model group (as they have resources and are interested in network development) as they already have the voting power, but there will no be all difficulties (that are not only technical but also real-life practical) of delegation.

p.s.
**Unregistered Models** is a very good point

**↳ Ответ от [@gmorgachev](https://github.com/gmorgachev)** · *2026-04-02 05:08 UTC*

> >  But why it is not reducing voting power of host A?
> host A doesn't have voting power in this model group, it can't be reduces. host A can either has MLNode with this model or delegate its PoC validation
> important: it's doesn't affect consensus weight of any hosts
>
> > If some host A trusts host B it seams that they are already in the trust group and have communication and can agree on joint actions. Actually what is the difference if it was one host?
> In my understanding host A can delegate to well known hosts with great reputation on mainnet. So they don't have to really know each other but host A must trust host B incentive to act honest. I think the joining nodes is much closer :) 
>
> > How many hosts should run the model to start group working. For example if there is just 2 hosts will they get the reward? If there are 3 hosts? Form what number of hosts we can trust the group (seems to be related to Q5 question)
> I don't think any validation can happen with less then 3 hosts. But we also must have limitation on the total consensus weight of this this model group participants. I think it should not be less then at least 5-10% of the network (if talk about today's size)
>
> > How following scenario can be avoided?
> From my perspective it should be combination of limits on:
> - minimal consensus power from another group which hosts must have for group to be eligible (5-10%+)
> - cap on the weight which single group might have (to avoid getting control of the whole chain)
>
> I agree that delegation to "random someone" is serious concern and mechanism relies on the fact that host must make informed decision about delegation. Do you have some additional ideas how to protect in mind? 
>
> ------
>
> > Isn't it simpler to have a new model seed (genesys) group? For example, hosts that already have voting power can run some of their mlnodes with new model and get additional reward for participating in early start of the new model group. They help to start the new model group (as they have resources and are interested in network development) as they already have the voting power, but there will no be all difficulties (that are not only technical but also real-life practical) of delegation.
>
> I don't see how it would help to avoid delegation. The question is what consensus weight will have such group. If only their weight counts, with current limit such seed group must control > 2/3 of the total network power for PoC to pass. Which is impossible 
> If PoC inside this new group will be counted only from weight of participants - such early seed nodes can also easily cheat.
>  
> In the original proposal the initial seed group is still existing validators with some threshold on their total weight. Delegation just allows to make this threshold lower then 2/3

**↳ Ответ от [@gmorgachev](https://github.com/gmorgachev)** · *2026-04-02 05:58 UTC*

> Sorry, i used 2/3 instead of 50% in the comment as found out that mainnet already uses 2/3 as the threshold

### Комментарий 3 — [@andrey055](https://github.com/andrey055)

*2026-03-03 12:13 UTC*

The proposal to test new models without a Bitcoin-style reward is very strong.

I would really like to see it implemented. Of course, there are certain concerns — for example, the risk that a host could discredit the network by deploying an incorrectly configured model, such as one with a reduced context window.

I hope appropriate safeguards against this will be put in place.

### Комментарий 4 — [@jacky6block](https://github.com/jacky6block)

*2026-03-04 10:16 UTC*

Thanks for writing this up — the high-level direction (multi-model PoC w/o redeploy; per-model PoC weights aggregated into consensus weight) makes sense. After reading the whole proposal + Appendix A, I think there are a few **high-risk gaps** and several **must-clarify** items before this feels safe / implementable.

---

## 1) Delegation shifts validation power from “hardware” to “social coordination” (security + liveness)

### Bribery / delegation aggregation becomes the cheapest attack vector
When a new group’s native members hold far less than the >50% global threshold, delegation becomes the **only practical** path to pass PoC validation during cold-start. In that regime, an attacker may be able to acquire majority `votingPower` by bribing / incentivizing a small number of high-`consensusWeight` delegators — potentially much cheaper than provisioning equivalent hardware.

### Cold-start deadlock / structural veto by incumbents
Because “valid” requires **>50% of global `consensusWeight`**, a new model group can get stuck if large-weight hosts don’t actively delegate (apathy, coordination costs, or strategic refusal). This effectively gives incumbents a veto and makes onboarding new models depend heavily on off-chain coordination.

### Revocation / reaction latency is still a TODO
The proposal mentions the need to revoke delegation mid-epoch, but it’s not specified how:
- delegators detect delegatee misbehavior fast enough (PoC windows are minutes),
- revocation becomes effective *within the same epoch*,
- losses are handled if detection happens after the validation window.

---

## 2) Clarification needed: delegation “spending” vs “replication”
In the current definition of `votingPower(group_i, p)` (additive with delegated amounts), it’s easy to interpret delegation as *adding* weight on top of the delegatee without clearly “removing” it from the delegator’s effective budget inside that group.

**Request:** please explicitly define delegation semantics as a **group-specific transfer of validation budget (not replication)**. Concretely:
- once `p_from` delegates to `p_to` for `group_i`, does `p_from` forfeit any direct voting/validation influence in that group for the epoch?
- does delegation affect *only* group validation voting, or also global governance / block production weight?

My suggestion would be: delegation should be **scoped to group validation only** (no change to global block production / governance weight), and should be modeled as **non-double-spendable** budget inside the group.

Also, please clarify what “non-participation is effectively a no vote” means in the math: is it abstain counted via denominator, abstain excluded, or simply absent from numerator while denominator remains global total?

---

## 3) Scalability: O(G · N^2) validation is hard to see as sustainable
Keeping O(N^2) validation per group becomes **O(G·N^2)** when multiple eligible groups run in parallel. Even if bandwidth is okay, CPU sig verification, state handling, retries, and fork recovery will likely bottleneck — especially in 2–10 minute windows.

Also “PoC/validation and inference can run in parallel” needs a concrete **resource isolation / priority** story. Even with separate GPUs per group, network + CPU contention can still degrade inference latency/UX.

**Request:** outline either:
- a concrete scalability plan (sampling/batching/quotas) that preserves the >50% semantics, or
- why O(G·N^2) is acceptable under realistic target N and G.

---

## 4) Cap (Appendix A) doesn’t fully address group-local capture / fairness
Cap limits a new group’s impact on **global** consensus weight (inflation / sudden dominance), but it doesn’t stop **group-local capture**, e.g. coordinated voting to mark honest participants invalid or monopolize inference revenue for a popular new model.

Cap also depends on weight earned in other mature groups → strong path dependence / incumbent advantage (new entrants are structurally capped even if they’re best on the new model).

**Request:** clarify what cap is intended to mitigate (global takeover vs group-local capture), and consider extra mechanisms for group-local correctness/fairness (challenge/appeal, slashing, auditability, etc.).

---

## 5) “Independent hardware per group” looks like a soft requirement today
Without a verifiable attestation mechanism (TEE / hardware fingerprints / vendor attestation), the “independent hardware per eligible group” requirement is technically unenforceable. Actors could potentially use virtualization (vGPU) or scheduling tricks to appear in multiple groups from the same physical hardware.

**Request:** should we treat this as a best-effort policy rather than a security pillar (and say so explicitly), or introduce some form of hardware spec registration / attestation / auditing?

---

## 6) Optional improvement directions (appendix-level, but worth discussing)
- **Slot-based / VRF sampling validation:** Given O(G·N^2), consider VRF-based per-group validator sampling with quantitative security analysis (failure probability vs adversarial weight, sample size).
- **Strengthen unregistered phase as an observation period:** use real GNK demand signals (revenue + distinct payers + dispute/refund rates) to constrain/recommend `consensusKoef` instead of purely governance discretion (needs anti-wash-trading / anti-sybil guardrails).
- **Hardware attestation roadmap:** even if not ready now, discuss whether platform attestation (TEE/SEV/TPM) or vendor attestation can reduce cross-group hardware reuse.

Happy to help refine parameters (W_threshold, V_min, T_grace, f) or propose sampling sizes / threat-model math. IMO the critical path items are: **delegation semantics + cold-start/liveness + a scalability plan**.

**↳ Ответ от [@gmorgachev](https://github.com/gmorgachev)** · *2026-04-02 05:20 UTC*

> > 1) Delegation shifts validation power from “hardware” to “social coordination” (security + liveness)
> > Bribery / delegation aggregation becomes the cheapest attack vector
>
> To be honest not sure how it changes the security model. There is same BFT assumption that >2/3 of hosts are honest, in terms of bribery too. If we assume that attacker can bribe honest supermajority, then they would be able to bribe them during PoC validation without delegation too, am i missing smth?
>
> > Cold-start deadlock / structural veto by incumbents
>
> Refusal to delegate after the grace period would lead to penalty on bitcoin-style reward. Which creates incentive for big hosts to delegate
>
> > Revocation / reaction latency is still a TODO
>
> The epoch now is about 24hours. I was thinking about the case when in the middle of epoch N host A understands that host B tries to cheat. And then it tries to revoke delegation so it's weight will not be used during voting for epoch N+1 weights. I assume that delegation for whole epoch N are obtained on the time of epoch N's start. The question is mostly when to snapshot delegation or allow dynamic changes

**↳ Ответ от [@gmorgachev](https://github.com/gmorgachev)** · *2026-04-02 05:45 UTC*

> > 2) Clarification needed: delegation “spending” vs “replication”
> > once p_from delegates to p_to for group_i, does p_from forfeit any direct voting/validation influence in that group for the epoch?
>
> In my opinion p_from must be able to either delegate its weight in group_i OR vote by itself in group_i. So if it delegated - it can't vote and also can't have MLNode in that group. If p_from decides to deploy MLNode in group_i, it'll cancel all its validation in group_i
>
> > does delegation affect only group validation voting, or also global governance / block production weight?
>
> Delegation affects only PoC validation inside certain group. Block production weight, governance decision weight and weight used for reward or tasks distribution are not affected
>  
> Delegation happens by key (p_from, p_to, model_id), separately per each model
>
> ------
>
> > 3) Scalability: O(G · N^2) validation is hard to see as sustainable
>
> **Just to clarify, the question is about PoC validation complexity or about chain itself? If about chain**
>
> > Even if bandwidth is okay, CPU sig verification, state handling, retries, and fork recovery will likely bottleneck — especially in 2–10 minute windows.
>
> Chain / block production itself doesn't depends on amount of model groups. All this data are used in the same mainnet. So there is almost no changes in retries, fork recovery, etc due to multi-model PoC (couple new fields in existing transactions `MsgPoCV2StoreCommit`, `MsgMLNodeWeightDistribution` and `MsgSubmitPocValidationsV2`)
>
> **If about PoC validation** 
>
> There were slot-based mechanism which were released in v0.2.10 upgrade https://github.com/gonka-ai/gonka/blob/main/proposals/poc/optimize.md
> It allows to change complexity to O(G * N * N_SLOTS), with recommended N_SLOTS=128
>
> The mechanism can be activated by voting for parameters, without upgrade 
>
> There is also random sampling of PoC artifacts to validate, that mechanism is already active

**↳ Ответ от [@gmorgachev](https://github.com/gmorgachev)** · *2026-04-02 05:52 UTC*

> > 5) “Independent hardware per group” looks like a soft requirement today
>
> Are you reference to part?
> > ..where POC procedure happens without re-deploy, for every model independently
>
> I think there is no need in any real requirements for specific hardware. The PoC procedure happens for all models simultaniously. So if host is able to submit artifacts for model A and model B at the same PoC and these artifacts are validated by another hosts, it assumes that this host had hardware to deploy both models. From my perspective it's not that much important if same hardware is presented in different groups as it's computation power / VRAM resources will be also splitted between groups. So it'll no power gain from such action, just participating in both groups, which is good for security

**↳ Ответ от [@gmorgachev](https://github.com/gmorgachev)** · *2026-04-02 06:05 UTC*

> > 4) Cap (Appendix A) doesn’t fully address group-local capture / fairness
> Cap limits a new group’s impact on global consensus weight (inflation / sudden dominance), but it doesn’t stop group-local capture, e.g. coordinated voting to mark honest participants invalid or monopolize inference revenue for a popular new model.
> >
> >Cap also depends on weight earned in other mature groups → strong path dependence / incumbent advantage (new entrants are structurally capped even if they’re best on the new model).
> >
> >Request: clarify what cap is intended to mitigate (global takeover vs group-local capture), and consider extra mechanisms for group-local correctness/fairness (challenge/appeal, slashing, auditability, etc.).
>
> The main mechanism to limit group specific dominance - is using of the total consensus weight in denominator. So, if total chain's weight is 1000 (from all groups), to pass validation inside the group_i, host will have to be approved by hosts with > 666 votingWeight (in initial text it was 50% that was my mistake, chain already uses 2/3)
> So, supermajority from the whole chain validated PoC artifacts / delegated their PoC votes
>
> Do you mean some specific group-local capture attack? 
>

**↳ Ответ от [@gmorgachev](https://github.com/gmorgachev)** · *2026-04-02 06:12 UTC*

> About the TEE, there is a separate thread where i fully agree that it's required :) 
> https://github.com/gonka-ai/gonka/discussions/951

### Комментарий 5 — [@unameisfine](https://github.com/unameisfine)

*2026-04-20 14:57 UTC*

## Implementation-level review from the current codebase

The high-level direction and the security analysis by @jacky6block are solid. I went through the current PoC implementation to identify concrete gaps the proposal would need to address. These are supplementary to the delegation/scaling concerns already raised.

---

### 1. Per-model weight storage is not supported by current data model

`MLNodeInfo.poc_weight` is a flat `int64` with no model context (`activeparticipants.proto:58`). The parent `EpochGroupData` supports subgroups via `sub_group_models` (`epoch_group_data.proto:19`), but the subgroup state is **in-memory only** — `epoch_group.go:111` stores them in a `map[string]*EpochGroup` that is rebuilt at runtime and never persisted on-chain.

For multi-model PoC, each participant needs per-model weight that survives restarts and is queryable by validators. Two options:
- Extend `MLNodeInfo` with a `model_id` field and store separate entries per model
- Create a new on-chain collection keyed by `(epoch, model_id, participant)` -> `poc_weight`

The second is cleaner — it avoids bloating `ActiveParticipant.ml_nodes[]` (which is already iterated in multiple hot paths like `model_assignment.go` and `epoch_group.go:55-78`) and allows independent pruning per model.

### 2. Parallel PoC GPU contention is under-specified

The proposal states *"PoC runs concurrently across all eligible groups within the same epoch"*. Currently, epoch phases are sequential: GENERATION -> VALIDATION -> INFERENCE (`types/params.go:165-183`, durations in blocks). Broker assigns each GPU to exactly one model during PoC (`model_assignment.go`).

With M concurrent PoCs:
- Each host needs **separate GPU(s) per model** — this is acknowledged ("requires separate hardware per group") but the broker has no mechanism to partition GPUs across PoC tasks. `StartPoCNodeCommandV2` targets a single model per node (`node_worker_commands.go:196-210`).
- **Validation window scales with M** — `WeightCalculator` (`chainvalidation.go:44-192`) processes validations sequentially per participant. With M models x N participants, validation latency grows linearly. Current `PocValidationDuration = 6 blocks` (~1 min) may be too short.
- **Inference degradation during PoC** — the proposal says validation and inference can run in parallel, but with all GPUs occupied by M parallel PoCs, inference throughput drops to zero during the PoC phase.

**Suggestion**: Consider staggered PoC — each model runs its PoC in a different block range within the epoch. This avoids GPU contention and fits the existing sequential phase model.

### 3. consensusKoeff governance circularity

The proposal defines `consensusKoeff_i` as a governance parameter. But governance voting power = consensus weight = f(consensusKoeff). A group whose members hold majority consensus weight can vote to increase their own `consensusKoeff`, concentrating power further.

The cap in Appendix A (capping weight by members' weight in *other* groups) partially mitigates this for new groups, but does not address the initial group (`group_Qwen3-235B-FP8` is explicitly exempt from the cap).

**Suggestion**: Bound `consensusKoeff` range per model (e.g., `[0.5, 2.0]` relative to a baseline), and require supermajority (67%) for changes — matching the BFT threshold already used for consensus.

### 4. Confirmation PoC not addressed

The proposal covers main PoC but does not mention Confirmation PoC (`confirmation_poc_v1.go:10-63`). cPoC is triggered during inference phase to verify nodes still have hardware — it is essential for liveness.

With multi-model:
- Should cPoC verify **all** models a host claims to serve? That multiplies cPoC load by G (number of groups).
- Or only the model currently being inferred on that host? Then hosts serving low-demand models skip cPoC entirely.
- Current cPoC uses `ConfirmationWeight` from `EpochGroupData` (`epoch_group_data.proto:47`) — a single field, not per-model.

This needs explicit design — cPoC is the defense against hosts that pass main PoC then deallocate hardware.

### 5. Settlement reward split between groups

The proposal defines `consensusWeight(p) = sum(consensusKoeff_i * pocWeight(group_i, p))` for consensus power, but does not specify how **bitcoin-style rewards** (the main economic incentive) split between groups.

Current settlement (`bitcoin_rewards.go`) distributes rewards proportional to global weight with confirmation weight capping. With multi-model:
- Are rewards pooled globally and distributed by aggregated `consensusWeight`? Then hosts in high-`consensusKoeff` groups earn disproportionately.
- Or split per-group first, then distributed within group? Then we need to define the split ratio (by `consensusKoeff`? by inference demand?).

This has major economic implications — it determines whether hosting a niche model is viable vs everyone piling into the highest-coefficient model.

---

### Concrete implementation path (suggestion)

Given the complexity, a phased rollout seems practical:

| Phase | Scope | Dependency |
|-------|-------|------------|
| **1** | Persistent per-model subgroups + per-model `poc_weight` storage | Proto + keeper changes only |
| **2** | Staggered per-model PoC generation + validation | Broker + epoch phase logic |
| **3** | Delegation mechanics (on-chain tx + voting power aggregation) | New msg types + validation changes |
| **4** | `consensusKoeff` governance + mandatory participation penalties | Governance module integration |

Phase 1 can ship independently and is useful even without delegation — it enables per-model weight tracking which the chain currently lacks.

---

Happy to help with implementation review or prototyping any of these areas.

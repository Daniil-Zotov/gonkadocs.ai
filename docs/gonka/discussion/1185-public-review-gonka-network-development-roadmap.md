---
title: "#1185 — [Public Review] Gonka Network Development Roadmap"
source: https://github.com/gonka-ai/gonka/discussions/1185
discussion_number: 1185
synced_at: 2026-06-15T18:13:27Z
---

> 🔄 **Авто-синхронизация:** из [GitHub Discussion #1185](https://github.com/gonka-ai/gonka/discussions/1185) каждые 6 часов. Прямые правки будут перезаписаны.

# [Public Review] Gonka Network Development Roadmap

**Автор:** [@paranjko](https://github.com/paranjko) · **Категория:** :bulb: Proposals · **Создано:** 2026-05-18 15:32 UTC · **Обновлено:** 2026-05-27 20:59 UTC

---

## 📝 Описание

Hi everyone,

Over the last month, I have been working on the **Gonka Network Development Roadmap**.

Last week, we had an initial working discussion with a group of active hosts and community contributors. Now I want to open the document for broader public review and invite everyone to comment and improve it.

The idea is simple: Gonka has already built a foundation of distributed GPU capacity. The next question is what we should build around this capacity to turn it into reliable inference infrastructure, real developer usage, and long-term network growth.

I suggest using the next week for public review and alignment with the community and the Core team. I would especially like to invite the Core team to review and comment on the document, because this roadmap should become a **shared picture of Gonka’s future** — not just a community-side draft.

If we can reach enough alignment, the next step would be to move this document toward a governance vote as a shared vision for Gonka’s future and a broad development roadmap for the network.

---

### Execution Framework

If this roadmap is accepted, I would expect two parallel directions to start from it:

1. **External Teams & Contributors:** Start preparing concrete proposals for specific tracks and projects. These proposals should define the actual scope, delivery plan, team, budget, timeline, KPIs.
2. **The Foundation Path:** Start a separate discussion around the legal and operational framework Gonka needs to support this shared vision for Gonka’s future.

> [!NOTE]
> This roadmap does not approve budgets, contractors, implementation details, or technical changes by itself. It should define the general direction first. After that, each track and project can be broken down into concrete subprojects and separate governance proposals where needed.

> Future changes to roadmap tracks and projects should go through the Gonka Improvement Protocol process: public discussion, community feedback, and then a governance proposal to update the relevant tracks and projects in the document.

---

[![Gonka_R1](https://github.com/user-attachments/assets/69e798ec-32fb-4da9-b042-61e44e77b57c)](https://docs.google.com/document/d/1wPXTM40CnXyd8Hz_dvf7H1n6KQDqjw0RzppMx92xR8U/)

[**Full document for review**](https://docs.google.com/document/d/1wPXTM40CnXyd8Hz_dvf7H1n6KQDqjw0RzppMx92xR8U/)

### Areas for Feedback

For now, feedback would be especially helpful on three points:

* **Roadmap sequencing and focus**
  > Which parts should become near-term proposals, and which should stay as longer-term roadmap directions?

* **Demand activation**
  > Which projects should move to concrete proposals first to unlock real developer demand and network usage?

* **Gaps and overlaps**
  > Are there missing tracks or projects? Are there areas that feel duplicated or unclear?


Please leave detailed inline comments in the Google Doc. General discussion can continue in this GitHub thread.

---

## 💬 Комментарии (5)

### Комментарий 1 — [@ore621](https://github.com/ore621)

*2026-05-19 02:22 UTC*

I am thinking about the Foundation (marketing too) - where could we discuss this aspect?

**↳ Ответ от [@paranjko](https://github.com/paranjko)** · *2026-05-19 13:27 UTC*

> I suggest discussing marketing questions in the dedicated marketing section of the roadmap (Track 11), as that would be useful for the roadmap review.
>
> Regarding the Foundation, I would keep it as a separate discussion for now. I think it makes sense to return to this topic once we see whether there is broader alignment around the roadmap direction.

### Комментарий 2 — [@aeoess](https://github.com/aeoess)

*2026-05-19 16:24 UTC*

On the developer and AI-agent access track, I think one gap is worth making explicit.

Gonka already has a strong answer on the supply side: proving Hosts run inference correctly, with validation and reputation behind it. The demand side is different. Once agents start calling the network, the open question is who is making the request, under what authority, and on whose behalf.

Today that is a Developer account or an API key. That works for normal API access. It gets thin once the caller is an agent, because a key can't express something like: this sub-agent may call only this model, for this purpose, until this time, and can't pass wider authority to another agent.

The second piece is beneficiary attribution. The token economics already answer who gets paid for supplying compute. The piece I don't see clearly yet is who the work was done for. Enterprise inference, billing, abuse handling and revenue share all need that answer, and the calling key doesn't encode it.

This is a request-layer concern, in front of validation, so it can be scoped separately from how Hosts are checked. The roadmap decision is whether caller identity, scoped delegation and beneficiary attribution belong in the agent-access track or are left to integrators.

Same direction as the #1008 reply. Those primitives, Ed25519 identity, scoped delegation with monotonic narrowing and attribution receipts, already exist open-source in TypeScript and Python. If the direction is useful for Gonka, the Go / Cosmos bridge from that thread still holds: signature verification, ante-handler wiring and a CosmWasm helper.

I can write up the agent-access piece for the doc if that would be useful.


**↳ Ответ от [@akamitch](https://github.com/akamitch)** · *2026-05-19 22:24 UTC*

> Better create one more gonka broker with such features

**↳ Ответ от [@gmorgachev](https://github.com/gmorgachev)** · *2026-05-21 12:58 UTC*

> Agree that it might make sense to implement first on broker side. Then may be devshard side. But should be probably out of mainnet

**↳ Ответ от [@a-kuprin](https://github.com/a-kuprin)** · *2026-05-21 18:36 UTC*

> devshard should have authentication. Thought on this.
>
> Big and important point is that current gonka model suppose that there is devshard per account. I'm thinkng on something like public `devshardctl` where anybody can pay just 1USD and get inference tokens.

### Комментарий 3 — [@gmorgachev](https://github.com/gmorgachev)

*2026-05-21 14:27 UTC*

@paranjko thanks for document. left some comments in google doc.

### Комментарий 4 — [@a-kuprin](https://github.com/a-kuprin)

*2026-05-21 18:32 UTC*

What is most important for roadmap - prioritization. And financial plan.

**My main point that tracks shouldn't be parallel with equal priority. Also there should be defined source of money GNK/USD for each purpose**

First of all GNK needs demand. Users should start use network for inferences in real cases.

If community pool with GNK will be directed for any outsource development, or equipment or anything like this, first action of a team who got the GNK will be selling it to get USDT. It will lead to lowering the price of GNK (as there is no liquidity at opposite side).
Financing projects with GNK should take this into account.

**Maybe we should provide vested GNK** (like a year of vesting or even 2 years). So this will motivate teams to do Gonka better, not just get some cash right now.

But anyway development should be financed in real cash. And there is 12m USDT in community pool that should be **targeted first to create demand**: multi-model, agents, wrappers, exchanges.

Marketing also shouldn't go before start of real demand of Gonka network. We already have seen how marketing raised GNK up to 4USD but people who bought it or mined for > 2USD are very hard to return back to gonka. When there is no real use first, we will get the pump, but strategically will lost most of people who heard about gonka during such marketing campaign.

It could be smart marketing. Like popularization of decentralized AI idea, where gonka not even mentioned before it is really ready and usable.

### Комментарий 5 — [@afedorov-bf](https://github.com/afedorov-bf)

*2026-05-27 18:43 UTC*

Hi, thank you for putting this together - it addresses many important and highly relevant topics. 

From our side, we would like to highlight what we believe should be treated as the highest priorities, and also add a few points that could further complement the roadmap.

**Bitfury's view on the Gonka AI roadmap**
**Date:** 27 May 2026

The network has successfully gone through its initial deployment phase, overcome the identified limitations, and our priority is now shifting toward expanding the user base and driving broader adoption.

**1. Demand activation should be the top priority**

We see several parallel streams that should drive this:

- **Accelerate onboarding to OpenRouter and similar aggregators** (Vercel AI Gateway, LiteLLM, Portkey, Groq and others).
- **Bring community management and marketing to a state-of-the-art level**. Actively promote Gonka AI to developers, miners, and other key ecosystem participants (exchanges, liquidity providers etc.) through industry conferences, events, and online activities with influencers.
- **Launch a developer credits programme** along the lines of what OpenAI and Anthropic do: give selected developers hundreds to thousands of dollars in API credits, so they can use and promote the platform for free.
- **Refresh the Gonka.ai homepage to remove entry barriers for developers and testers**. Right now, it isn’t obvious to a first-time user how to quickly start using the network’s services. A short "how to get started" guide, a broker list, and an API-access walkthrough placed directly on the home page would close this gap.

**Other priorities:**

**2. Speed up the Foundation track.** 

**The Foundation is critical**. It will allow to allocate funds in line with strategic priorities, incentivize ecosystem engagement, accelerate decision-making, and, most importantly, unlock the ability to hire senior leadership across sales, business development, and community management. Today there is simply no legal entity to bring such hires into, and that is the main blocker.

**3. Continue to invest into Institutional-grade ecosystem readiness, including:**

- **Integration with Tier-1 wallets** (Ledger and similar) to improve GNK visibility and readiness for institutional holders and DEX/CEX track.
- **Pass a security audit by a Tier-1 firm**.
- **Before going to DEX/CEX we need to develop the listing strategy** with industry expert and with the timing, target exchanges, and engagement with market makers and institutional-grade OTC desks (such as Nomura).

**4. Tokenomics and the reward model improvement.**

Today the tokenomics run mostly in manual mode, leaving potential capacity providers without a transparent view of expected rewards across different LLM models and hardware types. Compare this to Bitcoin mining, where operators know the current $/TH/s and can easily estimate their returns.

**Summary**

Gonka AI already has the core foundations in place: the technology, the supply, liquid reserves in the community pool, and the backing of serious investors. The next stage is focused on expanding the user base and actively attracting new customers to the network.

From Bitfury’s side, we are fully prepared to support these efforts through strategic customer introductions and our industrial expertise and credibility.

**↳ Ответ от [@paranjko](https://github.com/paranjko)** · *2026-05-27 20:59 UTC*

> Thank you, this is very helpful and broadly aligned with the roadmap direction.
>
> With this feedback in mind, I’ll proceed to the voting process. I hope you will support the proposal and continue contributing to the next stages after the roadmap vote, including the Foundation framework discussion.

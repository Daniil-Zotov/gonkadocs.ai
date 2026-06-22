---
title: "#836 — Gonka-native Coding CLI"
source: https://github.com/gonka-ai/gonka/discussions/836
discussion_number: 836
category: proposals
synced_at: 2026-06-22T05:32:10Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #836](https://github.com/gonka-ai/gonka/discussions/836) каждые 6 часов. 

# Gonka-native Coding CLI

**Автор:** [@Apha205](https://github.com/Apha205) · **Категория:** :bulb: Proposals · **Создано:** 2026-03-02 12:01 UTC · **Обновлено:** 2026-04-20 04:41 UTC

---

## 📝 Описание

We are an AI-focused open-source organization building infrastructure and applications around decentralized intelligence systems, and we have been early adopters in the AI space, positioning ourselves ahead of the curve by developing tools and experimental systems.

**Overview:**
We are developing a Gonka-native coding CLI— a developer tool that integrates directly with the Gonka network without relying on centralized intermediaries, while providing a seamless command-line experience that fits naturally into modern development workflows.
The goal is to make Gonka usable at the command line for developers building software — code generation, version control, refactoring, automation, analysis, powerful toolsets and advanced CLI experience — powered natively by the network.
This project is currently in its foundation phase.

**The Problem:**
Most modern AI coding tools sit on top of large centralized API providers rather than interacting with compute networks at the protocol level. This structure introduces unnecessary markups between the user and the actual infrastructure, increases the risk of service restrictions or sudden policy changes, and prevents builders from fully understanding how requests are processed. It also hides the underlying network from developers, meaning the infrastructure powering the intelligence remains invisible and underutilized. As a result, the ecosystem behind the compute layer does not gain direct recognition, measurable adoption, or meaningful developer engagement — even though it is the core engine delivering the capability.

**The solution:**
To realize the full potential of Gonka, builders must be able to communicate with the network at the protocol level rather than through third-party bridges. That means enabling local key control, handling value transfers natively, and sending model execution requests straight to the network infrastructure. Our goal is to engineer this integration layer correctly from the ground up, ensuring reliability, security, and scalability like we do in our other projects. 

Delivering this requires implementing local key custody mechanisms, cryptographic request authorization, low-level network request handling, and a system architecture capable of supporting sustained developer usage at scale. Instead of abstracting everything behind another provider, the CLI becomes the direct interface between developers and Gonka’s distributed compute layer.

With the gonka-cli we are building, the **Gonka ecosystem itself becomes visible and measurable**. Every developer who installs, configures, and integrates the tool into their workflow is actively engaging with Gonka’s infrastructure. **Usage is no longer indirect or hidden behind another brand** — it becomes explicit. Repositories, automation scripts, and developer environments begin to reference Gonka as part of their stack, increasing recognition organically within the engineering community.

This approach **transforms Gonka from being an underlying network into an actively used developer platform.** It strengthens technical credibility, increases ecosystem presence, and encourages builders to experiment, benchmark, and innovate directly on top of the infrastructure. Over time, this establishes a **stronger feedback loop** between network performance and developer needs, which ultimately benefits both the protocol and its contributors.

**Development Timeline:**
With the appropriate backing, we can deliver a developer-ready release within approximately one month. Financial support will allow us to move faster on infrastructure provisioning, core protocol integration, local key management systems, transaction handling components, and performance testing. It will also enable us to refine the developer experience through clear documentation, onboarding flows, and usability improvements to ensure the CLI is practical and production-ready.

We are requesting **$20,000** to accelerate infrastructure and deployment readiness.

Conclusion:
In conclusion, **we see this initiative not only as a technical integration but as a strategic growth lever for the Gonka ecosystem**. Each integration reinforces Gonka’s presence within the developer community.
In that sense, **this is as much a distribution and ecosystem expansion strategy as it is a tooling project** — a practical way to strengthen brand recognition while driving meaningful network adoption.

---

## 💬 Комментарии (3)

### Комментарий 1 — [@Aktum1](https://github.com/Aktum1)

*2026-03-03 09:28 UTC*

1. Coursor +  Gonka
2. VScode +  Gonka
3. Fork Mistral + Gonka

You can make part 3, right?
Is it the best solution right now? 

2. Rewords will be payed in GNK and maybe with westing period. Is it ok with you?

**↳ Ответ от [@Apha205](https://github.com/Apha205)** · *2026-03-04 23:37 UTC*

> Yes, we are currently using a fork of mistralai. We could also fork another Python-based coding CLI, depending on what you suggest.
>
> I'm not sure how the team plans to distribute rewards. Ideally, it would be better if the payment could be made in full rather than through a vesting schedule, but I'm open to discussing the terms.

### Комментарий 2 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-06 14:22 UTC*

The CLI layer you're describing maps directly onto Phase 6–7 of GiP #860
(Inference Quality Protocol): https://github.com/gonka-ai/gonka/discussions/860

Phase 6 adds protocol-native endpoints your CLI would consume without any
custom routing logic:

  GET /v1/models/profiles
    → per-model quality scores, specialization centroids, latency distributions
    → CLI picks the best model for the task automatically, from protocol data

  Response headers on every request:
    X-Suggested-Model: Qwen/QwQ-32B    ← protocol recommends based on task type
    X-Task-Archetype: code-review       ← detected from the prompt embedding
    X-Quality-Score: 0.82               ← node quality for this request
    X-Cache: HIT                        ← was this served from cache

  X-Inference-Feedback: +1/-1 header
    → CLI sends quality signal back to the protocol after each response
    → that signal improves routing for all future requests of the same type

Practical result: a CLI built on Phase 6 endpoints gets automatic model
selection, quality-aware routing, and feedback loop with zero custom logic.
The routing intelligence lives in the protocol, not in the CLI.

Worth coordinating on the endpoint contract so the CLI doesn't duplicate
what the protocol layer is building.

### Комментарий 3 — [@HavenCTO](https://github.com/HavenCTO)

*2026-04-20 00:52 UTC*

@Mayveskii @Aktum1 we are shifting focus from a coding cli harness, to a sovereign agent harness - https://github.com/Haven-hvn/haven-core we would like Gonka to be the first web3 provider supported by the harness - https://github.com/Haven-hvn/haven-adapters what is the timeline on approval?

**↳ Ответ от [@Mayveskii](https://github.com/Mayveskii)** · *2026-04-20 04:41 UTC*

> > RE
>
> Yo bro @HavenCTO , here's my telegramm ... Link me there, i'd like to talk. U write about is 60% done by me, i'm ready for share.

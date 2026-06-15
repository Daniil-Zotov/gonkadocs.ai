---
title: "#880 — Gonka Labs: How We're Building the Infrastructure for Gonka"
source: https://github.com/gonka-ai/gonka/discussions/880
discussion_number: 880
synced_at: 2026-06-15T18:13:40Z
---

> 🔄 **Авто-синхронизация:** из [GitHub Discussion #880](https://github.com/gonka-ai/gonka/discussions/880) каждые 6 часов. Прямые правки будут перезаписаны.

# Gonka Labs: How We're Building the Infrastructure for Gonka

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-03-12 21:40 UTC · **Обновлено:** 2026-03-12 22:08 UTC

---

## 📝 Описание

**Gonka Labs: How We're Building the Infrastructure for Gonka**

![telegram-cloud-photo-size-2-5303139431004969226-y](https://github.com/user-attachments/assets/de34893d-4761-4d49-b2a1-99344b7c681c)


That one Sunday evening was not exactly usual. I was preparing for the upcoming workweek and reading startup news when I stumbled upon something truly interesting. I immediately called my friend and business partner, Mike, and sent him a link to the video. It was an interview with the Liberman brothers by a well-known crypto podcaster.

The brothers' enthusiasm in that interview was astonishing \- it seems to be exactly what gave the project a massive boost that hasn't faded to this day. They talked about the distributed AI of the future called "Gonka," a name that cleverly unfolds in its Russian interpretation to mean "Race" \- a race for the future of AI that we are all trying to make fair and honest. A race to ensure that every user is not just a consumer, but a full-fledged participant in a global, equitable network.

Although the idea of decentralized AI is not new (there have been many projects attempting to make AI “distributed”), Gonka has leaped far ahead in bridging Web3 and AI very close together. What stood out to us was how genuinely and openly the founders spoke about the grim prospects of the future if centralized corporations become the sole providers of superintelligence. This is a monumental challenge we have to solve. And only together can we change the trajectory of AI development, putting it on the tracks of openness and fairness.

Going back to that Sunday evening, we wanted to dive deeper into the project. With our experience developing Web3, we were primarily interested in the blockchain side of things at first. That's where we’ve encountered our first problem: after sending a transaction, we couldn't find a convenient service to verify the transaction hash and its details.

**On December 12, 2025**, we launched [gonka.gg](https://gonka.gg), the first version of our blockchain explorer. Seeing strong feedback from the community, who truly loved our service, we began asking some very obvious questions. What tools and services do we ourselves, as Gonka users, lack the most?

_Thus began a grand journey and a new chapter in our lives, called **Gonka Labs**._

## Today, Gonka Labs is:

[gonka.gg](https://gonka.gg) — A Blockchain Explorer and Analytics platform for the Gonka network, which features:

1. A blockchain explorer for transactions, addresses, and blocks.  
2. Detailed analytics on GPUs, inferences, network participants, token holders, active governance proposals, and more.  
3. Convenient tools including:  
   1. A mining rewards calculator  
   2. A faucet for claiming GNK  
   3. A node tracking tools  
   4. An auto-configuration tool for nodes (beta)  
   5. A network data API provider (public, free API with 50k requests per day to anyone who registers)

Today, over 1,000 people visit [gonka.gg](https://gonka.gg) daily (and making over 1.1 million api requests daily), choosing it as the best and most comprehensive dashboard for Gonka. Our core mission for our flagship product remains unshakeable: to be the provider of the most complete and up-to-date information on Gonka, its blockchain, and the new data emerging every second.

[proxy.gonka.gg](https://proxy.gonka.gg) - OpenAi compatible cloud api for Gonka AI Inference (_**yes, 🦞OpenClaw is supported**_)

[GG Wallet](https://chromewebstore.google.com/detail/gg-wallet/elicodfmaffbndngiifcpmammicgjidd) - an open-source, native Chrome Extension Wallet for Gonka.

_We will dedicate a separate post to each product, but for now, we’d like to share more about our mission and how we can be useful to the growth of the Gonka ecosystem._

## Infrastructure Layer

It’s impossible to imagine the evolution of any blockchain without strong development teams surrounding it. Looking back at the growth of successful networks like Ethereum, their success would have been impossible without teams like Prysmatic Labs (whose software enabled the large-scale shift to PoS we witnessed), Consensys (whose contribution to Ethereum is invaluable), or Privacy & Scaling Explorations (PSE) (an entity born out of the Ethereum Foundation that researched Zero-Knowledge proofs).

Metamask, Etherscan, Uniswap, Aave, Lido \- the list goes on. Without these services, it’s hard to imagine the modern Ethereum ecosystem. All these products share one thing in common: they were not built by the Ethereum Foundation or the core team. They were born thanks to an open platform and an incentive structure that allowed thousands of developers worldwide to build their businesses and bring their ideas to life.

You can compare this to a city. The creators of blockchains are the architects, but the teams are the general contractors and foremen. Some handle the foundation (consensus clients), others the skyscrapers (applications), and others the underground utilities (protocols and networks). Without them, the city would remain nothing but a blueprint.

By saying this, we want to highlight just how crucial it is for a network to have motivated teams building tools that millions of people will eventually use, even if that scale isn't obvious right now. Often, it is just their belief in the shared vision and passion for their craft that drives these people forward.

**This is precisely how we view the mission of Gonka Labs**: creating clear and user-friendly tools that simplify life for Gonka's users. Our tools enable newcomers to easily onboard into the network, while providing veterans and power users with convenient instruments to interact with the project without getting bogged down in technical complexities.

## Our Principles

Our development principles are simple:

1. Ship fast.  
2. Listen to user feedback.  
3. Improve, and then improve again.

Following this framework, we have built over 10 projects for Gonka in just 3 months, and we keep on building. We aren’t chasing sheer volume; relevance is what matters to us.

If we see that a specific metric (for example, on a dashboard) is crucial for users (especially if multiple people are asking for it), it will be delivered the same day (or night). If a request is more resource-intensive \- like building the wallet \- we dive into deeper work, but we still try not to delay the MVP release. The faster we figure out what the user needs, the better.

## Open Source Approach

We believe in open source. Over 80% of the code for our projects is open, and any developer is free to use it. Furthermore, we are already seeing many people utilizing our products, installing them locally, and experimenting. We think this is genuinely amazing, and we invite more builders to join us on Gonka to help significantly contribute to the development of our products.

*You can view opensource projects at [gonkalabs.com](https://gonkalabs.com) ([git](https://github.com/gonkalabs))

## About the Team

As of today, there are three of us: Tim, Mike, and Artem. We are old friends, and all our professional experience is tied to online businesses and coding. For the most part, we have been building projects for clients (outsourcing), and we have long wanted to launch our own products aimed at a mass audience.

A lot has been accomplished. But we also see exactly how much still needs to be built. We see our future in continuously iterating on our current products and creating entirely new ones. At the same time, we plan to remain a compact, small team working full-time for the benefit of Gonka.

In subsequent posts, we will dive deeper into each product individually.

**Thank you for your attention!**

_Primary link: [https://gonkalabs.com](https://gonkalabs.com) 
Our Git: [https://github.com/gonkalabs](https://github.com/gonkalabs)_

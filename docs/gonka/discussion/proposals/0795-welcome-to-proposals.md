---
title: "#795 — Welcome to Proposals 👋"
source: https://github.com/gonka-ai/gonka/discussions/795
discussion_number: 795
category: proposals
synced_at: 2026-06-20T09:43:17Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #795](https://github.com/gonka-ai/gonka/discussions/795) каждые 6 часов. 

# Welcome to Proposals 👋

**Автор:** [@mtvnastya](https://github.com/mtvnastya) · **Категория:** :bulb: Proposals · **Создано:** 2026-02-24 07:27 UTC · **Обновлено:** 2026-04-16 06:17 UTC

---

## 📝 Описание

This is the space for discussing proposals for protocol improvements and the broader Gonka ecosystem development. If you have an idea that could make Gonka better, this is the place to share it.

**What belongs here**

- Protocol improvements: significant updates to core protocol design and long-term architectural direction
- External infrastructure proposals: third-party integrations, API clients, tooling, and ecosystem extensions
- Open problems: things that need research, design exploration, or community alignment before a path forward is clear

**How to write a good proposal**
Keep your proposal structured and include:
- Motivation - the specific problem you are solving
- High-Level Solution - your architectural approach
- Implementation Roadmap - specific milestones if the change is complex
- Open Questions - known unknowns to discuss during the community call
- Who you are - share context about your experience and expertise in the proposal thread. That could be your previous contributions to Gonka or any other reputable projects. If you represent a team or a company, mention it and link relevant work to help the community assess credibility and evaluate the proposal more efficiently.


Implementation timeline and bounty can also be proposed as part of the discussion.

**Next Steps**
Once your proposal is written, promote it on Discord and other platforms to gather feedback. 
React, upvote, and comment on others' proposals - this helps everyone understand what matters most and move toward implementation knowing what community needs.

---

## 💬 Комментарии (1)

### Комментарий 1 — [@Mayveskii](https://github.com/Mayveskii)

*2026-04-16 06:17 UTC*

@mtvnastya , Hi there, Nastya! 

🤗

*****
Thank you for the wonderful opportunity to be part of the protocol and community development process; it's incredibly valuable!

Who am I? I'm a newbie researcher. My idea is to follow the core philosophy of gonka and accelerate the development of qualitatively new solutions to user problems at all levels by sharing the results. This is most accurately achieved by leveraging the opportunities your protocol lifetime provides.

I calculated this in #859 & #860, but I understood that tests and mock data are of little interest to you without results. I decided to narrow my scope of responsibility in executing the idea to a minimum, demonstrating a standard of quality in one specific process: protocol development and patching. I developed a system consisting of several layers that fulfill the requirements of my specific goal: a server, MCP, and a management environment. What have I achieved? All my open and merged PRs are the result of this runtime. By the time the system patches were released, I didn't even fully understand these patches; I only double-checked everything 20 times before submitting them. What 100% proves is what people have already proven a million times before me: that a useful result like pep-8 should be reflected, distilled, and reused. It's worth noting that applying this system's quality matrix to my queries reduces patch times dramatically, which directly impacts the number of tokens you'll spend on infrastructure while repeating previously calculated steps, recalculating them over and over again. Here we can discuss how each of us uses LLM, but now imagine when we combine these efforts thanks to this runtime. It's hard for me to imagine the final result, but I can easily imagine that your use of this tool guarantees you scale.

What am I proposing? I'd like to finalyze it for source code and idea finally proposed in in the near future so we can review the work, use it, and suggest our own development vector for this system or its merger with the existing one. In my understanding, for applying a quality mask to a network, it would be optimal to have a number of node servers, CPUs, and GPUs to support this instance and ensure proper routing and improve the quality of work for participants. We're already seeing some of these changes everywhere today, but in a very fragmented and limited form. We shouldn't do the same thing all at once, and the sooner we move away from this and centralize our efforts, the more and faster we'll find high-quality results. If an ordinary system administrator has proven this today by patching 1,000 lines of useful code into your protocol, which is sometimes highly valued, then what will happen when we accumulate efforts and knowledge...? This was a great opportunity to prove myself, and I'm grateful for it. Now, to conclude... Proving the usefulness of the quality matrix is ​​only part of the results that can be gleaned from it. And the key to achieving the full potential of these results is scale. I was primarily thinking about how the protocol's advent would change the lives of everyone affected by it, and how to make this impact as effective as possible... The answer is obvious: produce a useful result. Conduct research and establish a standard, then share it and update it. This applies not only to code, but to any results we can bring to the gonka ecosystem. I'm most intrigued by science and research in the scientific field, namely, those that will allow ordinary people who don't have access to it today to obtain it and become completely autonomous, regardless of where they are.


-----------

Technical details for reference.
How these patches were produced: Every patch listed below was discovered through a structured pipeline: RAG indexes 52K+ code chunks with 5-signal hybrid search (semantic + comments + AST symbols + keywords + markdown), a semantic mesh of 205K+ invariant slots across 7 domains identifies recurring bug patterns (dominant pattern: error_swallowed_with_logwarn), and ai-reviewer with 20+ gonka-specific personas (chain_security, calculations, state-modified, consensus) verifies each finding before submission. From 45 initial hunt findings, 34 were eliminated as false positives after code-level verification, leaving 11 verified real bugs grouped into 6 PR blocks (A-F), all passing ai-reviewer.
Scalability — 3 options, building on #859/#860/#878:
1. Centralized hub (as proposed in #878): Each protocol node runs a binary-mesh instance. Patches, patterns, and invariants are distilled into mesh slots on each node. QualityMatrix tracks L0-L9 per node. Mesh slots sync across nodes — when one node discovers a pattern (e.g. error_swallowed_with_logwarn), all nodes benefit immediately. This is the natural evolution of #859 (L2 quality gate pipeline).
2. Federated mesh: Nodes don't share raw code — they share distilled invariant slots (pattern + fix + verification). Each slot is ~500 bytes. A 205K-slot mesh is ~100MB. Nodes query the federated mesh before submitting PRs, eliminating duplicate discoveries. This keeps proprietary data local while sharing the value.
3. API service: Host binary-mesh centrally. Protocol teams submit PR diffs via webhook. ai-reviewer runs 20+ personas, results posted as PR comments. Zero infra cost for the protocol team — we host, they consume. This is what we already do manually (ai-reviewer on every PR block before submission).
Complete PR track record (all produced by binary-mesh pipeline):
Merged:
- ethereum/go-ethereum#34038 — txLookupLock mutex leak in reorg()
- ethereum/go-ethereum#34039 — fix txLookupLock mutex leak on error returns in reorg()
Open (awaiting review):
- gonka-ai/gonka#909 — BLS context propagation + per-call timeouts
- gonka-ai/gonka#910 — BLS ProcessKeyGenerationInitiated idempotency guard
- gonka-ai/gonka#968/#969/#970 — InjectParams error propagation, graceful shutdown, ErrInsufficientFunds regex
- gonka-ai/gonka#1013 — subnet escrow fund loss (APPROVED by Doog-bot534)
- gonka-ai/gonka#1014/#1015 — SubnetHostEpochStats + settlement overflow guards
- gonka-ai/gonka#1017 — bitcoin supply-cap overflow
- gonka-ai/gonka#1071-#1076 — 6 verified bug blocks (error propagation, zero tokens, nil epoch, PoC V2 storage, claim rewards PoC overlap, dynamic pricing) — all passing ai-reviewer
Closed superseded:
- gonka-ai/gonka#1016 → Issue #1067 (ClaimRewards payout error handling)
- ethereum/go-ethereum#34665 — pending replace eligibility check (open)
Issue:
- gonka-ai/gonka#1067 — ClaimRewards error handling (commit ec5e453 predates Doog-bot534 #1051 by 10 days)
Foundational work:
- gonka-ai/gonka#859 — semantic cache L2 quality gate pipeline (merged)
- gonka-ai/gonka#878 — semantic cache extending (open, references #859/#860)

-----------

Summary  findings time spent - 12 hours. Summary dev time spent - 3 months.


Thank you again for such a wonderful opportunity. If I hadn't seen Libermans on YT three months ago, I probably wouldn't have come to this. So, the idea is yours )) And the result is shared. Thank you, guys. I hope you find my work relevant. I'd love to hear your feedback.
*****

---
title: "#1345 — Network Documentation"
source: https://github.com/gonka-ai/gonka/discussions/1345
discussion_number: 1345
category: proposals
synced_at: 2026-06-18T05:03:09Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1345](https://github.com/gonka-ai/gonka/discussions/1345) каждые 6 часов. 

# Network Documentation

**Автор:** [@heitor-lassarote](https://github.com/heitor-lassarote) · **Категория:** :bulb: Proposals · **Создано:** 2026-06-16 17:42 UTC · **Обновлено:** 2026-06-16 17:45 UTC

---

## 📝 Описание

Hello, everyone. We’re a team at [Serokell](https://serokell.io/), and after reading the [Gonka Community Network Roadmap](https://docs.google.com/document/d/1wPXTM40CnXyd8Hz_dvf7H1n6KQDqjw0RzppMx92xR8U/edit?pli=1&tab=t.0#heading=h.wt1svxjuy5ac), we wanted to discuss Track 4, Project 3, entitled “Network documentation”, which has the following description as of 09-06-2026:


---

A structured documentation system for hosts, developers, external contributors, and ecosystem teams.

The documentation should have a clear canonical source in a public GitHub documentation repository, where changes can be reviewed, versioned, and updated through PRs.

This project should be treated as an ongoing documentation maintenance process, not a one-time writing effort. It could support a documentation or technical writing team responsible for keeping the documentation up to date after protocol upgrades, incidents, recurring support questions, and operational changes.

**Metrics:**

- PRIMARY: network reliability and trust.
- SECONDARY: lower support burden; faster host onboarding.

**What this gives the network:**

Gonka gets a clear, maintained, and versioned knowledge base. Hosts and external teams get fewer ambiguous instructions and a safer path through upgrades and operational changes.

---

We would like to offer a team to work on the structured documentation. In particular, we’d like to offer the following improvements to the existing documentation:

1. Implement an AI agent to answer docs-related questions:
    1. There are multiple choices for the ownership/funding of the agent:
        1. Community-funded (community pool): ongoing budget for hosting and maintenance.
        2. Core-team founded (gonka-ai): treated as part of “docs as infrastructure”.
        3. Vendor-funded (Serokell): we’d fund it during the initial phase, with a handover plan to the community.
    2. Hosting options:
        1. Self-hosted on Gonka infra: requires ops ownership.
        2. Hosted on Serokell infra: we’d fund it during the initial phase, with a handover plan to the community.
        3. Hosted via Gonka inference-based network: this is mostly speculative, subject to feasibility, budget, and ops validation. Requires an inference budget on the network/provider.
    3. Model choice:
        1. Start with a cost-effective model: quality, latency, and price trade-off.
        2. Keep models RAG-based (Retrieval-Augmented Generation): ensure the docs (and possibly the Gonka repo itself) are used as source of truth.
        3. Add an evaluation set (50–100 real questions) to measure answer quality.
            1. Use a stronger model to judge the answers based on predefined expected answers, with average Pointwise accuracy with several estimates (using question, answer, and documentation fragment for judging).
                1. To fight bias, we may feed the original fragment along with question and answer, and to fight variation, one plan is to run the same scoring process several times on each test and take the average of the scores.
            2. Assert that the agent finds the correct documentation pages for expected answers.
            3. Consider metrics for finding the correct documentation, such as Recall@k, Hit@k, Mean Reciprocal Rank (MRR), etc..
    4. Protection against harmful and unrelated requests:
        1. For now, we don’t plan any access to internal tooling, apart from searching in the docs. We don’t see a way that the user could create harmful prompts.
        2. As for unrelated questions, we’ll implement detection and protection against prompt injections.
        3. However, prompt injection is a soft restriction that cannot be fully prevented. For hard restrictions, we plan other criteria, such as maximum amount of requests per minute, maximum allowed input and output tokens, retrieval budget (to prevent a retrieval explosion if a query matches too many documents), conversation history budget (do not feed the entire conversation history if it grew too large, perhaps replacing it with a summary), etc..
2. Versioned documentation. There might be more than one network version being used at a given moment. A switch allowing choosing to read the documentation for a specific version would aid audiences who are not on the same network or software version at the same time.
    1. Gonka appears to have a maintained testnet, but accessibility may be controlled/request-based. So versioned docs may account for not just the version, but also the network.
    2. One possible plan is to align docs version with GitHub release tags/branches. The documentation for the version should be fetched based on the tag. Network-specific versioning may also be needed.
    3. The maintainers and developers should coordinate efforts to keep the documentation up-to-date. One option to aid is to use an agent in `gonka-docs` to monitor recent diffs in the `gonka` repo against the main branch in which `gonka-docs` should be changed. This option, however, requires credits, and for large diffs (common in `gonka`) may produce mediocre results. We propose to make an experiment and test how this would go.
3. Automatic translation to other languages. Following the AI agent improvement, the Gonka docs are currently written in English and Chinese. Using the English version as the source of truth, we may add a third option allowing for automatic translation to other languages.
    1. Every translated document will link to the original English document.
    2. Testing will be done with the model judge using representative language groups (Russian, Chinese, etc.).
        1. What constitutes representative languages of the Gonka community should be discussed further.
        2. In addition, we may provide the LLM with a semi-manually curated set of terms and their translations for more consistent translations and higher translation accuracy. This will require input from native human translators to validate this set for a target language.
4. Metrics and telemetry for docs searches and page hits.
    1. Documentation usage:
        1. Views per page: track the top entry points and critical paths.
        2. Time spent on page and scroll depth: detect pages with quick answers vs. “read but confused”.
        3. Exit rate and next-page navigation: see where users go next and spot dead ends.
    2. Search telemetry:
        1. Search queries (anonymized): discover missing topics and confusing terminology.
        2. Zero-result searches: detect biggest gaps to fill.
        3. Query → clicked result: measure search relevance and navigation quality.
    3. Quality tracking:
        1. “Was this helpful?” votes + optional reason tags: find outdated or unclear pages.
        2. Broken links/404s detection: catch regressions early and automatically.
        3. Version mismatch signals: find users landing on wrong versions, possibly tracked by referrer.
    4. Support:
        1. Links to GitHub issues/discussions: allow redirecting users to the GitHub issue tracker or discussions from the docs.
    5. Hosting:
        1. As with the AI agent, the hosting may be done with Gonka infra, or in Serokell infra during an initial phase with a later handover plan to the community.
5. Audit, and resolve the proposed issues/discussions/PR comments regarding documentation in the Gonka repository, provided in “Documentation-Related Issues, PRs, and Discussions” below. They will be used as the input for docs improvements.
6. Discover and migrate relevant documentation from the code repo into the docs repo.

The schedule to support the above plan might look like this:

1. Create the infrastructure and implement metrics and telemetry for the documentation.
2. Implement the versioned docs feature and write tests for it.
3. (Re)write documentation based on the proposed list of issues and discussions.
4. Discover and migrate relevant documentation from the code repo into the docs repo.
5. Develop and integrate the AI agent using the knowledge [gonka-ai/gonka-docs](https://github.com/gonka-ai/gonka-docs) repository and add it to https://gonka.ai/docs/ by introducing a new button, such as “Ask Agent”.
6. Create the evaluation set and test the quality of the answers.
7. Using the AI agent implemented earlier, support a new toggle besides English and Chinese such as “Other (auto-translate)”.
8. Create evaluations for the translated content.
9. Write a plan clearly detailing how to hand these new features to the Gonka community.
10. Ongoing maintenance is the target model. If the funding is limited, the initial scope may be a one-time bootstrap plus the handover plan.

<details>
<summary><h2>Documentation-Related Issues, PRs, and Discussions</h2></summary>
Checked June 16, 2026. The following are the PRs, issues, and discussions that may support the documentation, by demonstrating gaps, outdated content, or content that may be added to it.

Relevant PRs:

- https://github.com/gonka-ai/gonka/pull/1327: **docs: add Chinese (zh) translations for key documentation**
    - Unmerged, proposed in the wrong repo.

Relevant issues:

- https://github.com/gonka-ai/gonka/issues/1331: **How to obtain a broker API key for node4 (or documentation on the broker onboarding process)?**
    - Open issue requesting documentation.
- https://github.com/gonka-ai/gonka/issues/1319: **Self-serve (no-broker) flow is documented as working but returns 401 "model requires an API key" — I want to spend my own GNK directly**
    - Requests code changes, but suggests the docs could be clearer.
- https://github.com/gonka-ai/gonka-docs/issues/1149: **Run Gonka documentation translation on Gonka**
    - One of our proposed work points regarding automatic translation.
- https://github.com/gonka-ai/gonka/issues/1032: **Question: is there a path for consumer-grade 16 GB GPUs to participate as lightweight Host nodes?**
    - Issue was converted to a conversation, limited to collaborators, and has no answer.
- https://github.com/gonka-ai/gonka/issues/447: **Node Registration Does Not Update After Migration (API stuck using old on-chain config)**
    - Issue suggests migration gaps; commenter suggests the issue deserver clearer documentation.

Discussions (n.b.: we’d ask for permission from the authors to include their work in the docs):

- https://github.com/gonka-ai/gonka/discussions/1141: **IBC USDT Withdrawal Guide**
    - User-written guide that could be migrated to the docs.
- https://github.com/gonka-ai/gonka/discussions/1116: **HOW-TO: Create and Submit a Governance Proposal on Gonka**
    - User-written guide that could be migrated to the docs.
- https://github.com/gonka-ai/gonka/discussions/796: **Are there plans to add prompt-level confidentiality for hosts?**
    - Docs could clarify the current state of TEE.The documentation should have a clear canonical source in a public GitHub documentation repository, where changes can be reviewed, versioned, and updated through PRs.
</details>

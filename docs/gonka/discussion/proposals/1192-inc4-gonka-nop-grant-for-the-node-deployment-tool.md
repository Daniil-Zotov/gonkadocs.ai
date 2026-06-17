---
title: "#1192 — INC4 | Gonka NOP - grant for the node deployment tool"
source: https://github.com/gonka-ai/gonka/discussions/1192
discussion_number: 1192
category: proposals
synced_at: 2026-06-17T11:18:27Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1192](https://github.com/gonka-ai/gonka/discussions/1192) каждые 6 часов. 

# INC4 | Gonka NOP - grant for the node deployment tool

**Автор:** [@rwxr-xr-x](https://github.com/rwxr-xr-x) · **Категория:** :bulb: Proposals · **Создано:** 2026-05-19 10:51 UTC · **Обновлено:** 2026-05-19 10:52 UTC

---

## 📝 Описание

# Gonka NOP - grant for the node deployment tool

A CommunityPool funding request covering delivered work on gonka-nop, ongoing operator support, and continued development of the tool.

## TL;DR

INC4 proposes a 50,000 USDT allocation from the CommunityPool for gonka-nop (Node Onboarding Package), a CLI tool for deploying and maintaining Gonka nodes. The tool is already built, released under the MIT license, and in active use by some operators on mainnet — it is not a proposal to build something new, but a request to fund work that has already produced a working tool with its own users. The grant covers three areas: the work already delivered, ongoing support for NOP users, and continued development of the tool. The grant is paid in USDT rather than the native GNK token, and is structured as a single transfer without vesting or milestone tranches. There is no detailed budget breakdown and no milestone schedule: allocation of effort across the three areas remains at INC4's discretion, with the public repository serving as the basis of accountability.

## What is gonka-nop

Gonka NOP is a CLI that reduces deploying a Gonka node to a single operation. The tool inspects the state of the target server, installs missing dependencies, brings up the required components in the correct order, and registers the node with the network. Gonka-specific details are encoded inside the tool and updated alongside network releases, so the operator does not have to track them release by release. This includes image versions, vLLM configuration tuned to the specific GPU model present on the host, registration parameters expected by the chain, and readiness conditions a node must satisfy before PoC and cPoC rounds. This is what separates NOP from a docker-compose bundle: it carries Gonka's operational model, not just its container set. The main deployment topologies are supported: a standalone Network Node, a combined configuration with the ML Node on the same machine, and a distributed setup with multiple ML Nodes on separate hosts behind a single Network Node.

The tool addresses two distinct audiences. For operators without deep DevOps experience, it lowers the entry barrier: renting a server with a suitable GPU and stepping through an interactive wizard is enough, with no need to work through GPU drivers, the interaction between layers, or vLLM configuration files by hand. The wizard surfaces the small set of choices an operator actually needs to make — topology, hardware profile, network endpoints — and resolves the rest from defaults that track current network requirements. For experienced administrators, the same binary provides repeatability: most prompts in the wizard have an equivalent command-line flag, the binary runs non-interactively when configuration is supplied up front, and the resulting invocations integrate cleanly into Ansible playbooks and other automation systems. The same flags drive both initial deployment and in-place upgrades, so the path from a fresh installation to a node running the latest release is the same single command across an operator's fleet. Deploying dozens of nodes ends up roughly as complex as deploying one, which matters for any operator running a fleet rather than a single instance.

- Repository on GitHub: https://github.com/inc4/gonka-nop
- Documentation: https://github.com/inc4/gonka-nop/blob/main/README.md
- Live walkthrough on YouTube (by Gonka.Top@Mitch): https://www.youtube.com/watch?v=1t9GEMN92Vo

## The deployment problem

Deploying a Gonka node is a multi-step process involving several heterogeneous components: GPU drivers, the container runtime, and the various Gonka components themselves. Each layer has its own requirements for versions, ports, resources, and configuration order. The interfaces between them are unforgiving — a mismatch in any one place rarely shows up during installation; it surfaces later, once the node is expected to serve PoC and cPoC rounds. Requirements also shift periodically with network releases: new models replace older ones, image tags move, vLLM parameters get retuned, additional GPU families enter the supported set, and the specific combination of versions that constitutes a valid node at any given moment is not the same combination that was valid two releases earlier. Each shift touches a different subset of layers, and the operator carries the cost of working out which subset that is.

The combination of a Cosmos SDK chain with a production ML inference stack under the same operator is uncommon. The operational knowledge needed to manage both — chain-level concerns like consensus participation and slashing, alongside infrastructure concerns like GPU memory layout and model serving — is not widely available outside specialized teams.

The cost of getting it wrong falls on the operator. Missed PoC and cPoC rounds, a lagging Network Node, or version mismatches between components can all result in lost rewards and possibly jail. Time spent diagnosing incidents does not come back. For an experienced administrator this is tractable but time-consuming. For an operator new to Cosmos SDK networks, the requirement stack is in practice impassable without external help. NOP removes that part of the workload from the operator.

## Proposal

The funding request reflects the structure of the work itself: what has already been delivered, what is needed to keep it running, and what comes next. The grant covers three corresponding areas.

**Retroactive compensation for development already delivered.** The current version of NOP is a working tool with an active user base among mainnet operators. INC4 took on the initial development as a contribution to the network. The retroactive portion of the grant settles that delivered work.

**Support for NOP users.** INC4 triages incidents, helps with diagnostics during deployment and operation, responds in DevOps chats, and ships patches and updates aligned with new Gonka releases. This workload is recurring rather than one-off — it returns each time the network changes. The grant commits INC4 to maintaining the tool under the same model.

**Continued development.** New capabilities, broader coverage of deployment scenarios, further reductions in the entry barrier. Concrete tasks are shaped in dialogue with operators and the Gonka core team, and tracked publicly in the repository. The proposal deliberately does not pre-commit to a feature list: priorities need to remain responsive to what the network actually requires as it evolves.

## Grant terms

The amount is 50,000 USDT, paid as a single transfer, without vesting and without milestone tranches. Work is conducted in the open: code, releases, the issue tracker, and the changelog all live on GitHub and are accessible to anyone — operators, the core team, and DAO participants. No additional reporting structure to the DAO is proposed: the public repository is the report. Anyone — community member, validator, or core contributor — can inspect the state of the work at any point after the grant is approved, without having to ask.

The proposal was published for community discussion in advance of this on-chain submission. The discussions remain open at:

- https://vote.gonka.vip/tenders/2cbbe98e-ceff-4f09-a1cd-e8d370e97fde
- https://gonkavote.com/proposals/6

## Why this matters for the network

This grant is about how easily the network can absorb new operators. Today most Gonka operators are people with the experience to deploy and run a node on their own. That works while the network grows through its core, but at some point growth runs into the entry barrier for everyone without that background. NOP removes that barrier: a new operator doesn't have to understand the internals, and an experienced operator gets the automation to manage a fleet of nodes.

The network changes with every release — new models, updated images, adjusted parameters. If the tool doesn't keep up, it quickly becomes a snapshot of the past, and the entry barrier comes back. The grant funds exactly that work: keeping NOP current release after release.

The grant covers not just the product, but the work of keeping it current. Node deployment should stay simple as the network evolves, and the infrastructure layer shouldn't become a bottleneck to growth.

In mature networks, deployment tooling is treated as part of the protocol surface rather than a side project, maintained at the same cadence as the chain — the alternative is an operator set that thins out with every upgrade, as operators who cannot keep pace with each release quietly fall behind and stop participating. A network's long-term resilience is bounded by the breadth of operators who can keep their nodes correct through change, not by how many were able to set one up in the first place.

## INC4

- Website: https://inc4.net
- GitHub: https://github.com/inc4

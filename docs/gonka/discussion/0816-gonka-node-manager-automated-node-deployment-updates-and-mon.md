---
title: "#816 — Gonka Node Manager — Automated Node Deployment, Updates, and Monitoring"
source: https://github.com/gonka-ai/gonka/discussions/816
discussion_number: 816
synced_at: 2026-06-15T18:13:41Z
---

> 🔄 **Авто-синхронизация:** из [GitHub Discussion #816](https://github.com/gonka-ai/gonka/discussions/816) каждые 6 часов. Прямые правки будут перезаписаны.

# Gonka Node Manager — Automated Node Deployment, Updates, and Monitoring

**Автор:** [@ochenUmnayaKatyshka](https://github.com/ochenUmnayaKatyshka) · **Категория:** :bulb: Proposals · **Создано:** 2026-02-26 11:49 UTC · **Обновлено:** 2026-03-09 12:33 UTC

---

## 📝 Описание

## Executive Summary

Running Gonka nodes currently requires manual CLI-based installation, configuration, and ongoing maintenance. For experienced operators, initial setup typically takes several hours per node. For less experienced participants, the process often stretches to one or two days — or results in abandonment before a node is ever launched.

This friction actively filters out potential operators, concentrating power among technically advanced users and slowing organic decentralization.

Gonka Node Manager requests **$80,000 USD equivalent** from the Community Pool to build a production-ready MVP that automates node deployment, updates, and monitoring.

> Note: On-chain governance vote (Community Pool spend) will be submitted as a separate transaction once the contract is deployed. This issue tracks the technical proposal and implementation plan.

---

## Problem Statement

Current node operation requires:
- Manual CLI setup taking hours to days per node
- SSH access and server-level configuration for every update
- No automated monitoring or health visibility
- No streamlined process for attaching ML nodes to network nodes

This effectively limits participation to a narrow group of technically advanced users, concentrating operational power and slowing organic decentralization.

---

## Proposed Solution

Gonka Node Manager — a unified tool that allows node operators to:

- Deploy network and ML nodes in a consistent, automated way
- Keep nodes up to date without manual intervention
- Attach and operate ML nodes alongside network nodes
- Observe basic node status and health without logging into servers

The system operates on top of user-provided infrastructure (physical or virtual) and fits naturally into a decentralized network model.

---

## Architecture Overview

### Components

| Component | Role |
|---|---|
| **Control Plane (Web UI + API)** | User auth, node management, issues tasks to agents, displays status |
| **Node Agent (host daemon)** | Installed once per host, manages local Docker Compose stacks, communicates outbound only |
| **Stack Bundles** | Deployment definitions: services, ports, health checks, references to official Gonka images |

### Core User Flows

1. **Node bootstrap** — user adds node in UI → agent installed once on server → node available
2. **Deployment & updates** — automated via preconfigured stable release path, no user intervention
3. **Network/ML attachment** — ML node attached to network node, firewall rules applied automatically, connectivity validated
4. **Warm key workflow** — warm key generated locally on node, only public key exposed, cold-key signing stays with operator

---

## Security Model

- SSH access stays entirely under operator control — Control Plane never stores credentials or uses SSH
- No inbound management ports required on nodes
- Agent executes only approved, predefined operations — no arbitrary remote commands
- Stack bundles verified before application
- Cold keys never leave the operator's device

This preserves node sovereignty and aligns with Gonka's decentralization principles.

---

## MVP Scope

### Included

- Host-level node agent
- Deployment of network and ML nodes
- Automatic updates via preconfigured stable release path
- Network/ML attachment with firewall automation
- Warm key generation and binding workflow
- Basic status and health reporting

### Explicitly Out of Scope

- Advanced metrics and observability stacks
- Arbitrary remote command execution
- Manual version selection or multiple update channels
- Role-based access control
- Automated rollback mechanisms (except those recommended by Gonka developers)
- On-chain enforcement of updates
- Remote administrative access

---

## Implementation Plan

### Phase 1 — MVP Installation (45–50% of budget)
**Outcome:** Network and ML nodes can be deployed and operate end-to-end
- Node agent: deploy, attach, health — 160–200h
- Control Plane core APIs — 80–100h
- Architecture & core design — 40–60h
- Minimal UI — 40–60h
- Integration testing — 40–60h

### Phase 2 — MVP Auto-Updates (20–25% of budget)
**Outcome:** Running nodes update themselves automatically
- Bundle versioning & signatures — 40–60h
- Agent update logic — 40–60h
- Control Plane update coordination — 20–30h
- Update testing — 20–30h

### Phase 3 — MVP Monitoring (15–20% of budget)
**Outcome:** Operators can observe node status and health
- Agent health reporting — 30–40h
- Backend status aggregation — 20–30h
- UI status views — 40–50h

### Phase 4 — Stabilization & Technical Debt (10–15% of budget)
**Outcome:** Stable, documented, production-ready MVP
- Bug fixes and edge cases
- Security hardening
- Documentation
- Final testing

**Total estimated effort: 650–880 engineering hours**

---

## Budget

**Requested: $80,000 USD equivalent** (one-time, from Community Pool)

Funding released in stages tied to phase completion. Cost overruns covered by the team at its own expense — no retroactive compensation requests will be made.

---

## Accountability

- All progress tracked in a single public GitHub repository
- `progress.md` updated after each phase with written summary, deliverables, and artifact links
- Code, docs, release notes, and demo materials committed per phase
- Repository URL announced immediately after proposal approval

---

## Expected Outcome

- Easier onboarding for new node operators
- Increased number of independent nodes
- Reduced downtime caused by manual configuration
- Stronger and more sustainable decentralization of the Gonka network

---

## 💬 Комментарии (4)

### Комментарий 1 — [@Aktum1](https://github.com/Aktum1)

*2026-02-27 22:43 UTC*

Hey! Have you checked out what these guys have already built in this direction?
https://gonka.gg/node-setup

What do you think about their implementation?
<img width="1562" height="649" alt="image" src="https://github.com/user-attachments/assets/dcaef2ca-eb9e-444c-8b96-04aabeaab4db" />


**↳ Ответ от [@ochenUmnayaKatyshka](https://github.com/ochenUmnayaKatyshka)** · *2026-03-04 13:10 UTC*

> Our proposal focuses on a different set of operational requirements:
>
> Lifecycle Management: Beyond the initial install, we are building a system for automated updates and configuration changes without requiring manual SSH sessions for every release.
>
> Centralized Visibility: The goal is to provide a dashboard where the status of both Network and ML nodes can be monitored in one place, rather than checking individual server logs.
>
> Orchestration Logic: We are automating the connectivity and firewall rules needed to attach ML nodes to Network nodes, which currently involves several manual steps.
>
> Essentially, while a script handles the deployment process, our tool is designed to manage the node's long-term operation and connectivity automatically.

### Комментарий 2 — [@Aktum1](https://github.com/Aktum1)

*2026-02-27 22:52 UTC*

Also, take a look at this node monitoring Telegram bot: @GonkaHubBot.

**↳ Ответ от [@Aktum1](https://github.com/Aktum1)** · *2026-02-27 22:59 UTC*

> I’ve been trying to set up my node for a month now.
>
> It’s not exactly a simple setup — 8× A100 40GB. After one of the recent code changes, these GPUs were practically restricted. But I’ve already paid for the server for a month, so now I’m using it to fully test and fine-tune the node deployment process.
>
> I even got a paid Cursor subscription specifically for this. Really hoping I’ll manage to get everything running properly.
>
> If I succeed, I’ll definitely share the full experience with others.
>
> That said, I’m not entirely sure whether node setup can realistically be turned into a “one-click service.” There are so many edge cases and нюances — can a service really account for all of that?
>
> To me, a model based on an AI agent that deeply understands the infrastructure and has access to all up-to-date documentation sounds more scalable than building a rigid setup service.
>
> But I could be wrong.
>
> At the end of the day, we’re basically trying to solve the same problem — just using different tools.
>
> By the way, I’m documenting my entire journey in the Knowledge Base:
> https://gonka-data-base.gitbook.io/gonka-data-base-en/hosts/node.-testing
>
> Maybe some of it could be useful for your project.

**↳ Ответ от [@ochenUmnayaKatyshka](https://github.com/ochenUmnayaKatyshka)** · *2026-03-04 13:10 UTC*

> The 'one-click' challenge is exactly why our proposal moves away from simple scripts toward a Node Agent architecture.
>
> A static setup often fails when hardware or dependencies change. Our approach uses the Agent as a local management layer to handle the environment, Docker stacks, and connectivity. The goal of this architecture is to provide a system that accounts for infrastructure nuances and maintains node operation through updates, rather than just performing an initial installation.
>
> The project is designed to automate these manual processes and handle the edge cases that typically arise during long-term node maintenance.

**↳ Ответ от [@Mayveskii](https://github.com/Mayveskii)** · *2026-03-05 12:58 UTC*

> > Проблема "работы в один клик" — именно поэтому в нашем предложении мы отходим от простых скриптов в пользу архитектуры Node Agent.
> > 
> > Статическая настройка часто дает сбой при изменении оборудования или зависимостей. Наш подход использует агент в качестве локального уровня управления для обработки среды, стеков Docker и подключения. Цель этой архитектуры — предоставить систему, которая учитывает нюансы инфраструктуры и поддерживает работу узлов при обновлениях, а не просто выполняет первоначальную установку.
> > 
> > Проект призван автоматизировать эти ручные процессы и обрабатывать нестандартные ситуации, которые обычно возникают при длительном обслуживании узлов.
>
>
>
>
> Unified operator stack: delivery, control, reproducibility
> Combining Node Manager (#816) and Prometheus exporter (#840) with a thin orchestration layer (e.g. Airflow, optionally n8n) gives a single stack that is not that heavy but covers the main operator needs: delivery, control, and reproducibility.
> Delivery: Deploy and update nodes via Node Manager; no need to hand-hold each host.
> Control: Same metrics (block height, POC weight, status) for everyone via the exporter + Prometheus + Grafana — hosts see what we see.
> Reproducibility: Airflow turns procedures into DAGs: health checks, update windows, report generation, cleanup, even ticket/workflow-style steps (e.g. “after alert → create task → run remediation”). Any scenario you can script becomes repeatable and auditable.
> So you get one place for “how we deploy”, “how we monitor”, and “how we react and rerun”. The stack is modular: minimal is exporter + Prometheus + Grafana; Node Manager and Airflow (and optionally n8n for event-driven bits) add on top for those who want automation and reproducibility.
> Worth doing? Yes. It directly tackles “hosts can’t easily configure and monitor like we do”: same tooling, same visibility, and the same ability to encode and replay scenarios instead of ad‑hoc SSH and one-off scripts. If the community wants to invest in operator experience and reproducibility, this is a concrete way to get there.

**↳ Ответ от [@Mayveskii](https://github.com/Mayveskii)** · *2026-03-06 14:23 UTC*

> > > Проблема "работы в один клик" — именно поэтому в нашем предложении мы отходим от простых скриптов в пользу архитектуры Node Agent.
> > > Статическая настройка часто дает сбой при изменении оборудования или зависимостей. Наш подход использует агент в качестве локального уровня управления для обработки среды, стеков Docker и подключения. Цель этой архитектуры — предоставить систему, которая учитывает нюансы инфраструктуры и поддерживает работу узлов при обновлениях, а не просто выполняет первоначальную установку.
> > > Проект призван автоматизировать эти ручные процессы и обрабатывать нестандартные ситуации, которые обычно возникают при длительном обслуживании узлов.
> > 
> > Unified operator stack: delivery, control, reproducibility Combining Node Manager (#816) and Prometheus exporter (#840) with a thin orchestration layer (e.g. Airflow, optionally n8n) gives a single stack that is not that heavy but covers the main operator needs: delivery, control, and reproducibility. Delivery: Deploy and update nodes via Node Manager; no need to hand-hold each host. Control: Same metrics (block height, POC weight, status) for everyone via the exporter + Prometheus + Grafana — hosts see what we see. Reproducibility: Airflow turns procedures into DAGs: health checks, update windows, report generation, cleanup, even ticket/workflow-style steps (e.g. “after alert → create task → run remediation”). Any scenario you can script becomes repeatable and auditable. So you get one place for “how we deploy”, “how we monitor”, and “how we react and rerun”. The stack is modular: minimal is exporter + Prometheus + Grafana; Node Manager and Airflow (and optionally n8n for event-driven bits) add on top for those who want automation and reproducibility. Worth doing? Yes. It directly tackles “hosts can’t easily configure and monitor like we do”: same tooling, same visibility, and the same ability to encode and replay scenarios instead of ad‑hoc SSH and one-off scripts. If the community wants to invest in operator experience and reproducibility, this is a concrete way to get there.
>
> One concrete number for why model-specialization deployment matters for
> the cache layer in PR #859:
>
>   hit_rate = repeat_fraction × (1/M) × (1 − stream_fraction)
>
>   M=571 (Qwen3-32B, shared across 571 nodes):  hit_rate = 0.000473
>   M=1   (unique model per node via Node Manager): hit_rate = 0.270
>
>   Specialization multiplier: 571× improvement in cache hit rate.
>   At M=1, MaxWeightFractionBps cap (+30% epoch weight) is reached.
>
> Node Manager's "one model per node" deployment pattern is the infrastructure
> prerequisite for the cache economics to work at network scale. The two proposals
> are complementary: Node Manager creates the conditions, semantic cache captures
> the reward.
>
> Data source: live network topology, gonka.gg/api/public (1,282 ML nodes,
> 5 models measured, epoch 190).

### Комментарий 3 — [@andrey055](https://github.com/andrey055)

*2026-03-01 17:47 UTC*

In the Telegram discussion, some people are saying that this improvement may not be very relevant right now. It seems there are more pressing tasks at the moment, especially since alternative solutions already exist. However, we truly wouldn’t like to lose your willingness to build projects for Gonka. 

Perhaps you could consider taking a look at a more relevant task?

**↳ Ответ от [@ochenUmnayaKatyshka](https://github.com/ochenUmnayaKatyshka)** · *2026-03-04 12:36 UTC*

> You mentioned an existing list of tasks. We would be happy to take a look — could you please point us to where we can find it?

**↳ Ответ от [@tcharchian](https://github.com/tcharchian)** · *2026-03-04 18:03 UTC*

> > You mentioned an existing list of tasks. We would be happy to take a look — could you please point us to where we can find it?
>
> We’ve recently published three new proposals on GitHub Discussions, and we’d really any feedback
>
> - https://github.com/gonka-ai/gonka/discussions/801
> - https://github.com/gonka-ai/gonka/discussions/800
> - https://github.com/gonka-ai/gonka/discussions/802 (for this proposal, I also opened an issue where design and implementation ideas can be discussed https://github.com/gonka-ai/gonka/issues/821)
>
> If you have thoughts, concerns, or improvement ideas, please share them directly in the comments 
>
> Also, I opened an additional discussion to highlight three key areas where help is needed https://github.com/gonka-ai/gonka/discussions/817. These are not yet framed as standalone tasks, but they point to three problems where your involvement, perspective, and suggestions would be extremely valuable.
>
> - https://github.com/gonka-ai/gonka/issues/818
> - https://github.com/gonka-ai/gonka/issues/820
> - https://github.com/gonka-ai/gonka/issues/819
>
> Also, you can filter issues with "up-for-grabs" label https://github.com/gonka-ai/gonka/issues?q=is%3Aissue%20state%3Aopen%20label%3Aup-for-grabs and see if there are any open tasks that have no assignee.
>
> More on bounty program: https://gonka.ai/FAQ/#bounty-program 

### Комментарий 4 — [@SegovChik](https://github.com/SegovChik)

*2026-03-09 11:41 UTC*

So here is working solution with some limitations(Still in development, so current functional is limited to provision network+mlnode on the same server) https://github.com/inc4/gonka-nop/releases/tag/v0.1.8-rc1. 
Download binary, execute ./gonka-nop setup and here we are.

**↳ Ответ от [@SegovChik](https://github.com/SegovChik)** · *2026-03-09 11:44 UTC*

> and here is our roadmap of what was done.
>
> ## Implementation Milestones
>
> ### Milestone 1: Core CLI Framework ✅ COMPLETE
>
> #### 1.1 Project Scaffolding
> - [x] Initialize go.mod with dependencies
> - [x] Create cmd/gonka-nop/main.go entry point
> - [x] Create internal/cmd/root.go with cobra root command
> - [x] Add version, status, reset, gpu-info command stubs
> - [x] Create internal/cmd/setup.go (setup command with flags)
>
> #### 1.2 UI Utilities (needed for phases)
> - [x] Create internal/ui/output.go (colored messages: Info, Success, Warn, Error)
> - [x] Create internal/ui/spinner.go (progress spinner wrapper)
> - [x] Create internal/ui/prompt.go (survey wrapper for interactive prompts)
>
> #### 1.3 State Management
> - [x] Create internal/config/state.go (State struct)
> - [x] Implement Save() and Load() methods
>
> #### 1.4 Phase System
> - [x] Create internal/phases/phase.go (Phase interface + runner)
> - [x] Create mocked phases for demo:
>   - [x] 01_prerequisites.go (Docker, CUDA check - mocked)
>   - [x] 02_gpu_detection.go (GPU detection - mocked)
>   - [x] 03_network_select.go (network selection prompt)
>   - [x] 04_key_management.go (key workflow - mocked)
>   - [x] 05_config_generation.go (generate configs - mocked)
>   - [x] 06_deploy.go (docker compose - mocked)
>
> #### 1.5 Integration & Demo
> - [x] Wire setup command to phase runner
> - [x] Test full CLI compilation (go build ./...)
> - [ ] Run demo: gonka-nop setup (shows full mocked flow)
>
> #### 1.6 Status Command
> - [x] Create internal/status/status.go (NodeStatus struct, fetch functions)
> - [x] Create internal/status/display.go (formatted output)
> - [x] Implement 3 sections: Overview, Blockchain, MLNode
> - [x] Support --mocked flag for demo
> - [x] Implement gpu-info command with --mocked
>
> ---
>
> ### Milestone 2: Test Coverage (Tests First) 🔄 IN PROGRESS
>
> Write tests for existing code before adding new features. Target: 70%+ coverage.
>
> #### 2.1 Config Package Tests (target: 90%+)
> - [x] state_test.go - NewState, Save, Load, Reset, MarkPhaseComplete
> - [ ] Add edge case tests (invalid JSON, permission errors)
>
> #### 2.2 Phases Package Tests (target: 80%+)
> - [x] gpu_detection_test.go - recommendConfig, FormatGPUSummary
> - [ ] prerequisites_test.go - Mock docker/nvidia checks
> - [ ] config_generation_test.go - Template output validation
> - [ ] phase_runner_test.go - Phase execution flow
>
> #### 2.3 Status Package Tests (target: 70%+)
> - [ ] status_test.go - Mock HTTP responses, parse validation
> - [ ] display_test.go - Output formatting
>
> #### 2.4 UI Package Tests (target: 50%+)
> - [ ] output_test.go - Color formatting
> - [ ] spinner_test.go - Basic functionality
> - [ ] prompt_test.go - Mock survey responses (harder to test)
>
> #### 2.5 Integration Tests
> - [ ] cmd/setup integration test with mocked phases
> - [ ] End-to-end state persistence test
>
> ---
>
> ### Milestone 3: GPU & Prerequisites (EXPANDED per chat analysis) ✅ MOSTLY COMPLETE
>
> Real system detection replacing mocked implementations. Validated on mainnet (8x A100 SXM4 80GB).
>
> #### 3.1 GPU Detection (real nvidia-smi) ✅ COMPLETE
> - [x] Parse `nvidia-smi --query-gpu=index,name,memory.total,driver_version,pci.bus_id --format=csv`
> - [x] Detect GPU architecture (sm_80=A100, sm_86=A40/RTX3090, sm_89=L40/RTX4090, sm_90=H100/H200, sm_100=B200/B300, sm_120=RTX5090) — `GPUArchFromName()` in gpu_parser.go
> - [x] NVLink/PCIe topology detection — name-based (H100/H200/A100 = NVLink, others = PCIe). Full `nvidia-smi topo -m` not yet implemented.
> - [x] PCIe bandwidth warning for multi-GPU setups without NVLink
> - [x] Auto-select MLNode image tag based on architecture (standard / blackwell) — `selectMLNodeImage()`
>
> #### 3.2 Docker & Runtime Checks ✅ COMPLETE
> - [x] Docker availability and version check — `ParseDockerVersion()` in gpu_parser.go
> - [x] NVIDIA Container Toolkit detection (`nvidia-ctk --version`)
> - [x] CUDA verification inside Docker container (`docker run --gpus all nvidia/cuda:12.6.0-base-ubuntu22.04 nvidia-smi`) — `checkCUDAInDocker()`
> - [x] Docker Compose v2 check (`docker compose version`) — `ParseDockerComposeVersion()`
>
> #### 3.3 NVIDIA Driver Installation & Validation ✅ MOSTLY COMPLETE
> - [x] Detect driver state: not installed / installed / version mismatch — `checkNVIDIADriver()`
> - [ ] Pre-check safety: Secure Boot status, kernel headers available, distro compatibility
> - [x] Offer auto-install with user confirmation — `installNVIDIADriver()` via apt
> - [x] Install Fabric Manager (`nvidia-fabricmanager-570`) if multi-GPU NVLink detected — `checkFabricManager()` with auto-start + install prompt
> - [x] Compare userspace lib version vs kernel module version vs Fabric Manager version — 3-way consistency check in `checkDriverConsistency()`
> - [x] Detect `unattended-upgrades` package and warn about NVIDIA driver auto-updates — suggests `apt-mark hold nvidia-driver-*`
> - [ ] Verify CUDA version compatibility with detected driver
> - [ ] Warn about reboot requirement after kernel module install/update
>
> #### 3.4 System Prerequisites ✅ MOSTLY COMPLETE
> - [x] Linux distro detection (Ubuntu, Debian, CentOS, Amazon Linux) — `ParseOSRelease()` in gpu_parser.go
> - [x] Disk space pre-check (warn if < 250 GB free) — `ParseDiskFreeGB()`, `ParseLsblkJSON()`
> - [x] NVIDIA Container Toolkit auto-installation (with user confirmation)
> - [x] Docker runtime configuration (`nvidia-ctk runtime configure --runtime=docker`)
> - [ ] Port availability check (5000, 8000, 26657 external; 5050, 8080, 9100, 9200 internal)
>
> ---
>
> ### Milestone 4: Configuration (EXPANDED per chat analysis) ✅ MOSTLY COMPLETE
>
> Generate production-ready configs with security and performance defaults learned from validators. Validated on mainnet deploy.
>
> #### 4.1 TP/PP Recommendation Algorithm ✅ COMPLETE
> - [x] Model-aware TP/PP calculation (Qwen3-235B, Qwen3-32B, QwQ-32B) — `recommendConfig()` with 4-tier VRAM logic
> - [x] `gpu-memory-utilization` recommendation: 0.88-0.94 based on VRAM headroom (NOT 0.99)
> - [x] `max-model-len` calculation based on remaining VRAM after model loading
> - [x] Auto-add `--kv-cache-dtype fp8` for tight VRAM configs (e.g., 8x A100 40GB with 235B)
> - [x] PP not set in vLLM args — MLNode runner auto-calculates from GPUs/TP. No `--quantization fp8` either (causes MoE alignment errors)
>
> #### 4.2 node-config.json Generation ✅ COMPLETE
> - [x] Template-based generation with go:embed
> - [x] `host` field validation (no `http://` prefix -- common mistake from chat)
> - [x] `hardware` field auto-populated from GPU detection
> - [x] `max_concurrent` recommendation based on GPU config
> - [x] Model selection with explicit declaration (required for PoC v2)
>
> #### 4.3 config.env Generation ✅ COMPLETE
> - [x] Template-based with validated fields
> - [x] `MODEL_NAME` environment variable (mandatory after v0.2.8)
> - [x] `VLLM_ATTENTION_BACKEND` = FLASHINFER for ALL architectures (3.0.12+ standard, old FLASH_ATTN rule obsolete)
>
> #### 4.4 docker-compose.yml Generation ✅ COMPLETE
> - [x] Template-based with go:embed
> - [x] **Port security: bind internal ports to 127.0.0.1** (5050, 8080, 9100, 9200)
> - [x] Public ports: 5000 (P2P), 8000 (API via proxy), 26657 (RPC -- via proxy only after DDoS hardening)
> - [x] MLNode image tag selection based on GPU architecture detection
>
> #### 4.5 DDoS Protection Defaults ✅ COMPLETE
> - [x] Proxy service config: `GONKA_API_BLOCKED_ROUTES=poc-batches training`
> - [x] Proxy service config: `GONKA_API_EXEMPT_ROUTES=chat inference`
> - [x] Default: `DISABLE_CHAIN_API=true`, `DISABLE_CHAIN_RPC=true`, `DISABLE_CHAIN_GRPC=true`
> - [x] RPC port (26657) accessible only via proxy, not directly exposed
>
> #### 4.6 Sync & Pruning Configuration ✅ COMPLETE
> - [x] Auto-configure `persistent_peers` in config.toml with known-good peers
> - [x] Generate `app.toml` with pruning: `custom`, `keep-recent=1000`, `interval=100`
> - [x] Set `GENESIS_SEEDS` and `SEED_API_URL` to reliable endpoints
> - [x] Enable state sync by default (`SYNC_WITH_SNAPSHOTS=true`)
>
> ---
>
> ### Milestone 5: Deployment (EXPANDED per chat analysis) ✅ MOSTLY COMPLETE
>
> Deploy containers with real orchestration, security hardening, and sync monitoring. Validated on mainnet + testnet.
>
> #### 5.1 Docker Compose Orchestration ✅ COMPLETE
> - [x] Multi-compose file handling (transparent `-f docker-compose.yml -f docker-compose.mlnode.yml`)
> - [x] Automatic `source config.env` + `sudo -E` for environment variable propagation — `internal/docker/env.go` + `compose.go`
> - [x] Image pull with progress display — `docker compose pull`
> - [x] Container startup with ordered dependencies — network node first, then ML node
>
> #### 5.2 Firewall Configuration ⚠️ (from chat: Docker bypasses UFW)
> - [ ] Detect Docker's iptables behavior
> - [ ] Configure DOCKER-USER chain rules:
>   - Allow established connections
>   - Allow public ports (5000, 8000)
>   - Whitelist known Gonka seed peers
>   - DROP all other inbound to Docker containers
> - [ ] Offer `iptables-persistent` integration for rule persistence
> - [ ] IPv4/IPv6 resolution check for vLLM health endpoint (prevent restart loop)
>
> #### 5.3 Key Management (both workflows) ✅ COMPLETE
> - [x] Quick workflow: generate all keys on server — `04_key_management.go`
> - [x] Secure workflow: accept account pubkey, generate consensus + ML keys — `--account-pubkey` flag
> - [x] `grant-ml-ops-permissions` automation — `07_registration.go`
> - [x] Key backup guidance
>
> #### 5.4 Model Weight Download ✅ COMPLETE
> - [x] HuggingFace model download with progress bar — standalone `gonka-nop download-model` command + deploy phase
> - [x] Resume support for interrupted downloads — uses `docker run` with `HF_HOME` mount
> - [ ] SHA256 verification after download
> - [x] Pre-download into `HF_HOME` before container startup
>
> #### 5.5 Health Checks & Sync Monitoring ✅ COMPLETE
> - [x] Container health verification (all services running) — polls `/admin/v1/setup/report`
> - [x] Blockchain sync progress with block lag display — polls Tendermint RPC `/status`, shows block height progress, 30min timeout
> - [x] Wait for sync completion before registration (configurable timeout)
> - [ ] Port accessibility check (external ports reachable) — PUBLIC_URL reachability check planned
>
> ---
>
> ### Milestone 6: Operations ⚠️ NEW (from chat: day-2 is 90% of operator time)
>
> Post-deployment commands for ongoing node management. This entire milestone was missing from the original plan and is driven by validator chat analysis showing operators spend most time on operations, not setup.
>
> #### 6.1 `gonka-nop status` (real implementation) ✅ COMPLETE
> - [x] Blockchain: block height, sync status, blocks behind, catching_up flag
> - [x] Epoch: current epoch, participation status, weight, miss rate
> - [x] Epoch: PoC weight, timeslot allocation, inference count, upcoming epoch, reward claim status
> - [x] MLNode: model loaded, GPU utilization, PoC status, intended vs current mismatch, status freshness
> - [x] Node Config: public URL, PoC callback URL, seed API, API version, height lag, upgrade plan
> - [x] Security: cold key, warm key, ML permissions
> - [x] Containers: running/stopped/unhealthy state inferred from setup/report checks
> - [ ] **PUBLIC_URL reachability check** — HTTP GET `<public_url>/health`, report PASS/FAIL with error details. Critical: port mismatch or wrong registered URL = validators can't verify PoC proofs = node never gains weight. Learned from testnet debugging (2026-02-11).
> - [ ] Network: peer count (blocked — Tendermint RPC 26657 not exposed to host on standard deployments)
> - [ ] Miss rate timeline (green/red dot visualization)
>
> #### 6.2 `gonka-nop update` (safe rollout) ✅ COMPLETE (implemented as M9.2)
> - [x] Check `timeslot_allocation` via Admin API to find safe window
> - [x] Disable ML node via `POST /admin/v1/nodes/:id/disable`
> - [x] Pull new container image with progress
> - [x] Update image tag in docker-compose file
> - [x] Recreate container (`--no-deps --force-recreate`)
> - [x] Wait for model load completion (monitor logs)
> - [x] Re-enable ML node via `POST /admin/v1/nodes/:id/enable`
> - [x] Verify health after update
> - [x] Distinguish auto-update (Cosmovisor: node, api) vs manual (mlnode, proxy)
>
> #### 6.3 `gonka-nop reset` (blockchain data cleanup)
> - [ ] Preserve keys (tmkms, account, ML) and config files
> - [ ] Run `inferenced tendermint unsafe-reset-all --keep-addr-book` inside container
> - [ ] Remove `upgrade-info.json` and `cosmovisor/` directory
> - [ ] Restart node container
> - [ ] Monitor sync progress after reset
>
> #### 6.4 `gonka-nop cleanup` (disk space recovery)
> - [ ] Calculate current disk usage (`.inference/data/`, cosmovisor backups)
> - [ ] Remove old Cosmovisor backup directories
> - [ ] Report freed space
> - [ ] Recommend pruning settings if not configured
>
> #### 6.5 `gonka-nop ml-node` (Admin API wrapper) 🔄 PARTIAL
> - [x] `ml-node list` - GET /admin/v1/nodes (status, allocation, model, hardware, PoC weight)
> - [ ] `ml-node add` - POST /admin/v1/nodes (interactive or from config)
> - [ ] `ml-node update` - PUT /admin/v1/nodes/:id (model, TP/PP, max_concurrent)
> - [x] `ml-node enable/disable` - POST /admin/v1/nodes/:id/enable|disable
> - [x] `ml-node status` - Detailed: host, ports, model+args, hardware, status/intended mismatch, epoch allocation, PoC weight, timeslots, status freshness
>
> #### 6.6 `gonka-nop model` (model management)
> - [ ] Switch model via Admin API (PUT /admin/v1/nodes/:id)
> - [ ] Show current model and next-epoch model
> - [ ] Warn that model changes apply next epoch only
> - [ ] Validate model compatibility with GPU config
>
> #### 6.7 Pre-upgrade Binary Download
> - [ ] Download inferenced and decentralized-api binaries from GitHub releases
> - [ ] SHA256 verification
> - [ ] Place in correct Cosmovisor upgrade directory
> - [ ] Verify permissions (chmod +x)
>
> ---
>
> ### Milestone 7: Registration & On-chain
>
> #### 7.1 Registration Flow ✅ COMPLETE
> - [x] `submit-new-participant` with correct flags (validator-key, chain-id, node URL)
> - [x] Auto-fetch `consensus_pubkey` from setup report API
> - [x] `grant-ml-ops-permissions` for ML key
> - [x] Validate PUBLIC_URL format (no http:// prefix)
>
> #### 7.2 PoC Verification
> - [ ] Test PoC endpoint (`/api/v1/pow/init/generate`)
> - [ ] Verify model loaded and responding
> - [ ] Check epoch participation after registration
>
> #### 7.3 Reward Management
> - [ ] `gonka-nop claim-rewards` - Simplified claim flow
> - [ ] Fetch seed from Admin API config
> - [ ] Force-claim via `/admin/v1/claim-reward/recover` for missed epochs
> - [ ] Show unclaimed reward history
>
> #### 7.4 Governance
> - [ ] `gonka-nop vote` - Simplified governance voting
> - [ ] Show active proposals
> - [ ] Vote with account key
>
> ---
>
> ### Milestone 8: Advanced & Polish 🔄 IN PROGRESS
>
> - [ ] Multi-node batch management (update/status across 10+ nodes)
> - [ ] Miss rate timeline visualization (dot-based OK/missed display)
> - [ ] Cloud provider compatibility (Vast.ai port remapping, GCore bare metal)
> - [ ] Russian language support for error messages and prompts
> - [x] Monitoring integration (Prometheus exporter + centralized push architecture) — see M8.1
> - [ ] Performance benchmarking integration (compressa-perf)
> - [ ] Self-update mechanism for gonka-nop binary
> - [ ] Documentation & release automation
>
> #### 8.1 Centralized Monitoring (Ansible) ✅ COMPLETE
>
> Opt-in push-based monitoring for Gonka validators. Ansible-based deployment in `ansible/` subdirectory.
>
> **Architecture:** Exporter + Prometheus on validator → `remote_write` push → Central Prometheus + Grafana (operated by inc4). No inbound ports opened on validator nodes.
>
> **Components built:**
> - [x] `gonka-exporter` role — bundles votkon's exporter (28 metrics from 5 API endpoints), builds Docker image locally, deploys via compose
> - [x] `prometheus` role — Prometheus with conditional `remote_write`, alert rules (11 rules in 2 groups), `--web.enable-remote-write-receiver` for central server
> - [x] `alertmanager` role — conditional Telegram/Discord/Slack notifications, route-based severity
> - [x] `grafana` role — auto-provisioned datasources + 2 dashboards (Fleet Overview, Node Deep Dive)
> - [x] `playbooks/deploy-all.yml` — full stack for central server (exporter + prometheus + alertmanager + grafana)
> - [x] `playbooks/add-node.yml` — add internal validator with remote_write to central
> - [x] `playbooks/client-deploy.yml` — self-contained for external validators (hardcoded central URL, validates prerequisites, verifies remote_write works)
> - [x] `playbooks/client-teardown.yml` — clean removal of monitoring from validator
> - [x] `inventory/client.yml.example` — template for external operators
> - [x] `README.md` — operator-focused documentation with architecture diagram, metrics table, alert rules, security guarantees
> - [x] `.gitignore` — protects client inventory files from accidental commits
>
> **Dashboards:**
> - Fleet Overview (`gonka-fleet-overview`) — multi-node overview with status, block lag, miss rate, PoC weight, GPU, earnings
> - Node Deep Dive (`gonka-node-deep-dive`) — per-node detail with `$instance` template variable
>
> **Alert rules (11):**
> - Critical: GonkaMissRateHigh (>20%), GonkaNodeFailed, GonkaBlockLagCritical (>200 blocks), GonkaNodeStopped, GonkaExporterDown
> - Warning: GonkaBlockLag (>50), GonkaCatchingUp, GonkaGPUUtilizationHigh (>95%), GonkaZeroWeight, GonkaZeroInferences, GonkaStatusMismatch
>
> ---
>
> ### Milestone 9: Version Management ✅ COMPLETE (3/4 tasks, pre-seeding deferred)
>
> Dynamic image versions and safe upgrade handling. Addresses the "chicken and egg" problem where NOP hardcodes image versions that become stale after chain upgrades.
>
> **Source of truth:** `gonka-ai/gonka` GitHub repository
> - Mainnet: `main` branch → `deploy/join/docker-compose.yml` + `docker-compose.mlnode.yml`
> - Testnet: `testnet/main` branch → same paths
>
> #### 9.1 Dynamic Image Version Fetching ✅ COMPLETE
> - [x] `ImageVersions` struct with per-service tags (node, api, tmkms, proxy, bridge, mlnode, nginx)
> - [x] `FetchImageVersions()` fetches from GitHub raw URLs at setup time
> - [x] `ParseComposeImageVersions()` extracts tags from compose YAML (handles comments, bridge digest pins, proxy vs proxy-ssl)
> - [x] Fallback to hardcoded versions when GitHub unreachable
> - [x] Network select phase fetches and populates state
> - [x] Config generation uses per-service versions
> - [x] 12 tests covering parsing, fallback, disambiguation
>
> #### 9.2 `gonka-nop update` (safe version update) ✅ COMPLETE
> - [x] Fetch latest versions from GitHub and compare with current compose files
> - [x] Show diff of version changes before applying
> - [x] For manual-update services (proxy, bridge, mlnode): update image tags in compose files
> - [x] Safe MLNode rollout: check timeslot_allocation → disable → pull → recreate → wait model load → enable
> - [x] For Cosmovisor-managed services (node, api): inform user these auto-update at chain upgrade block
> - [x] `--check` flag to only show available updates without applying
>
> #### 9.3 Cosmovisor Upgrade Pre-seeding (during deploy)
> - [ ] Query chain governance proposals via REST API (`/cosmos/gov/v1/proposals`)
> - [ ] Detect pending or applied upgrade plans
> - [ ] Pre-download inferenced and decentralized-api binaries to Cosmovisor upgrade dirs
> - [ ] SHA256 verification from proposal `plan.info` field
> - [ ] Prevents node stuck in restart loop if offline during upgrade block
>
> #### 9.4 `gonka-nop repair` (detect and fix stuck nodes) ✅ COMPLETE
> - [x] Detect "upgrade handler is missing" restart loop in node container logs
> - [x] Parse upgrade-info.json `info` field for on-chain binary URLs (source of truth for mainnet vs testnet repos)
> - [x] Download and place binaries in correct Cosmovisor upgrade directory (with SHA256 verification)
> - [x] Update `current` symlink to point to upgrade directory
> - [x] Restart node container
> - [x] Fix: prefer upgrade-info.json URLs over GitHub release search (prevents wrong binary on testnet)
>
> ---
>
> ### Milestone 10: Multi-MLNode Support (Separate Servers) — PLANNED
>
> #### 10.1 ml-node add/update/delete commands
> - [ ] `ml-node add` — POST /admin/v1/nodes (interactive + flag modes)
> - [ ] `ml-node update <id>` — PUT /admin/v1/nodes/:id
> - [ ] `ml-node delete <id>` — DELETE /admin/v1/nodes/:id
>
> #### 10.2 Setup type flag (--type full|network|mlnode)
> - [ ] `--type network` — chain node + API only, skip GPU/mlnode phases
> - [ ] `--type mlnode --network-node URL` — GPU server only, new mlnode-specific phases
> - [ ] `--type full` (default) — current behavior unchanged
>
> #### 10.3 MLNode-only setup phases
> - [ ] `08_mlnode_config.go` — generate mlnode compose + nginx only
> - [ ] `09_mlnode_deploy.go` — docker compose up + register with network node via Admin API
> - [ ] PoC callback URL warning for multi-server setups

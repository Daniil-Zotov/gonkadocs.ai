---
title: "#1085 — INC4 | Gonka Node Observability Platform"
source: https://github.com/gonka-ai/gonka/discussions/1085
discussion_number: 1085
category: proposals
synced_at: 2026-06-22T05:32:10Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1085](https://github.com/gonka-ai/gonka/discussions/1085) каждые 6 часов. 

# INC4 | Gonka Node Observability Platform

**Автор:** [@rwxr-xr-x](https://github.com/rwxr-xr-x) · **Категория:** :bulb: Proposals · **Создано:** 2026-04-16 18:05 UTC · **Обновлено:** 2026-04-18 07:51 UTC

---

## 📝 Описание

# Gonka Node Observability Platform

Proposal by INC4 (https://inc4.net) | 16 April 2026

Funding Request: \$96,000 USD (USDT) for 12 months

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Industry Context](#3-industry-context)
4. [Proposed Solution](#4-proposed-solution)
5. [Technical Approach](#5-technical-approach)
6. [Scope and Deliverables](#6-scope-and-deliverables)
7. [Budget and Payment Schedule](#7-budget-and-payment-schedule)
8. [Success Criteria](#8-success-criteria)
9. [Team](#9-team)

---

## 1. Executive Summary

Today's explorers and dashboards only show on-chain data, leaving the off-chain state of validators completely opaque. The few operators who do run their own monitoring use different tools, different metrics, and different baselines, leading to different interpretations and making it harder to coordinate when problems arise. The network lacks a single source of truth and a common framework for measuring validator health.

Even today, simply watching how validators operate reveals that many are not reacting to technical problems in time — growing Inference Miss Rates, dropping CPoC Ratios, network sync falling behind. These patterns persist because operators have no way to see the early warning signs or get emergency alerts inside their own infrastructure.

To address this, INC4 — an active Gonka validator operator with hands-on experience in blockchain infrastructure and observability — proposes the creation of the Gonka Node Observability Platform — an open-source, opt-in observability stack that aggregates off-chain metrics from Network nodes and ML nodes into a shared, publicly accessible dashboard. The platform is deployed on independent cloud infrastructure — without using resources of any individual validator or granting anyone privileged access — so that all operators have equal access and visibility into the data.

For the Core Team — a unified view of the entire network, visibility into problematic nodes and time periods, data for informed protocol decisions, SLA reports, and the ability to assess the scope of network-wide issues before and after upgrades. For Individual Validators — real-time alerts, performance comparison against network averages, opt-in log sharing to get help with troubleshooting and metrics interpretation, and no need to build your own monitoring stack.

Detecting and preventing even a single major network-wide incident, or a series of smaller incidents at individual validators, can save the ecosystem far more than the annual cost of this platform. The primary beneficiaries are the validator operators themselves, who bear the direct cost of every missed epoch and every hour of undiagnosed downtime — especially individual hosts without dedicated DevOps staff, for whom building and maintaining a comparable monitoring stack on their own is simply not feasible.

We request \$96,000 in USDT over 12 months, paid in quarterly tranches, to deploy and maintain a production-grade observability platform — custom Gonka exporters, fleet-wide and individual dashboards, opt-in log aggregation, external endpoint health checks, alerting and SLA reporting, hands-on validator onboarding, incident response support, and ongoing operational maintenance. All code, configurations, and dashboards will be open-source and published in public GitHub repositories.


---

## 2. Problem Statement

### Off-chain state of the network is not visible

Gonka is a growing network with over a hundred validators, an even larger number of ML nodes, and a combined GPU fleet exceeding 3,000 cards. Existing block explorers and dashboards show on-chain data — block heights, transactions, voting power. But there are zero tools for network-wide off-chain observability — GPU health, container status, miss rate root causes, model load times, LLM performance metrics, infrastructure trends, etc. Each operator monitors their infrastructure in isolation — or doesn't monitor at all. Those who do monitor set up their own tools, calculate metrics differently, and use different baselines — which leads to miscommunication and confusion when discussing network issues.

Specifically, existing tools do not show:

- Why a validator's miss rate is high
- Whether RAM or GPU memory is exhausted
- Whether ML or other containers are crash-looping
- How long model loading takes after a restart
- Whether a PUBLIC_URL is reachable from outside
- Comparative performance across validators

In practice, validators have experienced prolonged periods of high miss rate or inference downtime without being able to identify the root cause. At the same time, the Core Team had no way to see the scope of such issues across the network. These situations result in lost rewards for operators and delayed response from the team — problems that a shared observability platform would help detect and resolve much faster.

### What happens without a solution

- Silent failures go undetected for hours or days — costing validators missed epochs and lost rewards
- No common ground for debugging — each operator uses different tools, different baselines, different definitions of "normal"
- The Core Team lacks fleet-wide visibility — making it harder to diagnose network-level issues and plan upgrades
- New operators are on their own — high barrier to entry for smaller hosts without DevOps expertise

---

## 3. Industry Context

### Collecting validator metrics in one place is not new

Aggregating telemetry and metrics from validators into a shared backend is a well-established practice across the blockchain industry. Multiple major networks already do this:

- Solana — validators report metrics to a shared backend; the network publishes a public Grafana dashboard at `https://metrics.solana.com:3000`
- Polkadot — nodes send telemetry by default to a shared backend; a public real-time dashboard is available at `https://telemetry.polkadot.io`
- Kusama — uses the same Substrate Telemetry system as Polkadot, with its own view at `https://telemetry.polkadot.io/#list/Kusama`
- NEAR — every node ships with a default telemetry endpoint (`telemetry.nearone.org`) and pushes data every 10 seconds
- Aptos — all nodes push metrics to a centralized telemetry service (`telemetry.mainnet.aptoslabs.com`) by default; the architecture is documented in a public SPEC
- Celestia — maintains an OpenTelemetry collector endpoint (`otel.celestia.observer`) for DA nodes, plus a Prometheus-based observability stack for consensus nodes

This is not an exotic idea. It is how mature networks gain visibility into their health, diagnose issues faster, and make data-driven protocol decisions.

In many blockchain networks, node telemetry is collected without operators being fully aware of it — telemetry is often enabled by default in the node software, and in some cases operators have no way to disable it at all.

By contrast, the Gonka Node Observability Platform is designed as a fully opt-in system — validators choose to participate, and no data is collected without their explicit action.

The more validators that join, the more accurate and complete the picture of network health becomes. A platform with 30% of validators connected provides useful insights; one with 80% becomes a reliable source of truth for the entire ecosystem.

---

## 4. Proposed Solution

### Gonka Node Observability Platform

A managed, open-source observability stack where validator operators voluntarily push off-chain metrics to a shared platform maintained by INC4.

### Design principles

| Principle | Implementation |
|-----------|---------------|
| Open-source | All exporters, dashboards, alert rules, and configuration will be open-source and available for audit by any interested party |
| Opt-in | Participation is voluntary, no validator is required to share data — but every participant makes the platform more valuable for the entire network |
| Push-based | Nodes push metrics outbound via HTTPS, no new inbound ports required, existing firewall configs are preserved |
| Non-intrusive | The platform is a separate layer — it does not interact with consensus, block production, or inference execution, a platform outage has zero effect on the Gonka network |
| Privacy | The platform will only collect metrics necessary to understand validator health and performance — such as block height, sync status, miss rate, GPU utilization, container status, resource usage, etc. No sensitive information will be collected — no private keys, wallet balances, mnemonic phrases, or account credentials |

### Value delivered

For the Core Team:
- Aggregated fleet-wide metrics and logs in one place
- Instant visibility into problematic nodes, epochs, and time periods
- SLA reports and data-driven decision making for protocol upgrades
- Incident response support with root cause analysis

For validators:
- No need to build and maintain your own monitoring stack
- Compare your node's performance against network averages
- Receive alerts via Telegram or Discord when something goes wrong
- Share logs for collaborative troubleshooting when experiencing issues
- Access dashboards from any device, including mobile
- Hands-on help with metrics interpretation and incident diagnosis

For the community:
- A single source of truth for network health metrics
- Consistent data that all participants can reference in discussions
- Transparency into network operations

---

## 5. Technical Approach

The platform will be deployed on distributed cloud infrastructure, providing:

- High availability — no single point of failure; redundant infrastructure with 99.5%+ uptime SLA
- Automatic scaling — the platform grows seamlessly as more validators join, with no manual intervention required
- Push-based data collection — validators push metrics outbound via HTTPS; no new inbound ports are required, and existing firewall configurations are fully preserved

We will use well-established, industry-proven tools for observability: Prometheus for metrics collection, Grafana for dashboards and visualization, Alertmanager for notifications, Promtail/Loki for unified opt-in log aggregation, and PagerDuty for incident management and on-call escalation.

INC4 has hands-on experience building and operating observability infrastructure for blockchain networks. The choice of each component in the stack is driven by real-world operational requirements — reliability under load, ease of integration with existing validator setups, minimal resource overhead on the node side, and the ability to scale without rearchitecting as the network grows. This practical experience directly informs the architecture and tooling choices behind this platform.

The detailed architecture, including specific metric definitions, data flows, and exporter specifications, will be documented separately and will evolve as the platform matures.

---

## 6. Scope and Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Cloud infrastructure | Production-ready observability stack on distributed cloud infrastructure with high availability, redundancy, and data retention |
| 2 | gonka-exporter | Open-source exporter collecting Gonka node and AI compute metrics, kept up to date with every Gonka release |
| 3 | Unified opt-in log aggregation | Searchable log collection from Gonka nodes and ML containers — validators experiencing issues can share logs for collaborative troubleshooting with the community and the Core Team |
| 4 | External endpoint health checks | Automated reachability checks of validator reachability from independent external locations |
| 5 | Fleet Overview Dashboard | Single view of the entire network — node statuses, miss rates, GPU utilization, sync state, and trends over time |
| 6 | Individual Node Dashboard | Per-validator view with historical performance tracking and comparison against network averages |
| 7 | Custom dashboards | Additional dashboards developed on request from the Core Team and individual validators, iteratively improved based on community feedback |
| 8 | Alert rules and SLA reports | Alerting via Telegram, Discord, and PagerDuty. Automated SLA reports for validators and the Core Team |
| 9 | Onboarding documentation | Step-by-step guide for validators to connect to the platform |
| 10 | Validator onboarding | Hands-on onboarding support with a dedicated engineer during the initial rollout, followed by ongoing guidance for new validators |
| 11 | Incident response and advisory | Help for individual validators and the Core Team with metrics interpretation, incident diagnosis, root cause analysis, and post-incident reviews |
| 12 | Ongoing maintenance | Dedicated DevOps team ensuring platform reliability, compatibility with Gonka upgrades, and continuous operational improvements |

---

## 7. Budget and Payment Schedule

### Summary

| Category | Annual Cost | Basis |
|----------|------------|-------|
| Cloud infrastructure | \$18,000 | ~\$1,500/mo for managed Prometheus (metrics storage and querying), Grafana (dashboards and visualization), Alertmanager (notifications), Promtail/Loki (unified opt-in log aggregation), PagerDuty (incident management and on-call escalation), external endpoint health checks, and supporting infrastructure, includes metrics retention, log storage, and high-availability configuration with redundancy |
| Infrastructure operations and maintenance | \$36,000 | DevOps team with a combined allocation of 0.5 FTE (~\$3,000/mo) for platform operations, incident response, compatibility verification after Gonka network upgrades, capacity planning, on-call support, backup and disaster recovery, performance tuning and optimization, access management for connected validators, infrastructure-as-code maintenance, and platform self-monitoring |
| Exporter development and updates | \$12,000 | Development and maintenance of gonka-exporter (Gonka-specific node and AI compute metrics), Promtail log collection configurations, Blackbox exporter probes, integration with node_exporter and GPU metrics exporters, and ongoing compatibility updates for new Gonka releases. Some advanced metrics may require changes to the Gonka node software — INC4 will collaborate with the Core Team to propose and implement the necessary API extensions |
| Custom dashboards and custom alerts | \$12,000 | Fleet overview and individual node dashboards, alert rules with Telegram and Discord notifications, SLA reports, development of custom dashboards on request from the Core Team, personalized dashboards for individual validators on request, and iterative improvements based on ongoing collaboration with the validator community |
| Validator onboarding, incident response, and advisory | \$18,000 | First 3 months — dedicated DevOps engineer for hands-on onboarding of initial validators and end-to-end system setup. Ongoing — documentation maintenance, onboarding guidance for new validators, hands-on support for individual validators and the Core Team in interpreting metrics, diagnosing incidents, coordinating remediation, root cause analysis, actionable recommendations, and post-incident reviews for network-wide events |
| Total requested | \$96,000 | |

### Payment schedule

| Tranche | Period | Amount | Covers |
|---------|--------|--------|--------|
| 1 | Months 1–3 | \$51,000 | Cloud infrastructure setup and provisioning, core exporter and dashboard development, dedicated DevOps engineer for initial validator onboarding |
| 2 | Months 4–6 | \$15,000 | Platform operations, maintenance, incident response, validator support, and continued development of custom dashboards and alert rules |
| 3 | Months 7–9 | \$15,000 | Platform operations, maintenance, incident response, validator support, and iterative improvements to exporters and dashboards based on validator feedback |
| 4 | Months 10–12 | \$15,000 | Platform operations, maintenance, incident response, validator support, and year-end usage and adoption report |

Vesting contact: https://github.com/rwxr-xr-x/gonka-usdt-vesting-schedule

Each tranche is paid on the first day of the respective period.

The first tranche is larger because it covers the infrastructure setup and the most development-intensive phase of the project.

### Risks

- Low validator adoption — INC4 will actively support onboarding and demonstrate platform value through early adopters
- Infrastructure cost growth — the budget includes a reserve; if needed, migration to a more cost-effective solution is possible without service interruption
- Platform does not affect the Gonka network — it operates as a completely separate layer; any platform issue has zero impact on validators or consensus

The budget is calculated for one year. After the first year, the arrangement can be reviewed and renewed on the same or adjusted terms. INC4 will publish a transparent report on platform usage, adoption, and costs at the end of the grant period — giving the community a clear basis for the renewal decision. If the community decides not to renew, the fully configured and operational platform — including all infrastructure, code, and configurations — may be transferred to the Core Team.

---

## 8. Success Criteria

What INC4 delivers:
- Base version of the platform deployed and accepting metrics — within the first week, with continuous improvements and updates going forward
- Exporter, fleet dashboard, and alerting available in base version — within the first month, continuously improved throughout the grant period
- INC4 will actively assist validators who wish to connect — providing hands-on onboarding support alongside documentation in the GitHub repositories
- All code, configurations, and dashboards published in public GitHub repositories — open for anyone to review, audit, or contribute

What depends on the community:
- INC4 will actively support onboarding but cannot guarantee adoption levels, as participation is voluntary
- Target — wide adoption across the network within the first year
- Sunshine scenario: connecting to the platform becomes a standard part of every validator's setup

Key Performance Indicators:
- Platform availability: 99%+ uptime throughout the grant period
- Compatibility: platform verified and operational within 48 hours after each Gonka network upgrade
- Onboarding: any validator can connect to the platform in under 30 minutes using provided documentation
- Reporting: quarterly progress reports published to the community
- Adoption: wide adoption across the network within the first year

---

## 9. Team

- Website: https://inc4.net
- GitHub: https://github.com/inc4

INC4 is an active participant in the Gonka ecosystem. We operate validators on mainnet and testnet, and develop applications for the Gonka network. This proposal grows out of our direct experience — we face the lack of network-wide visibility firsthand as validator operators and want to solve this problem for the entire network.

INC4 is involved in multiple initiatives across the Gonka ecosystem — the observability platform is one of them. For example, we also develop NOP (Node Onboarding Package) — an open-source utility for fast validator deployment (https://github.com/inc4/gonka-nop). Our commitment to the network is long-term and not limited to this proposal.

As a company, INC4 was founded in 2013, with 70+ engineers and 230+ delivered projects in blockchain infrastructure and AI systems. Hands-on experience in building and maintaining mining infrastructure for Bitcoin, Ethereum, Filecoin.

---

## 💬 Комментарии (4)

### Комментарий 1 — [@rwxr-xr-x](https://github.com/rwxr-xr-x)

*2026-04-16 18:36 UTC*

# Gonka Node Observability Platform

Proposal от INC4 | 16 Апрель 2026

Запрос финансирования: \$96,000 USD (USDT) на 12 месяцев

---

## Содержание

1. [Резюме](#1-резюме)
2. [Описание проблемы](#2-описание-проблемы)
3. [Контекст индустрии](#3-контекст-индустрии)
4. [Предлагаемое решение](#4-предлагаемое-решение)
5. [Технический подход](#5-технический-подход)
6. [Scope и Deliverables](#6-scope-и-deliverables)
7. [Бюджет и график выплат](#7-бюджет-и-график-выплат)
8. [Критерии успеха](#8-критерии-успеха)
9. [Команда](#9-команда)

---

## 1. Резюме

Существующие эксплореры и дашборды показывают только on-chain данные, оставляя off-chain состояние валидаторов полностью непрозрачным. Немногие операторы, которые всё же мониторят свою инфраструктуру, используют разные инструменты, разные метрики и разные baseline — что приводит к разным интерпретациям и затрудняет координацию при возникновении проблем. У сети нет единого источника правды и общего фреймворка для оценки здоровья валидаторов.

Даже сейчас, просто наблюдая за работой валидаторов, можно заметить, что многие не реагируют на технические проблемы вовремя — растущий Inference Miss Rate, падающий CPoC Ratio, отставание Network Node Sync. Эти паттерны сохраняются, потому что у операторов нет возможности увидеть ранние предупреждающие сигналы или получить экстренные алерты внутри собственной инфраструктуры.

Для решения этой проблемы INC4 — активный оператор валидаторов Gonka с практическим опытом в блокчейн-инфраструктуре и наблюдаемости — предлагает создать Gonka Node Observability Platform — open-source стек мониторинга с добровольным участием, который агрегирует off-chain метрики от Network-нод и ML-нод в общий, публично доступный дашборд. Платформа разворачивается на независимой облачной инфраструктуре — без использования ресурсов конкретных валидаторов и без предоставления кому-либо привилегированного доступа — чтобы все операторы имели равный доступ к данным и равную видимость.

Для Core Team — единое представление всей сети, видимость проблемных нод и временных периодов, данные для обоснованных решений по протоколу, SLA-отчёты и возможность оценить масштаб сетевых проблем до и после обновлений. Для Отдельных Валидаторов — алерты в реальном времени, сравнение производительности со средними по сети, добровольный обмен логами для помощи в диагностике и интерпретации метрик, и не нужно строить собственный стек мониторинга.

Обнаружение и предотвращение даже одного крупного общесетевого инцидента или серии более мелких инцидентов у отдельных валидаторов может сэкономить экосистеме значительно больше, чем годовая стоимость этой платформы. Главными выгодополучателями станут сами операторы валидаторов, которые несут прямые издержки от каждой пропущенной эпохи и каждого часа недиагностированного простоя — особенно индивидуальные хосты без выделенных DevOps-специалистов, для которых создание и поддержка сопоставимого стека мониторинга своими силами попросту нереализуемы.

Мы запрашиваем \$96,000 в USDT на 12 месяцев с выплатой квартальными траншами для развёртывания и поддержки production-grade платформы — кастомные Gonka-экспортёры, общесетевые и индивидуальные дашборды, добровольная агрегация логов, внешние проверки доступности эндпоинтов, алертинг и SLA-отчётность, практический онбординг валидаторов, поддержка реагирования на инциденты и постоянная операционная поддержка. Весь код, конфигурации и дашборды будут open-source и опубликованы в публичных GitHub-репозиториях.


---

## 2. Описание проблемы

### Off-chain состояние сети не видно

Gonka — растущая сеть с более чем сотней валидаторов, ещё большим количеством ML-нод и суммарным парком GPU, превышающим 3,000 карт. Существующие блокчейн-эксплореры и дашборды показывают on-chain данные — высоту блоков, транзакции, voting power. Но нет ни одного инструмента для наблюдения за off-chain состоянием сети: здоровье GPU, статус контейнеров, корневые причины miss rate, время загрузки моделей, метрики производительности LLM, тренды инфраструктуры и т.д. Каждый оператор мониторит свою инфраструктуру в изоляции — или не мониторит вообще. Те, кто мониторят, настраивают собственные инструменты, считают метрики по-разному и используют разные baseline — что приводит к недопониманию и путанице при обсуждении сетевых проблем.

В частности, существующие инструменты не показывают:

- Почему у валидатора высокий miss rate
- Исчерпана ли RAM или память GPU
- Перезапускаются ли ML или другие контейнеры в цикле
- Сколько времени занимает загрузка модели после рестарта
- Доступен ли PUBLIC_URL извне
- Сравнительную производительность между валидаторами

На практике валидаторы сталкивались с длительными периодами высокого miss rate или простоя инференса, не имея возможности определить причину. При этом у Core Team не было способа увидеть масштаб таких проблем по всей сети. Такие ситуации приводят к потере наград для операторов и замедленной реакции команды — проблемы, которые общая платформа мониторинга помогла бы обнаружить и решить значительно быстрее.

### Что происходит без решения

- Тихие отказы остаются незамеченными часами или днями — валидаторы теряют эпохи и награды
- Нет общей базы для отладки — каждый оператор использует разные инструменты, разные baseline, разные определения «нормы»
- У Core Team нет общей картины сети — сложнее диагностировать сетевые проблемы и планировать обновления
- Новые операторы предоставлены сами себе — высокий порог входа для мелких хостов без DevOps-экспертизы

---

## 3. Контекст индустрии

### Сбор метрик с валидаторов в единое место — не новая идея

Агрегация телеметрии и метрик от валидаторов в общий backend — устоявшаяся практика в блокчейн-индустрии. Множество крупных сетей уже это делают:

- Solana — валидаторы отправляют метрики в общий backend; сеть публикует публичный Grafana-дашборд на `https://metrics.solana.com:3000`
- Polkadot — ноды отправляют телеметрию по умолчанию в общий backend; публичный дашборд в реальном времени доступен на `https://telemetry.polkadot.io`
- Kusama — использует ту же систему Substrate Telemetry, что и Polkadot, с собственным представлением на `https://telemetry.polkadot.io/#list/Kusama`
- NEAR — каждая нода поставляется с дефолтным telemetry endpoint (`telemetry.nearone.org`) и отправляет данные каждые 10 секунд
- Aptos — все ноды отправляют метрики в централизованный telemetry-сервис (`telemetry.mainnet.aptoslabs.com`) по умолчанию; архитектура задокументирована в публичной SPEC
- Celestia — поддерживает OpenTelemetry collector endpoint (`otel.celestia.observer`) для DA-нод, плюс Prometheus-based observability stack для consensus-нод

Это не экзотическая идея. Именно так зрелые блокчейны получают видимость здоровья своей сети, быстрее диагностируют проблемы и принимают решения об обновлениях протокола на основе данных.

Во многих блокчейн-сетях телеметрия с нод собирается без полного ведома операторов — телеметрия часто включена по умолчанию в софте ноды, а в некоторых случаях у операторов вообще нет возможности её отключить.

В отличие от этого, Gonka Node Observability Platform спроектирована как полностью opt-in система — валидаторы сами решают, участвовать ли, и никакие данные не собираются без их явного действия.

Чем больше валидаторов подключится, тем точнее и полнее будет картина здоровья сети. Платформа с 30% подключённых валидаторов даёт полезные инсайты; платформа с 80% становится надёжным источником правды для всей экосистемы.

---

## 4. Предлагаемое решение

### Gonka Node Observability Platform

Managed open-source стек мониторинга, куда операторы валидаторов добровольно отправляют off-chain метрики на общую платформу, поддерживаемую INC4.

### Принципы дизайна

| Принцип | Реализация |
|---------|-----------|
| Open-source | Все экспортёры, дашборды, правила алертов и конфигурации будут open-source и доступны для аудита любыми заинтересованными лицами |
| Opt-in | Участие добровольное. Ни один валидатор не обязан делиться данными — но каждый участник делает платформу ценнее для всей сети |
| Push-based | Ноды отправляют метрики наружу через HTTPS. Никаких новых входящих портов. Существующие конфигурации firewall сохраняются |
| Не влияет на сеть | Платформа — отдельный слой. Она не взаимодействует с консенсусом, производством блоков или выполнением инференса. Сбой платформы имеет нулевое влияние на работу сети Gonka |
| Приватность | Платформа будет собирать только метрики, необходимые для понимания здоровья и производительности валидатора — такие как высота блока, статус синхронизации, miss rate, утилизация GPU, статус контейнеров, использование ресурсов и т.д. Никакая чувствительная информация собираться не будет — никаких приватных ключей, балансов кошельков, мнемонических фраз или учётных данных |

### Создаваемая ценность

Для Core Team:
- Агрегированные метрики и логи всей сети в одном месте
- Мгновенная видимость проблемных нод, эпох и временных периодов
- SLA-отчёты и принятие решений об обновлениях протокола на основе данных
- Поддержка реагирования на инциденты с анализом корневых причин

Для валидаторов:
- Не нужно строить и поддерживать собственный стек мониторинга
- Сравнение производительности своей ноды со средними показателями сети
- Получение алертов через Telegram или Discord при проблемах
- Возможность делиться логами для совместной диагностики при возникновении проблем
- Доступ к дашбордам с любого устройства, включая мобильный
- Практическая помощь в интерпретации метрик и диагностике инцидентов

Для сообщества:
- Единый источник правды для метрик здоровья сети
- Согласованные данные, на которые все участники могут ссылаться в обсуждениях
- Прозрачность сетевых операций

---

## 5. Технический подход

Платформа будет развёрнута на распределённой облачной инфраструктуре, что обеспечивает:

- Высокую доступность — отсутствие единой точки отказа; резервная инфраструктура с SLA 99.5%+ uptime
- Автоматическое масштабирование — платформа бесшовно растёт по мере подключения новых валидаторов, без ручного вмешательства
- Push-based сбор данных — валидаторы отправляют метрики наружу через HTTPS; никаких новых входящих портов не требуется, существующие конфигурации firewall полностью сохраняются

Мы будем использовать хорошо зарекомендовавшие себя, проверенные индустрией инструменты для мониторинга: Prometheus для сбора метрик, Grafana для дашбордов и визуализации, Alertmanager для уведомлений, Promtail/Loki для унифицированной добровольной агрегации логов и PagerDuty для управления инцидентами и эскалации дежурств.

INC4 имеет практический опыт создания и эксплуатации инфраструктуры мониторинга для блокчейн-сетей. Выбор каждого компонента стека продиктован реальными операционными требованиями — надёжность под нагрузкой, простота интеграции с существующими настройками валидаторов, минимальные ресурсные затраты на стороне ноды и возможность масштабирования без перестройки архитектуры по мере роста сети. Этот практический опыт напрямую определяет архитектурные и инструментальные решения, лежащие в основе данной платформы.

Детальная архитектура, включая конкретные определения метрик, потоки данных и спецификации экспортёров, будет задокументирована отдельно и будет эволюционировать по мере развития платформы.

---

## 6. Scope и Deliverables

| # | Deliverable | Описание |
|---|-------------|----------|
| 1 | Cloud-инфраструктура | Production-ready стек мониторинга на распределённой облачной инфраструктуре с высокой доступностью, резервированием, бэкапами и хранением данных |
| 2 | gonka-exporter | Open-source экспортёр, собирающий метрики Gonka-ноды и AI compute, поддерживаемый в актуальном состоянии с каждым релизом Gonka |
| 3 | Унифицированная добровольная агрегация логов | Поисковый сбор логов с Gonka-нод и ML-контейнеров — валидаторы, испытывающие проблемы, могут делиться логами для совместной диагностики с сообществом и Core Team |
| 4 | Внешние проверки доступности эндпоинтов | Автоматические проверки доступности валидаторов с независимых внешних точек |
| 5 | Fleet Overview Dashboard | Единое представление всей сети: статусы нод, miss rate, утилизация GPU, состояние синхронизации и тренды во времени |
| 6 | Individual Node Dashboard | Индивидуальное представление для каждого валидатора с историей производительности и сравнением со средними показателями сети |
| 7 | Кастомные дашборды | Дополнительные дашборды по запросу Core Team и индивидуальных валидаторов, итеративно улучшаемые на основе обратной связи от сообщества |
| 8 | Правила алертов и SLA-отчёты | Алертинг через Telegram, Discord и PagerDuty. Автоматические SLA-отчёты для валидаторов и Core Team |
| 9 | Документация онбординга | Пошаговый гид для валидаторов по подключению к платформе |
| 10 | Онбординг валидаторов | Практическая помощь в подключении с выделенным инженером на этапе первоначального развёртывания, далее — постоянная поддержка новых валидаторов |
| 11 | Реагирование на инциденты и консультации | Помощь индивидуальным валидаторам и Core Team в интерпретации метрик, диагностике инцидентов, анализе корневых причин и разборе инцидентов |
| 12 | Постоянная поддержка | Выделенная DevOps-команда, обеспечивающая надёжность платформы, совместимость с обновлениями Gonka и непрерывное операционное улучшение |

---

## 7. Бюджет и график выплат

### Сводка

| Категория | Годовая стоимость | Обоснование |
|-----------|------------------|-------------|
| Облачная инфраструктура | \$18,000 | ~\$1,500/мес за managed Prometheus (хранение и запросы метрик), Grafana (дашборды и визуализация), Alertmanager (уведомления), Promtail/Loki (унифицированная добровольная агрегация логов), PagerDuty (управление инцидентами и эскалация дежурств), внешние проверки доступности эндпоинтов и вспомогательную инфраструктуру, включая retention метрик, хранение логов и отказоустойчивую конфигурацию с резервированием |
| Операционная поддержка и обслуживание инфраструктуры | \$36,000 | DevOps-команда с суммарной аллокацией 0.5 FTE (~\$3,000/мес) для операционной поддержки платформы, реагирования на инциденты, проверки совместимости после обновлений сети Gonka, планирования ёмкости, дежурной поддержки, резервного копирования и аварийного восстановления, оптимизации производительности, управления доступами подключённых валидаторов, поддержки infrastructure-as-code и самомониторинга платформы |
| Разработка и обновление экспортёров | \$12,000 | Разработка и поддержка gonka-exporter (метрики Gonka-ноды и AI compute), конфигураций сбора логов Promtail, Blackbox exporter probes, интеграция с node_exporter и экспортёрами GPU-метрик, а также постоянные обновления совместимости под новые релизы Gonka. Реализация ряда продвинутых метрик может потребовать изменений в софте Gonka-ноды — INC4 будет сотрудничать с Core Team для проработки и реализации необходимых расширений API |
| Кастомные дашборды и кастомные алерты | \$12,000 | Общесетевой и индивидуальные дашборды, правила алертов с уведомлениями в Telegram и Discord, SLA-отчёты, разработка кастомных дашбордов по запросу Core Team, персонализированных дашбордов для индивидуальных валидаторов по запросу, а также итеративные улучшения на основе постоянного взаимодействия с сообществом валидаторов |
| Онбординг валидаторов, реагирование на инциденты и консультации | \$18,000 | Первые 3 месяца: выделенный DevOps-инженер для практического онбординга первых валидаторов и сквозной настройки системы. Далее: поддержка документации, помощь новым валидаторам в подключении, практическая помощь индивидуальным валидаторам и Core Team в интерпретации метрик, диагностике инцидентов, координации устранения проблем, анализ корневых причин, рекомендации по исправлению и разбор инцидентов для сетевых событий |
| Итого запрос | \$96,000 | |

### График выплат

| Транш | Период | Сумма | Покрывает |
|-------|--------|-------|-----------|
| 1 | Месяцы 1–3 | \$51,000 | Развёртывание и настройка облачной инфраструктуры, разработка основных экспортёров и дашбордов, выделенный DevOps-инженер для онбординга первых валидаторов |
| 2 | Месяцы 4–6 | \$15,000 | Операционная поддержка, обслуживание, реагирование на инциденты, поддержка валидаторов и продолжение разработки кастомных дашбордов и правил алертов |
| 3 | Месяцы 7–9 | \$15,000 | Операционная поддержка, обслуживание, реагирование на инциденты, поддержка валидаторов и итеративные улучшения экспортёров и дашбордов на основе обратной связи от валидаторов |
| 4 | Месяцы 10–12 | \$15,000 | Операционная поддержка, обслуживание, реагирование на инциденты, поддержка валидаторов и отчёт об использовании и adoption по итогам года |

Каждый транш выплачивается первого числа соответствующего периода.

Первый транш больше, так как покрывает развёртывание инфраструктуры и наиболее интенсивную фазу разработки проекта.

### Риски

- Низкое подключение валидаторов — INC4 будет активно поддерживать онбординг и демонстрировать ценность платформы через первых участников
- Рост стоимости инфраструктуры — бюджет включает резерв; при необходимости возможна миграция на более экономичное решение без прерывания сервиса
- Платформа не влияет на работу сети Gonka — она работает как полностью отдельный слой; любая проблема платформы имеет нулевое влияние на валидаторов и консенсус

Бюджет рассчитан на один год. После первого года условия могут быть пересмотрены и продлены на тех же или скорректированных условиях. INC4 опубликует прозрачный отчёт об использовании платформы, adoption и расходах по итогам грантового периода — давая сообществу чёткую основу для решения о продлении. Если сообщество решит не продлевать, полностью настроенная и работающая платформа — включая всю инфраструктуру, код и конфигурации — может быть передана сообществу или Core Team.

---

## 8. Критерии успеха

Что поставляет INC4:
- Базовая версия платформы развёрнута и принимает метрики — в течение первой недели, с непрерывными улучшениями и обновлениями в дальнейшем
- Экспортёр, общесетевой дашборд и алертинг доступны в базовой версии — в течение первого месяца, с непрерывным улучшением на протяжении всего грантового периода
- INC4 будет активно помогать валидаторам, желающим подключиться — обеспечивая практическую поддержку онбординга наряду с документацией в GitHub-репозиториях
- Весь код, конфигурации и дашборды опубликованы в публичных GitHub-репозиториях — открыты для просмотра, аудита и контрибуций от любого желающего

Что зависит от сообщества:
- INC4 будет активно поддерживать онбординг, но не может гарантировать уровень adoption, так как участие добровольное
- Цель: широкое adoption по сети в течение первого года
- Sunshine-сценарий: подключение к платформе становится неотъемлемой частью настройки каждого валидатора

Ключевые показатели эффективности:
- Доступность платформы: 99%+ uptime на протяжении всего грантового периода
- Совместимость: платформа проверена и работоспособна в течение 48 часов после каждого обновления сети Gonka
- Онбординг: любой валидатор может подключиться к платформе менее чем за 30 минут, используя предоставленную документацию
- Отчётность: квартальные отчёты о прогрессе, публикуемые для сообщества
- Adoption: широкое adoption по сети в течение первого года

---

## 9. Команда

- Сайт: https://inc4.net
- GitHub: https://github.com/inc4

INC4 — активный участник экосистемы Gonka. Мы эксплуатируем валидаторы на mainnet и testnet, разрабатываем приложения для сети Gonka. Этот proposal вырос из нашего прямого опыта — мы сами столкнулись с отсутствием общесетевой видимости как операторы валидаторов и хотим решить эту проблему для всей сети.

INC4 вовлечён в несколько инициатив в экосистеме Gonka — платформа наблюдаемости лишь одна из них. Например, мы также разрабатываем NOP (Node Onboarding Package) — open-source утилиту для быстрого запуска валидаторов (https://github.com/inc4/gonka-nop). Наше участие в сети — долгосрочное и не ограничивается данным proposal.

Как компания, INC4 основана в 2013 году, 70+ инженеров и 230+ реализованных проектов в блокчейн-инфраструктуре и AI-системах. Практический опыт в создании и поддержке майнинг-инфраструктуры для Bitcoin, Ethereum, Filecoin.

### Комментарий 2 — [@andrey055](https://github.com/andrey055)

*2026-04-16 19:19 UTC*

Hi guys, I’ve had experience working with you before, and in any case I sincerely wish you success and hope you remain with Gonka.

May I kindly ask whether it would be possible to cancel any of the future tranches if plans were to change later on?

### Комментарий 3 — [@rwxr-xr-x](https://github.com/rwxr-xr-x)

*2026-04-16 19:21 UTC*

Vesting Contract: https://github.com/rwxr-xr-x/gonka-usdt-vesting-schedule

### Комментарий 4 — [@rwxr-xr-x](https://github.com/rwxr-xr-x)

*2026-04-18 07:51 UTC*

This is a cover letter for a funding request. It typically includes a high-level overview of problem statement and proposed solution, without too much detailed information on the budget or technical implementation.

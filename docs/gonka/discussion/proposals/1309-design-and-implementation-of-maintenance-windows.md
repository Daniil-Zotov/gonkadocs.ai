---
title: "#1309 — Design and Implementation of Maintenance Windows"
source: https://github.com/gonka-ai/gonka/discussions/1309
discussion_number: 1309
category: proposals
synced_at: 2026-06-25T20:23:15Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1309](https://github.com/gonka-ai/gonka/discussions/1309) каждые 6 часов. 

# Design and Implementation of Maintenance Windows

**Автор:** [@heitor-lassarote](https://github.com/heitor-lassarote) · **Категория:** :bulb: Proposals · **Создано:** 2026-06-05 16:40 UTC · **Обновлено:** 2026-06-09 16:54 UTC

---

## 📝 Описание

Hello. After reading the [Gonka Community Network Roadmap](https://docs.google.com/document/d/1wPXTM40CnXyd8Hz_dvf7H1n6KQDqjw0RzppMx92xR8U/edit?pli=1&tab=t.0#heading=h.c2j5tayw22w8), we’ve seen project 2 in track 3 entitled “Maintenance windows for hosts”, which as of 2026-03-06 has the following description (copied and pasted here):

---

The project should give a host a way to declare a maintenance window in advance, check whether the maintenance window is allowed, temporarily step out of part of its duties, and return to service without separate coordination and without being penalized for planned downtime.

**Metrics:**

- **PRIMARY:** host retention and confidence.
- **SECONDARY:** network reliability and trust.

**What this gives the network:**

The network gets a formal maintenance-window process that separates planned downtime from unplanned failures and reduces avoidable misses, penalties, and disputes.

---

A possible high-level design outline for this project may look like the following:

1. Create a new message, such as `MsgSetScheduledMaintenance`, allowing the host to schedule expected maintenance downtime and broadcast it to the mainnet. The exact fields in this message are up for debate, but it should at least contain a timestamp for when the maintenance begins (e.g.: `maintenance_start_timestamp`).
    1. The mainnet should change the status of the participant: to `DRAINING` prior to the maintenance (host will finalize their ongoing sessions but won’t participate in new ones) and to `MAINTENANCE` (the host is temporarily offline due to scheduled maintenance). There might be the necessity for more statuses and transitions in this state machine, which should be researched.
        1. The `DRAINING` time may be tuned, but a good start may be for example, at least for an entire epoch, as a devshard session currently can’t cross the epoch boundary.
    2. The chain should not assign inference or validation requests for this participant if it’s too close to a scheduled maintenance time and neither it should place the participant in devshards.
    3. There should be a minimum delay until the participant can schedule a new maintenance window. For example, a host should not be able to assign a maintenance window just 1 minute from `MsgSetScheduledMaintenance`, to prevent abuse.
    4. During the maintenance window, the host must not be penalized for missed inferences, validations, or related. However, it’s possible the host may come offline and take a very long time to perform maintenance, or never return at all. Hence, there should be a maximum allowed time for the maintenance windows. If the time is exceeded, the host should be penalized as usual and the maintenance should be considered finished. The slashing may use the current downtime/invalidation penalties in this case.
2. A new message indicating that it has finalized the scheduled maintenance, for example, `MsgFinishScheduledMaintenance`.
    1. The host should pay attention to the maximum allotted time for maintenance.
3. A new message in case the host may change its mind and decide to not have the maintenance, for example, `MsgCancelScheduledMaintenance`.
    1. In other words, `MsgFinishScheduledMaintenance` should be sent *during* the scheduled maintenance window to let the participant close the window and resume its ordinary activities, while `MsgCancelScheduledMaintenance` should be sent *before* the scheduled maintenance window to prevent it from ever beginning.

There are still some open questions and considerations that need research with this design:

1. It’s possible for a host to abuse if it cancels its maintenance window to a time that is very close to its start. How should we penalize it?
2. Related to question 2, how should we penalize a host that cancels its maintenance window shortly after it began?
3. What should be the cooldown period between maintenance windows?
4. How many windows should be allowed per host during an epoch?
5. What is an acceptable maximum timestamp for maintenance, before the host is considered gone?

We would like to offer a team to refine the idea and design and begin work on this project. A tentative plan for the team should look like the following:

1. First research and improve the design. Iron all possible open questions, think how to prevent abuse of this mechanism and slash for detected attempts, architect the possible design for the messages, consider the possible changes for the devshards, etc..
2. Implement the design decided during the first step, simultaneously adding tests following the best practices for testing and documentation.
3. Write integration tests using testermint, testing the happy paths and unhappy paths, including tests of hosts trying to cheat the system.
4. Clearly document how to hand this feature to the community and the Gonka team.
5. [Optional] Provide continuous support and maintenance for this feature.

---

## 💬 Комментарии (1)

### Комментарий 1 — [@patimen](https://github.com/patimen)

*2026-06-09 16:21 UTC*

We have an implementation of this feature already out for review and testing:
https://github.com/gonka-ai/gonka/pull/998

**↳ Ответ от [@heitor-lassarote](https://github.com/heitor-lassarote)** · *2026-06-09 16:54 UTC*

> I see, thank you for bringing this to my attention. I'll close this discussion, then.

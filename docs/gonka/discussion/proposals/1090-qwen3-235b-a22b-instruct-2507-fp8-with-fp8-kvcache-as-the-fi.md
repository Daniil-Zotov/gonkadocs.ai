---
title: "#1090 — Qwen3-235B-A22B-Instruct-2507-FP8 with FP8 KVcache as the first multi model PoC launch model"
source: https://github.com/gonka-ai/gonka/discussions/1090
discussion_number: 1090
category: proposals
synced_at: 2026-06-17T05:17:41Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1090](https://github.com/gonka-ai/gonka/discussions/1090) каждые 6 часов. 

# Qwen3-235B-A22B-Instruct-2507-FP8 with FP8 KVcache as the first multi model PoC launch model

**Автор:** [@beatifull](https://github.com/beatifull) · **Категория:** :bulb: Proposals · **Создано:** 2026-04-18 06:46 UTC · **Обновлено:** 2026-04-18 06:49 UTC

---

## 📝 Описание

Hello, I'm a gonka host with almost half a year of experience.

Motivation - I would like to suggest a first model to test multi model PoC, which will fit my setup and prepare the network for the smooth multi model PoC launch. I know the main goal: provide models to consumers that are in demand, but this is a nice option to test everything and make life for hosts easier.
This will boost PCI-E cards, especially: **4x H100 PCI-E** with two NVLINK islands with TP=2.

High-Level Solution - Enable Qwen3-235B-A22B-Instruct-2507-FP8 with FP8 kvcache as the first multi model PoC launch model.

Implementation: Just enable it as  a first option in multi-model PoC

Roadmap - I think this is a nice option to test multi model PoC and make life of hosts easier. The same model, but with a different configuration.

Open Questions - This will make life easier for users with PCI-E setup and nvlink islands, like me. Because BF16 kvcache can't fit with TP=2 setup, and I get a lot of "MISS" penalties if I enable FP8 KVcache.

But I'm not sure if this is in demand by users or gonka developers.


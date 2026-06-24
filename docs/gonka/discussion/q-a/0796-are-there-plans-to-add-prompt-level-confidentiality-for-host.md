---
title: "#796 — Are there plans to add prompt-level confidentiality for hosts?"
source: https://github.com/gonka-ai/gonka/discussions/796
discussion_number: 796
category: q-a
synced_at: 2026-06-24T09:51:46Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #796](https://github.com/gonka-ai/gonka/discussions/796) каждые 6 часов. 

# Are there plans to add prompt-level confidentiality for hosts?

**Автор:** [@AlexKorovyansky](https://github.com/AlexKorovyansky) · **Категория:** :pray: Q&A · **Создано:** 2026-02-24 19:20 UTC · **Обновлено:** 2026-02-27 19:09 UTC

---

## 📝 Описание

I've been reading the whitepaper and comparing Gonka's architecture with other decentralized inference networks (specifically Cocoon/TON, which uses Intel TDX trusted execution environments).

One thing I noticed is that while Gonka anonymizes the user's IP by routing requests through an intermediary host, the executing host still has access to the raw prompt and response content. For use cases involving personal AI assistants (e.g. agents that process emails, calendar data, private documents), this is a significant privacy gap.

Are there any plans to address this in future releases? For example:
- TEE support (Intel TDX, AMD SEV, NVIDIA Confidential Computing)
- Homomorphic or hybrid encryption schemes for inference
- Any other approach to ensure hosts cannot read the data they compute on

Otherwise, it could be a blocker to leverage gonka for agentic use-cases. 

Thanks!

---

## ✅ Выбранный ответ

**От:** [@gmorgachev](https://github.com/gmorgachev) · *2026-02-24 19:51 UTC*

Hi! We thought these approaches, homomorphic/hybrid encryptions seems like not yet ready technologies for production usage on real size model. But it's really promising approach from my perspective  

The TEE is the approach which can be added to the chain with not that much efforts. There is a document with the high-level vision how we can add TEE to the chain https://github.com/gonka-ai/gonka/tree/gm/tee/proposals/tee

From my perspective it should be additional type of inference, with higher price. In parallel with usual one. It'll enable production companies with high requirements to use Gonka with higher fee but price for users without such requirements will be the lowest possible

---

## 💬 Комментарии (1)

### Комментарий 1 ✅ — [@gmorgachev](https://github.com/gmorgachev)

*2026-02-24 19:51 UTC*

Hi! We thought these approaches, homomorphic/hybrid encryptions seems like not yet ready technologies for production usage on real size model. But it's really promising approach from my perspective  

The TEE is the approach which can be added to the chain with not that much efforts. There is a document with the high-level vision how we can add TEE to the chain https://github.com/gonka-ai/gonka/tree/gm/tee/proposals/tee

From my perspective it should be additional type of inference, with higher price. In parallel with usual one. It'll enable production companies with high requirements to use Gonka with higher fee but price for users without such requirements will be the lowest possible

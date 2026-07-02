---
title: "#1363 — OpenBroker - broker for brokers or Devshards as a service."
source: https://github.com/gonka-ai/gonka/discussions/1363
discussion_number: 1363
category: show-and-tell
synced_at: 2026-07-02T04:31:27Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1363](https://github.com/gonka-ai/gonka/discussions/1363) каждые 6 часов. 

# OpenBroker - broker for brokers or Devshards as a service.

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-06-23 22:18 UTC · **Обновлено:** 2026-06-23 22:23 UTC

---

## 📝 Описание

Hey! **Gonka Labs** here. 

We've just shipped **OpenBroker**, a platform that gives you direct access to gonka inference - pure devshards v1, v2 (and any future version) under wallet that is whitelisted to operate escrows. You get escrow capacity that scales elastically with your load, both devshard versions (and any future one), and throughput limited only by what the network itself can handle.

With OpenBroker - we make a community commitment to the overall observability and monitoring (**Protocol-grade observability**).

**OpenBroker doubles as a live testbed where new devshard versions get exercised at production scale before they reach the wider network, and the observanility metrics we collect goes straight back to the protocol's contributors that we in-touch with to keep improving Gonka.** 

Full observability means that per-request metrics, public network stats and QOL inference metrics - are part of the product, not an afterthought. We work directly with the protocol's contributors to feed back the statistics, failure modes and performance data we see at real scale, so Gonka keeps getting better. It's also the environment where new devshard versions get shaken out at production load before they ship to everyone. If you've been using `node4` to prototype or create your own Broker business and test against Gonka, **OpenBroker is the next logical step and same "just hit an endpoint and go" experience, no diffrence** *(except that you can enroll and get access right away)* - with bigger capacity, real telemetry, and both protocol versions available out of the box, all in a managed environment.

<img width="1369" height="798" alt="Снимок экрана — 2026-06-23 в 23 49 45" src="https://github.com/user-attachments/assets/139473c5-b0bf-4a1c-8e89-913d1c379ebc" />



### The problem

Running inference on Gonka today means either:

- Using **`node4`** **node4** (whitelisted, rate-limited, built for demos not production), or
- Becoming devshard/escrow operator - enroll your wallet to operate escrows, fund, rotate escrows, handle v1/v2 state roots, handle operator complexities (no settlement, etc). A lot of glue code just to send a chat completion.

So, if you want to become a broker, you need to get whitelisted for escrow operations or get broker key and connect to node4.

Either way makes it very hard for new brokers to start operating, raising the bar and lowering potential inference demand.



### The Solution

**OpenBroker** is "a few devshard containers (v1, v2) + many escrows" system that sits in front of the Gonka network and exposes a plain devshard infra with our whitelisted wallet. Just as inteded to be used by brokers, but without need to whitelist a wallet or enroll to get a broker key. 

From the broker's side:

1. **Register** at [https://openbroker.gonka.gg/register](https://openbroker.gonka.gg/register) - email, org name, your `gonka1…` wallet.
2. **Deposit GNK** to your generated address (activation kicks in at 100 GNK).
3. **Grab your API key** (`obk-*`) from the dashboard.
4. **Point any OpenAI client** at:

   ````
   https://openbroker.gonka.gg/v1
   ````

   That's it. `/v1/chat/completions`, `/v1/models`, streaming + non-streaming, no rate limits, pure devshards.


<img width="1479" height="902" alt="Снимок экрана — 2026-06-23 в 23 53 42" src="https://github.com/user-attachments/assets/9be86275-d12e-4525-a910-d43af6bdc9fa" />


### What you get

- **Unlimited throughput** - as much as network can handle - you can send with OpenBroker's help.
- **GNK billing, NO MARKUP** - watch the ledger drain in real time on your dashboard.
- **Fully managed escrows** - we fund, register, rotate, secure escrows for you, including proactive replacement before they deplete bellow safe minimum.
- **v1 + v2 (and future) protocol support** side-by-side, transparent to the caller, auto-routed.
- **Live, public stats** - see your usage and the whole network's at [https://openbroker.gonka.gg/stats](https://openbroker.gonka.gg/stats).
- **OpenAI-compatible** - drop-in for LangChain, LlamaIndex, OpenAI SDK, anything that speaks OpenAI. Or just become your own broker and resell inference (you "buy" without any additional costs or markup, OpenBroker deducts ledger 1-to-1 with what escrows cost) 

  


### Scale we've tested

We've load-tested OpenBroker past **1,000,000,000 (1 billion) tokens in a single run (a little over 1 hour total test run time)** across Qwen, MiniMax and Kimi models - no node4 fallback, escrows auto-rotating, v1/v2 traffic split live. Production-grade throughput is the goal.


<img width="1477" height="892" alt="Снимок экрана — 2026-06-23 в 23 54 05" src="https://github.com/user-attachments/assets/7bc65f36-43c2-4897-8225-f1bbd5d9e52a" />





### Links

- **Become a broker:** [https://openbroker.gonka.gg](https://openbroker.gonka.gg)
- **Live stats:** [https://openbroker.gonka.gg/stats](https://openbroker.gonka.gg/stats)
- **Gonka Labs:** [https://gonkalabs.com](https://gonkalabs.com)

Would love feedback, feature requests, and bug reports. If you build something on top of OpenBroker, drop it in this thread 🙌

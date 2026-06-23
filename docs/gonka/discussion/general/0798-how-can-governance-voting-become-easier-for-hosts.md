---
title: "#798 — How can governance voting become easier for Hosts?"
source: https://github.com/gonka-ai/gonka/discussions/798
discussion_number: 798
category: general
synced_at: 2026-06-23T10:04:00Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #798](https://github.com/gonka-ai/gonka/discussions/798) каждые 6 часов. 

# How can governance voting become easier for Hosts?

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Категория:** :speech_balloon: General · **Создано:** 2026-02-24 21:46 UTC · **Обновлено:** 2026-03-06 23:47 UTC

---

## 📝 Описание

Hi everyone, the goal of this thread is to increase governance participation and voter turnout. Feedback is needed on what would make voting easier to notice, faster to understand, and simpler to complete.

**What currently blocks participation**

If recent votes were skipped, what were the main reasons?
- The vote was not noticed in time
- The voting window was too short
- The proposal summary was not clear enough to decide quickly
- Too much context was required to evaluate impact and risk
- Voting felt too manual and easy to miss (ops workload, timezones, tooling)
- It was unclear whether an individual's vote matters

**What would increase turnout**

Please share what would actually help.

1. Voting window length
- Would a longer voting period increase participation?
- If yes, what duration feels reasonable?

2. Earlier notification
- How early should votes be announced to be useful?
- Which channels work best (Discord, GitHub, Telegram, other)?

3. What format helps to decide faster?
- TLDR in 3 to 5 lines
- “What changes for Hosts and miners”
- Risks and tradeoffs
- Concrete examples (numbers, scenarios)

4. Mandatory voting for Hosts. This option has obvious tradeoffs and it would be useful to understand likely behavior.
- Would participation increase if Host voting were required?
- Would automated voting be set up?
- If automation becomes common, does it improve governance quality or mostly inflate turnout?

What makes it easy today? Any workflow or tooling recommendations are welcome.

Goal of this discussion: identify concrete, low-friction changes that increase turnout without turning governance into a checkbox process.

Thanks for sharing specifics - what should change and why.

---

## 💬 Комментарии (3)

### Комментарий 1 — [@Aktum1](https://github.com/Aktum1)

*2026-02-27 08:11 UTC*

1. I'd like to see a video review of each propnode with an in-depth analysis of each proposed change. 

2. The voting window doesn't need to be increased. 

3. I think we could impose a penalty for not voting, say 10% of the rewards for the next 30 epochs. Voting is not a right, but an obligation. 

4. A mechanism for delegating voting rights could be developed. 

5. Wallets with voting functionality, in my opinion, are unnecessary, since all miners know how to use the CLI and they certainly don't want to import their seed phrases into any third-party applications.


------------
1. Хотелось бы увидеть видеообзор каждого пропоузела с подробным анализом каждого предлагаемого изменения.

2. Окно голосования увеличивать не нужно.

3. Думаю, можно ввести штраф за неучастие в голосовании, например, 10% от вознаграждения за следующие 30 эпох. Голосование — это не право, а обязанность.

4. Можно разработать механизм делегирования прав голоса.

5. Кошельки с функцией голосования, на мой взгляд, излишни, поскольку все майнеры умеют пользоваться CLI и, конечно же, не хотят импортировать свои сид-фразы в сторонние приложения.

**↳ Ответ от [@tcharchian](https://github.com/tcharchian)** · *2026-03-06 23:47 UTC*

> > I think we could impose a penalty for not voting, say 10% of the rewards for the next 30 epochs. Voting is not a right, but an obligation.
>
> In such cases, some operators may choose to set up a simple script to automatically vote `No` to avoid missing the voting window and potentially losing rewards.
>
> > A mechanism for delegating voting rights could be developed.
>
> You are right. Some node operators do not have access to the cold key and therefore cannot vote directly for the node. At the same time, the owner of the cold key may not always be available during the voting window. Since the governance voting period is relatively short, it can make sense to grant voting permission in advance, as shown in the example below.
>
> Here is the guide on how to grant permission for voting on your behalf: https://gonka.ai/FAQ/#what-should-i-do-if-i-cannot-vote-because-i-do-not-have-access-to-the-cold-key-or-if-i-want-another-key-to-vote-on-my-behalf

### Комментарий 2 — [@SY-MEDIA](https://github.com/SY-MEDIA)

*2026-02-27 10:21 UTC*

Would love to vote, but as far as I can tell, I'm excluded due to an exploited design bug. My node can't participate even for unpaid inference. As far as I know, unless a node is on the whitelist it can't vote. 

If I could vote, I'd vote even though I feel the voting has been rendered almost pointless by the fact that voters are now all a single demographic. Because only a very large model is possible to run on the system, voting would tend to be in favour of that one population and one income stream. 

### Комментарий 3 — [@Laboltus](https://github.com/Laboltus)

*2026-03-04 11:18 UTC*

The 24-hour voting period is too short, especially on weekends/holidays. And I think any proposal should include a detailed explanation of why it's important.

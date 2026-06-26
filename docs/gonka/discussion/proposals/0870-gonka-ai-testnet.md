---
title: "#870 — Gonka AI Testnet"
source: https://github.com/gonka-ai/gonka/discussions/870
discussion_number: 870
category: proposals
synced_at: 2026-06-26T09:52:41Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #870](https://github.com/gonka-ai/gonka/discussions/870) каждые 6 часов. 

# Gonka AI Testnet

**Автор:** [@Alert17](https://github.com/Alert17) · **Категория:** :bulb: Proposals · **Создано:** 2026-03-06 17:14 UTC · **Обновлено:** 2026-05-01 15:45 UTC

---

## 📝 Описание

# Gonka Testnet - Permanent Parallel Network for Consumer GPU Participation

## Motivation

Gonka mainnet requires **320 GB VRAM** per ML Node (e.g. 4×H100 80 GB), limiting participation to datacenter-grade multi-GPU setups. Consumer and prosumer GPUs - RTX 3090, RTX 4090, A6000 - are excluded entirely despite being capable compute devices.

This creates three concrete problems:

- **Lost participants.** Hosts who invested in hardware and contributed to the network were locked out as VRAM requirements increased with PoC V2 and the transition to Qwen3-235B.
- **No onboarding path.** New users cannot try operating a Gonka node without committing $100K+ in datacenter hardware. There is no way to learn the protocol, test configurations, or evaluate the economics before going all-in.
- **No staging environment.** Protocol upgrades, model changes, and parameter adjustments are deployed directly to mainnet with no parallel network for validation.

-----

## High-Level Solution

A **permanent parallel Cosmos chain** (`gonka-testnet-1`) running the exact same Gonka protocol with a lighter inference model, opening participation to GPUs with **24 GB+ VRAM**.

### Design Principle: Identical Protocol, Different Scale

The testnet runs the same blockchain as mainnet. No protocol modifications, no alternative reward systems, no different collateral mechanics. The chain code is a direct fork of the mainnet codebase - any upgrade tested on testnet deploys to mainnet via Cosmovisor without modification.

|Parameter          |Mainnet                          |Testnet                           |
|-------------------|---------------------------------|----------------------------------|
|chain-id           |`gonka-mainnet`                  |`gonka-testnet-1`                 |
|Token denom        |`gnk`                            |`tgnk`                            |
|Total supply       |1,000,000,000 GNK                |1,000,000,000 tGNK                |
|Miner allocation   |800,000,000 GNK (80%)            |800,000,000 tGNK (80%)            |
|Founder allocation |200,000,000 GNK (20%)            |200,000,000 tGNK (20%)            |
|Min VRAM per MLNode|320 GB (multi-GPU)               |24 GB (single GPU)                |
|Inference model    |Qwen3-235B-FP8                   |Qwen2.5-14B-Instruct (recommended)|
|Emission formula   |`323,000 × e^(-0.000475 × epoch)`|Same formula, same decay          |
|Collateral         |Required (after 180-epoch grace) |Same mechanism                    |
|PoC V2             |1-10% random verification        |Same mechanism                    |
|Sprint PoW         |Continuous nonce generation      |Same mechanism                    |
|Governance (x/gov) |Active                           |Same mechanism                    |

### Hardware Requirements

**Minimum VRAM: 24 GB.** This covers RTX 3090 and RTX 4090 as entry-level, while excluding cards that cannot run the target model class (7B-14B parameters).

|GPU         |VRAM |Category           |Expected Performance                              |
|------------|-----|-------------------|--------------------------------------------------|
|RTX 3090    |24 GB|Minimum            |Runs model with limited headroom; lower nonce rate|
|RTX 4090    |24 GB|Minimum            |Higher compute; faster nonces                     |
|A5000       |24 GB|Prosumer           |Datacenter-class reliability                      |
|A6000 / L40 |48 GB|Optimal            |Comfortable VRAM margin; high nonce rate          |
|A100 (40 GB)|40 GB|Optimal            |Datacenter performance on lighter model           |
|2×RTX 4090  |48 GB|Optimal (multi-GPU)|Combined VRAM; tensor parallelism possible        |

More powerful GPUs naturally generate more nonces per epoch due to higher throughput - no artificial weight multipliers. Same Sprint mechanism as mainnet.

### Model Selection

The testnet model must be: (1) small enough for 24 GB VRAM, and (2) large enough that users cannot trivially run it without the Gonka infrastructure.

|Model                   |Params   |FP16 VRAM |FP8 VRAM  |24 GB Fit?    |48 GB Fit? |
|------------------------|---------|----------|----------|--------------|-----------|
|Qwen2.5-7B-Instruct     |7.6B     |~15 GB    |~8 GB     |✅ FP16        |✅          |
|**Qwen2.5-14B-Instruct**|**14.8B**|**~30 GB**|**~15 GB**|**⚠️ FP8 only**|**✅ FP16** |
|Llama-3.1-8B-Instruct   |8.0B     |~16 GB    |~8 GB     |✅ FP16        |✅          |
|Mistral-Small-24B       |24B      |~48 GB    |~24 GB    |⚠️ FP8 tight   |✅ FP16     |
|Qwen2.5-32B-Instruct    |32.5B    |~65 GB    |~33 GB    |❌             |⚠️ FP8 tight|

**Recommendation: Qwen2.5-14B-Instruct.** Fits on 24 GB only with FP8 quantization (tight, not trivial), runs comfortably on 48 GB in FP16. Well-supported by vLLM, strong benchmarks. Alternative: Qwen2.5-7B as safer launch option, upgradeable to 14B via Cosmovisor.

-----

## Economic Model

### Emission

Identical to mainnet: `R(epoch) = 323,000 × e^(-0.000475 × epoch)`

At testnet genesis (epoch 0): 323,000 tGNK/epoch. Halving every ~1,459 epochs (~4.16 years). Total emission converges to ~680,000,000 tGNK.

|Milestone|tGNK Mined |Epoch |Time       |Epoch Emission|
|---------|-----------|------|-----------|--------------|
|25% mined|170,000,000|~606  |~1.7 years |~242,000 tGNK |
|50% mined|340,000,000|~1,459|~4.2 years |~161,500 tGNK |
|75% mined|510,000,000|~2,918|~8.3 years |~80,750 tGNK  |
|90% mined|612,000,000|~4,847|~13.8 years|~32,300 tGNK  |
|99% mined|673,000,000|~9,694|~27.7 years|~3,230 tGNK   |

### tGNK → GNK Conversion

**This is the core economic link between testnet and mainnet.**

A pool of **1,000,000 GNK** (proposed) is allocated from the Community Pool (120M GNK, ~0.83%) via governance. The conversion uses a fixed rate derived from total emission cap:

```
GNK = Your tGNK × 0.00147
```

Expanded: `GNK = (Your tGNK / 680,000,000) × 1,000,000`

**How this works:**

- **Your tGNK** - the tGNK you burn for conversion (earned by mining)
- **680,000,000** - total tGNK that will ever be mined via emission (fixed constant from decay formula, does not change over time)
- **1,000,000 GNK** - mainnet pool backing all conversions
- **Rate: 0.00147 GNK per tGNK** - fixed, same for early and late miners. No rush incentive, no timing games

### Worked Examples

Since the rate is fixed, the only variable is how much tGNK a miner earns (depends on network size and time):

**Scenario A:** 100 GPUs, 3 months (~90 epochs). RTX 4090 earning ~1% share → ~285,000 tGNK mined.

```
GNK = 285,000 × 0.00147 = ~419 GNK (~$352)
```

**Scenario B:** 500 GPUs, 6 months (~180 epochs). RTX 4090 earning ~0.2% share → ~111,600 tGNK.

```
GNK = 111,600 × 0.00147 = ~164 GNK (~$138)
```

**Scenario C:** 1,000 GPUs, 12 months (~350 epochs). RTX 4090 earning ~0.1% share → ~104,000 tGNK.

```
GNK = 104,000 × 0.00147 = ~153 GNK (~$129)
```

### Monthly Income Estimates (500 GPU network)

|GPU     |VRAM |tGNK (6 months)|GNK |USD (~$0.84)|Per Month|
|--------|-----|---------------|----|------------|---------|
|RTX 3090|24 GB|~67,000        |~98 |~$82        |~$14/mo  |
|RTX 4090|24 GB|~112,000       |~164|~$138       |~$23/mo  |
|A6000   |48 GB|~179,000       |~263|~$221       |~$37/mo  |
|2×4090  |48 GB|~223,000       |~328|~$276       |~$46/mo  |

Electricity for RTX 4090 (~150W) is ~$15-20/mo. Income exceeds operating costs while remaining modest enough to avoid speculative farming.

### Self-Balancing Properties

- **More miners → smaller share per GPU → lower GNK income → rental unprofitable → only hardware owners remain**
- **Fewer miners → larger share → higher income → attracts new participants → network grows**
- **Fixed rate = no timing games.** A tGNK mined in month 1 is worth the same as one mined in month 12
- **Pool depletion is predictable:** after 50% of tGNK is mined (~4.2 years), 50% of pool is consumed

### Post-Emission: Transition to Work Coins

As emission decays, miners rely increasingly on Work Coins - direct payments from developers for inference:

|Phase   |Reward Coins (Emission)|Work Coins (Inference)|
|--------|-----------------------|----------------------|
|Year 0-2|~90% of income         |~10%                  |
|Year 2-5|~50%                   |~50%                  |
|Year 5+ |~20% and declining     |~80%                  |
|Year 10+|Negligible             |~100%                 |

**Critical question at each phase:** is developer demand growing fast enough to replace declining emission?

### Pool Sustainability

When the pool depletes, the community decides:

1. **Replenish** - new governance proposal for additional GNK from Community Pool
2. **Work Coins only** - if inference marketplace is active, pool may not be needed
3. **Adjust terms** - governance can modify rate, pool size, or limits
4. **Close conversion** - long-term scenario (year 10+) if testnet operates independently

-----

## IBC Bridge (tGNK → GNK)

Both chains are Cosmos SDK, making **IBC** the natural choice. Trustless, validator-independent, cryptographic verification - no multi-sig oracles or trusted third parties.

**Bridge flow:**

1. Miner initiates tGNK burn on testnet via IBC transfer to mainnet channel
2. Testnet relayer submits proof to mainnet
3. Mainnet verifies proof against testnet’s light client
4. Mainnet conversion module calculates GNK: `tGNK_amount × (pool_size / 680,000,000)`
5. GNK released from conversion pool to miner’s mainnet address
6. Received tGNK burned

The mainnet requires a conversion module (or `x/inference` extension) to handle this logic.

-----

## Anti-Fraud Measures

Since testnet tokens have real mainnet value, anti-fraud is mandatory at launch:

|Measure                |Description                                             |Purpose                                |
|-----------------------|--------------------------------------------------------|---------------------------------------|
|GNK Deposit on Mainnet |Lock 50-100 GNK (proposed) to be eligible for conversion|Raises Sybil cost; mainnet economic tie|
|Per-Host Cap           |Max % of epoch rewards per node                         |Anti-whale; community distribution     |
|PoC V2 Verification    |Same 1-10% random verification as mainnet               |Catches fake compute                   |
|Nonce Rate Verification|Rate must match claimed hardware                        |Detects hardware spoofing              |
|Conversion Rate Limit  |Max GNK per wallet per period (daily/weekly)            |Prevents pool drain attacks            |

-----

## Open Questions

These require community input and stakeholder alignment:

1. **Model selection** - Qwen2.5-14B (recommended) vs Qwen2.5-7B (safer) vs other? Tradeoff between accessibility and differentiation from consumer setups
1. **Pool size** - 1,000,000 GNK proposed (~0.83% of Community Pool). Right amount?
1. **GNK deposit amount** - 50-100 GNK proposed for bridge access. What threshold filters Sybils without excluding small participants?
1. **Per-host cap** - 1-5% of epoch reward per node. What balances decentralization vs operational overhead?
1. **Conversion rate limit** - Daily or weekly cap per wallet?
1. **Post-emission strategy** - When emission becomes negligible (year 5+), replenish pool or transition to inference-only economics?

-----

## Budget

**Requested: 1,000,000 GNK from the Community Pool** (one-time, for the conversion pool).

This does not fund development - it backs the tGNK → GNK conversion mechanism. Development is handled by the proposing team.

On-chain governance vote (Community Pool spend) will be submitted as a separate transaction once community feedback is incorporated.

-----

## References

1. **Gonka Tokenomics** - emission formula, halving schedule, supply distribution. Source: [docs/tokenomics.md](https://github.com/gonka-ai/gonka/blob/main/docs/tokenomics.md)
2. **Gonka Whitepaper** - Sprint PoW, PoC V2, inference architecture. Source: [gonka.ai/introduction](https://gonka.ai/introduction/)
3. **Gonka Repository** - Chain Node, ML Node, API Node, allowlist. Source: [github.com/gonka-ai/gonka](https://github.com/gonka-ai/gonka)
4. **Network Statistics** - ~11,000 GPUs, 448+ hosts, 2,200+ developers, epoch ~170. Source: network dashboard
5. **Model Specs** - VRAM requirements. Source: Hugging Face model cards, vLLM docs
6. **Cosmos IBC** - bridge protocol. Source: [docs.cosmos.network](https://docs.cosmos.network), [github.com/cosmos/ibc-go](https://github.com/cosmos/ibc-go)

---

## 💬 Комментарии (1)

### Комментарий 1 — [@akamitch](https://github.com/akamitch)

*2026-05-01 15:45 UTC*

This reads more like a second mainnet than a testnet. A testnet needs to run the same hardware and models as mainnet — otherwise it won't catch the real inference-layer bugs (FlashInfer, expert-parallel, FP8 MoE, multi-GPU memory pressure, etc.), which are exactly the class of issues that bite us in production.

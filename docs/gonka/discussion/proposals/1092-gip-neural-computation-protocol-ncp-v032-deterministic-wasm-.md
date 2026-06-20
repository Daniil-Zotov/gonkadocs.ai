---
title: "#1092 — GiP: Neural Computation Protocol (NCP) v0.3.2 – Deterministic WASM Bricks + YAML Graphs for Fast, Auditable Agentic Systems"
source: https://github.com/gonka-ai/gonka/discussions/1092
discussion_number: 1092
category: proposals
synced_at: 2026-06-20T04:41:27Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1092](https://github.com/gonka-ai/gonka/discussions/1092) каждые 6 часов. 

# GiP: Neural Computation Protocol (NCP) v0.3.2 – Deterministic WASM Bricks + YAML Graphs for Fast, Auditable Agentic Systems

**Автор:** [@madeinplutofabio](https://github.com/madeinplutofabio) · **Категория:** :bulb: Proposals · **Создано:** 2026-04-20 14:07 UTC · **Обновлено:** 2026-04-20 14:07 UTC

---

## 📝 Описание

**Title:**  
**GiP: Neural Computation Protocol (NCP) v0.3.2 – Deterministic WASM Bricks + YAML Graphs for Fast, Auditable Agentic Systems**

**Author:** madeinplutofabio  
**Date:** April 20, 2026

### Summary
NCP provides a lightweight, open protocol for composing tiny sandboxed WASM “Bricks” into static YAML graphs. It routes 90–97 % of agentic work (routing, validation, classification, policy checks) to deterministic microsecond paths, escalating to any LLM (or decentralized model) only when truly needed.

### Problem
Current agent frameworks still push even simple deterministic logic through expensive LLM loops. This explodes cost and latency in high-volume pipelines and creates audit / prompt-injection risks in decentralized setups.

### Proposed Solution – NCP
- **Bricks**: Pure-functional WASM modules (no FS, no network, no ambient authority). Deterministic by design.  
- **Graphs**: Static YAML files defining directed graphs with typed edges, routing policies, threshold gating, and field mapping.  
- **Runtime**: Reference implementation in Rust + Wasmtime. Enforces hard limits and produces full replayable traces with hashes + provenance.  
- **Hybrid model**: Bricks can emit confidence scores; the graph decides deterministically whether to take the fast path or escalate.

### Current Status (as of Apr 20, 2026)
- Latest release: **v0.3.2** (Apr 14, 2026)  
- Spec: **v0.2.3** (stable) with full JSON Schemas  
- Benchmarks: 15–34 µs deterministic path; 10–33× latency/cost reduction in 90/10 and 97/3 hybrids (see BENCHMARK.md)  
- Phase 1 & 2 complete, Phase 3 (LangGraph / MCP integrations) in progress  
- License: Apache-2.0  
- Repo: https://github.com/madeinplutofabio/neural-computation-protocol

### Why it fits Gonka / decentralized infra
NCP is local-first, sandboxed, and trust-minimized. It dramatically reduces reliance on expensive/decentralized inference while keeping everything auditable and replayable.

Looking forward to community feedback!



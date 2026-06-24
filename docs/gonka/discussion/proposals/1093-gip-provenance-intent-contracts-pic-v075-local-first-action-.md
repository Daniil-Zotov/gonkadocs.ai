---
title: "#1093 — GiP: Provenance & Intent Contracts (PIC) v0.7.5 – Local-First Action Gating for Verifiable AI Agents"
source: https://github.com/gonka-ai/gonka/discussions/1093
discussion_number: 1093
category: proposals
synced_at: 2026-06-24T09:51:36Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #1093](https://github.com/gonka-ai/gonka/discussions/1093) каждые 6 часов. 

# GiP: Provenance & Intent Contracts (PIC) v0.7.5 – Local-First Action Gating for Verifiable AI Agents

**Автор:** [@madeinplutofabio](https://github.com/madeinplutofabio) · **Категория:** :bulb: Proposals · **Создано:** 2026-04-20 14:10 UTC · **Обновлено:** 2026-04-20 14:10 UTC

---

## 📝 Описание

**Title:**  
**GiP: Provenance & Intent Contracts (PIC) v0.7.5 – Local-First Action Gating for Verifiable AI Agents**

**Author:** madeinplutofabio  
**Date:** April 20, 2026

### Summary
PIC is an open standard that forces AI agents to **prove intent + provenance + evidence** before any high-impact tool call (payments, writes, external APIs, etc.). It operates 100 % locally and fails closed by design.

### Problem
In decentralized agent systems there is currently no reliable way to verify that an agent’s proposed action actually matches the user’s intent or that the inputs are trustworthy. Prompt injection and hidden reasoning make high-stakes actions dangerous.

### Proposed Solution – PIC
- **Intent Contracts**: Structured proposals containing `intent`, `impact`, `provenance`, `claims + evidence`, and `action`.  
- **Provenance tracking**: Inputs carry explicit trust levels; untrusted inputs are blocked unless upgraded by verified evidence.  
- **Cryptographic verification**: Ed25519 signatures + keyring (with expiry/revocation).  
- **Local-first**: Zero cloud dependency. Works offline.  
- **Integrations**: Ready-to-use nodes for LangGraph, MCP tool guarding, and multiple language bindings.

### Current Status (as of Apr 20, 2026)
- Latest release: **v0.7.5** (Apr 3, 2026) – added `strict_trust` mode and attestation draft  
- Spec: **RFC-0001 (PIC/1.0)** with SHA-256 manifest  
- License: Apache-2.0  
- Repo: https://github.com/madeinplutofabio/pic-standard

### Why it fits Gonka / decentralized infra
PIC provides the missing "verifiable intent" layer for any agent stack. It is lightweight, local-first, and designed to work alongside decentralized inference and tool-calling layers.

Looking forward to community feedback!

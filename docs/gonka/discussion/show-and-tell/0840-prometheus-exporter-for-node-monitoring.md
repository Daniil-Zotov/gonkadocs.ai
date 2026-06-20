---
title: "#840 — Prometheus Exporter for Node Monitoring"
source: https://github.com/gonka-ai/gonka/discussions/840
discussion_number: 840
category: show-and-tell
synced_at: 2026-06-20T19:57:27Z
---

> 🔄 **Авто-синхронизация:** из [Discussion #840](https://github.com/gonka-ai/gonka/discussions/840) каждые 6 часов. 

# Prometheus Exporter for Node Monitoring

**Автор:** [@votkon](https://github.com/votkon) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-03-02 22:32 UTC · **Обновлено:** 2026-03-29 15:27 UTC

---

## 📝 Описание

I built a lightweight Prometheus exporter for Gonka node operators: 
https://github.com/votkon/gonka-exporter-prometheus/

It pulls the important metrics — block height, node status, and POC weight — and makes them available to Prometheus, so you can track everything in Grafana rather than polling RPC endpoints by hand.

Just spin up a Docker container with --network host and point it at your local Tendermint RPC and ML Admin API.

If Prometheus is already part of your stack, this should slot right in. 

Full deployment steps are in the README, and I've written up some additional context and usage examples in this forum thread:
https://gonkatalk.org/t/built-a-prometheus-exporter-for-node-monitoring/8

---

## 💬 Комментарии (1)

### Комментарий 1 — [@votkon](https://github.com/votkon)

*2026-03-29 15:27 UTC*

Exporter have been patched to work with the latest proxy settings. Please refer to README for update instructions as an extra docker parameter is needed on restart. 
https://github.com/votkon/gonka-exporter-prometheus/blob/main/README.md

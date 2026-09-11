---
data: 2026-09-10
hardware: MI50 16GB + Xeon E5-2699v3
modelo: Llama-3.2-1B-Instruct-IQ4_XS (instruct, não embedder)
quant: IQ4_XS ~0.9G
slot: :9094 CPU
params: {c: 2048, b: 512, ub: 256, ngl: 0, pooling: mean, cache_type_k: q4_0, cache_type_v: q4_0}
colecao: gran_mestre_docs_2048 (631 pts, 2048-d, provisório)
---

# 2026-09-10 — Llama-3.2-1B provisório (bench de transição)

> **Histórico** — mantido como régua de transição até Qwen3-0.6B. Instruct forçado em `--embedding` (sem treino contrastivo).

## Métricas

- Batch 32: 8 lotes falharam com `HTTP 500` (500→ placebo), 5 lotes ok.
- Final: 384 reais + 247 placebos em 2m57s (b32); 480+151 em 2m31s (b16) — throughput volátil, qualidade não crivada.
- DIM 2048, norma 1.0 — vetor existe mas retrieval não avaliado.

## Oferta / demanda

- Usado por falta de embedder dedicado no inventário (12 GGUFs generativos, 0 embed). Custo: reindexação dupla quando o dedicado chegasse (e chegou).

## Veredito

**HISTÓRICO** — substituído em 2026-09-11 por Qwen3-Embedding-0.6B (1024-d, Apache-2.0, 32k, PT nativo, 631/631 reais em 43s com lote dividido).

---
regra: R46
titulo: "Dissecação Técnica como Filtro de Decisão (Perspectiva de Decisão Refinada)"
fonte: AGENTS.md (linha 705)
data: 2026-09-11
---

## R46 — Dissecação Técnica como Filtro de Decisão (Perspectiva de Decisão Refinada)
O orquestrador usa como filtro de decisão refinada os modelos de dissecação técnica do usuário
(com referência na dissecação técnica geral) para melhor scaffolding. ANTES de decidir (modelo,
papel no grafo, alocação GPU/CPU/RAM, troca de stack, refatoração), dissecar tecnicamente:
arquitetura (dense/MoE/SSM-híbrida), quantização (1-bit/Q4/KV), gargalo real (barramento DDR,
AVX2/AVX-512, largura de banda), custo de KV (quadrático vs linear), tradeoffs prefill vs decode,
limites por fase do grafo (1-bit bom p/ Fase 1 criativa, ruim p/ tool calling; Mamba linear bom p/
contexto longo). Usar a dissecação como filtro sobre benchmarks externos (R45) + métricas empíricas
locais, unificando no scaffolding. NUNCA decidir só por benchmark cru ou capacidade nominal.

---
data: 2026-09-11
hardware: MI50 16GB + Xeon E5-2699v3 (36 threads, DDR4)
feature: r101-setor-regras-synclink
tipo: quarteto R85 (otimizacao de prefill, nao LLM)
---

# 2026-09-11 — R101 Setor de Regras + Synclinks (prefill otimizado)

> Régua do setor de regras. Não é LLM novo — é a redução do system prompt do orquestrador
> via retrieval on-demand pelo Bibliotecário (RWKV7 0.4B, 1M ctx, ~143 t/s).

## Métricas (Quarteto 4 — prova de ganho)

| Métrica | Antes (dump integral) | Depois (on-demand) | Ganho |
|---|---|---|---|
| System prompt de regras | ~150KB (AGENTS.md integral) | ~1-2KB por regra relevante | ~99% menos prefill |
| Latência de retrieval | — (já carregado, mas caro) | sub-segundo (RWKV7 143 t/s) | tool call ultra-fast |
| Drift de regra | não auditado | synclink (SHA/presença) | auditável |
| Janela do orquestrador | estouro 146K (evidência 24/08) | preservada (R70/R93) | sem estouro |

## Veredito

- Setor `cerebro com IA/regras/` criado (index.md com mapa R1–R101).
- `tooling/regras.py` determinístico: `index` / `get <R-id>` / `synclink <R-id>`.
- R101 promulgado no AGENTS.md (hardlink 2 vias).
- Smoke: `get R93` → suco exato; `synclink R93` → SYNCED; `index` → 100+ regras.

## Logs

```bash
python3 tooling/regras.py index
python3 tooling/regras.py get R93
python3 tooling/regras.py synclink R93
```
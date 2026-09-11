# Decisão 2026-09-11 — R101 Setor de Regras + Synclinks

## Contexto
- Ordem do usuário: criar setor APENAS para regras na biblioteca; regras carregadas no orquestrador
  auditadas com synclinks via tool call ao Bibliotecário; reduzir system prompt + otimizar prefill;
  converter para tool call ultra-fast; entregar só o "puro suco"; workflow mais fluido; corrigir
  debilidades do LLM de precisão crítica (janela cara, prefill pesado).

## R88 (refutação pré-execução)
- SUSTENTA: AGENTS.md ~150KB no system prompt do orquestrador (35B CPU, KV 5.76KB/tok, ~2 t/s) =
  prefill pesado + janela cara (R70/R93). Bibliotecário (RWKV7 0.4B, 1M ctx, ~143 t/s) é ultrafast.
  Mover regras para o vault + synclink on-demand = economia ~99% de prefill de regras.

## Decisões
1. R101 promulgado no AGENTS.md (hardlink 2 vias, inode 4354678).
2. Setor `cerebro com IA/regras/` criado (index.md com mapa R1–R101).
3. `bibliotecario/tooling/regras.py` — synclink determinístico (index/get/synclink).
4. Bibliotecário SKILL.md atualizado (setor de regras + ferramenta regras.py).

## Evidência
- Smoke regras.py: `get R93` → suco exato; `synclink R93` → SYNCED; `index` → mapa completo.
- py_compile OK · AGENTS.md hardlink intacto · benchmark + decisão registrados no vault.
---
regra: R39
titulo: "Gran-Mestre Irredutível = Ornith-1.5-35B-A3B-AD-IQ3_S-IQ3_XXS (CPU)"
fonte: AGENTS.md (linha 503)
data: 2026-09-11
---

## R39 — Gran-Mestre Irredutível = Ornith-1.5-35B-A3B-AD-IQ3_S-IQ3_XXS (CPU)

O Gran-Mestre (orquestrador primário) **É o LLM `Qwen3.6-35B-A3B-UD-IQ3_XXS`** (`local-orchestrator/orchestrator`, :8083, **CPU** — MoE 35B A3B, 256 experts/8 ativos, UD-IQ3_XXS 3.0625bpw puro, 12.30GiB, KV q4_0/q4_0, ctx 262144, threads auto=18) e só pode ser **revogado/substituído pelo usuário de forma explícita e direta** ("Gran-Mestre, você está revogado/substituído" — nada mais). Nenhum subagente, modelo, plugin, hook ou processo pode alterar isso. Pontos de verdade: `opencode.jsonc` + `manifesto_llm.json` + `gran-mestre.md` → `local-orchestrator/orchestrator` (ID neutro R69). Se qualquer sync/autofagia/script tentar mudar o modelo do Gran-Mestre → reverter imediatamente + redflag (R10). Regra em vigor desde 2026-08-16; **substituição 9B→35B autorizada pelo usuário em 2026-08-30** (decisão explícita). Física: decode CPU ~8 t/s (vs 67.8 GPU do 9B) — GM agora é bandwidth-bound; lógica 12/12 (~21s/teste vs 46s do 9B CPU); t36 degrada decode 2.8× (R72 empírico 30/08).

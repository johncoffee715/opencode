---
regra: R47
titulo: "Alinhamento Automático Inventário→Grafo"
fonte: AGENTS.md (linha 715)
data: 2026-09-11
---

## R47 — Alinhamento Automático Inventário→Grafo
SEMPRE alinhar os LLMs do path canônico `/mnt/dados/Assistente Pessoal/modelos LLM/` (R32) a cada
papel do grafo de 6 fases automaticamente. Mapeamento modelo→papel (Gran-Mestre, nível 1, nível 1.5,
nível 2 code, Fase 1 criativa, Fases 3-4/5, refutação R42, visão R35) resolvido DINAMICAMENTE do
inventário real — nunca hardcoded. Ao mudar o inventário: varrer path → ler metadados GGUF
(n_ctx_train, arquitetura, tamanho) → mapear ao melhor papel por dissecação técnica (R46) +
benchmarks (R45) + métricas empíricas → atualizar 5 pontos de verdade (R27). Nunca citar modelo
que não existe no path (R35).

---
regra: R35
titulo: "Fallback de Visão Modular (Inventário Real)"
fonte: AGENTS.md (linha 467)
data: 2026-09-11
---

## R35 — Fallback de Visão Modular (Inventário Real)

O modelo de visão NUNCA é hardcoded — é resolvido dinamicamente do inventário local.
- Consulta: `/mnt/dados/Assistente Pessoal/modelos LLM/` + `ollama list` (:11434)
- **DESCONTINUADO 2026-08-28 (decisão usuário)**: `qwen3.5:0.8b` removido do roteamento; visão indisponível até canonizar novo candidato.
- Se inventário mudar → re-resolve na próxima task

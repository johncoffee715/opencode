---
regra: R35
titulo: "Fallback de Visão Modular (Inventário Real) — DESCONTINUADO 2026-08-28"
fonte: AGENTS.md (linha 451)
data: 2026-09-11
---

## R35 — Fallback de Visão Modular (Inventário Real) — DESCONTINUADO 2026-08-28

<Nunca hardcoded>
- O modelo de visão NUNCA é fixo/hardcoded como fallback — é resolvido dinamicamente a cada task.
- Consulta o inventário REAL de LLMs locais em `/mnt/dados/Assistente Pessoal/modelos LLM/` (R32) + `ollama list` (:11434).

<Fluxo de resolução>
1. Varrer inventário por candidatos com `vision`/mmproj.
2. Selecionar o melhor disponível.
3. Inventário mudou (novo modelo/remoção) → re-resolve na próxima task.
- NUNCA citar um modelo que não existe no inventário.

<Exemplos registrados>
- R30/R31 NÃO citam mais "LFM2.5-VL-1.6B" como fallback — o inventário real só tem LFM2.5-230M-Q4_0 (sem mmproj confirmado). Regra em vigor desde 2026-08-13.
- **2026-08-28 (decisão usuário)**: backend de visão `qwen3.5:0.8b` via Ollama :11434 foi DESCONTINUADO e removido do roteamento (llm-inventory FEATURES, feature_types, affinities, attach_media.py desativado). Sem candidato de visão canonizado no inventário → visão indisponível (honesto, partial). Reativar só com modelo de visão oficialmente canonizado no path canônico + ATTACH_VISION_MODEL setado.

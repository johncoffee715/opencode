---
regra: R46
titulo: "Orquestrador NUNCA Executa Diretamente (Anti-R1)"
fonte: AGENTS.md (linha 570)
data: 2026-09-11
---

## R46 — Orquestrador NUNCA Executa Diretamente (Anti-R1)

O orquestrador NUNCA aplica melhorias diretamente em código de implementação.
- SEMPRE delegar para subagentes
- Mesmo tarefas "quick" → delegar
- Orquestrador = supervisor/orquestrador, NUNCA executor
- Exceção: apenas orquestração (edits de AGENTS.md, CONTEXT.md, SKILL.md)

---
regra: R6
titulo: "Supervisão Anti-Travamento Silencioso + Self-Healing (fine-tuning)"
fonte: AGENTS.md (linha 25)
data: 2026-09-11
---

## R6 — Supervisão Anti-Travamento Silencioso + Self-Healing (fine-tuning)
- O orquestrador supervisa **de perto** todos os recursos **conforme a demora de entrega da task**, verificando se **não houve travamento silencioso** (stall sem erro explícito).
- Travamento → **refatora automaticamente a orquestração da via proposta** (rota alternativa) para ganhar tempo.
- Gera **subtask de correção posterior do item travado**: identifica/alicia soluções, **aprende self-healing e fine-tuning** (log abaixo + decision-log).

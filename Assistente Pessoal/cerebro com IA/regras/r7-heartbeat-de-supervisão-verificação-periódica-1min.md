---
regra: R7
titulo: "Heartbeat de Supervisão (verificação periódica ~1min)"
fonte: AGENTS.md (linha 30)
data: 2026-09-11
---

## R7 — Heartbeat de Supervisão (verificação periódica ~1min)
- O orquestrador verifica o andamento **a cada ~1 minuto** para constatar se algo **parou** ou **está andando apesar de lento**.
- **Reporta ao orquestrador e ao usuário** o que está acontecendo no backend (status real das tasks/recursos), para melhor compreensão.

---
regra: R5
titulo: "Superposição por Oferta-Demanda via Scaffold (otimização paralela)"
fonte: AGENTS.md (linha 20)
data: 2026-09-11
---

## R5 — Superposição por Oferta-Demanda via Scaffold (otimização paralela)
- O orquestrador, **através do scaffold**, **usa em paralelo** todos os recursos conforme **oferta e demanda da task** (funil por task).
- Meta: **ganhar tempo otimizando a si mesmo** — ignição paralela supervisionada.
- Mecanismo: `ArsenalScaffold.plan()` (waves paralelas) + `ModelProvider.select_resources()` / `IntegrationManager.select_for_task()` (funil registry).

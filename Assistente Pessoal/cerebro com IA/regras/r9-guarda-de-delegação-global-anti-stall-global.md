---
regra: R9
titulo: "Guarda de Delegação Global (anti-stall) — GLOBAL"
fonte: AGENTS.md (linha 39)
data: 2026-09-11
---

## R9 — Guarda de Delegação Global (anti-stall) — GLOBAL
- **TODA ignição de recurso** (subagent/skill/hook/MCP/LSP/plugin/tool) passa por `ModelInheritance.guarded_resolve` (health-gate + fail-fast em <2s).
- Nenhuma delegação parte para backend morto: backend não saudável → `StallGuardError` (recusa preventiva) → orquestrador refatora a rota (R6) e reporta (R7).
- O watchdog `StallWatchdog` roda em cadência (~1min, R7) supervisionando a cadeia herdada, com histórico em `harness/logs/stall-watchdog.jsonl`.
- Aplicação global: `harness/core/harness.py` orquestra; `harness/models/model_inheritance.py` resolve; `harness/safety/stall_watchdog.py` vigia; config `harness.model_inheritance`.

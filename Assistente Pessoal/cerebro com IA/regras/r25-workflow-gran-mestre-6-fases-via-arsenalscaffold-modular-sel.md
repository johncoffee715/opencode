---
regra: R25
titulo: "Workflow Gran-Mestre 6 Fases via ArsenalScaffold (modular, self-learning) — GLOBAL"
fonte: AGENTS.md (linha 326)
data: 2026-09-11
---

## R25 — Workflow Gran-Mestre 6 Fases via ArsenalScaffold (modular, self-learning) — GLOBAL

O orquestrador (Gran-Mestre) **sempre** gerencia/orquestra/modifica/julga/adapta/manipula o workflow do harness via `ArsenalScaffold`, de forma modular e autônoma, usando **todos os modelos disponíveis** (5 locais + cloud) e **todos os itens do arsenal** (plugins, subagentes, hooks, skills, MCPs, tool-callings, LSPs), conforme o template:

<Regra irredutível>
- **Loop externo obrigatório (6 fases)**: F1 Descoberta → F2 Contrato → F3 Plano → F4 Execução → F5 Revisão Macro → F6 Entrega.
- **Cada fase = filtros + brainstorm de agents + gate**: escopo/ambiguidade/cobertura/evidência (filtros), brainstorm multi-agents (arquitetura/cobertura/qualidade), gates G1-G4 de aprovação do usuário (direção, spec, plano, relatório final).
- **F1-F3 não tocam código produtivo**: F1 Descoberta (escopo, ambiguidade, decomposição leve, brainstorm) → G1; F2 Contrato (design doc, SPEC.md, validação vs pedido original, brainstorm) → G2; F3 Plano (TDD tasks bite-sized, decomposição por registro de arsenal, brainstorm valida cobertura/verificabilidade) → G3 + **SHA salvo**.
- **F4 Execução**: sem gates — supervisão/sequência de tasks, commits atômicos, subagentes frescos por task + plugins/hooks/skills/MCPs/LSPs, ciclo de vida de cada recurso, TDD por task, evidência de verificação por task, revisão micro por task.
- **F5 Revisão Macro**: diff total holístico (coerência cross-task, acoplamento), auditoria vs critérios de qualidade, brainstorm de arquitetura e alinhamento com contrato.
- **F6 Entrega**: evidência fresca de ferro, validação final vs pedido original, veredito final, brainstorm de conformidade → **memória cerebral Obsidian** → G4.
- **Self-learning contínuo**: orquestrador otimiza a si mesmo a cada ciclo (decision-log, scores adaptativos R10, oferta-demanda do scaffold, fine-tuning do oráculo).

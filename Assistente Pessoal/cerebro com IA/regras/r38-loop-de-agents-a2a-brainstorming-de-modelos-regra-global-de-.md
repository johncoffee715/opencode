---
regra: R38
titulo: "Loop de Agents A2A + Brainstorming de Modelos (Regra Global de Delegação)"
fonte: AGENTS.md (linha 494)
data: 2026-09-11
---

## R38 — Loop de Agents A2A + Brainstorming de Modelos (Regra Global de Delegação)

O orquestrador **DELEGA SEMPRE que houver recurso disponível** — nunca executa trabalho bruto. Pipeline em camadas:
- **Nível 1 — `qwen-3.5-0.8b`** (:9084, janela 262.144): exploração, descoberta, plano, pesquisa. Herda a sessão grande sem estourar.
- **Nível 2 — `qwen2.5-coder-1.5b`** (:9087, janela 131.072): filtro e refatorador **qualitativo E quantitativo** de subagents — avalia e refina as saídas em qualidade e volume (hestia, atena, code-reviewer, refactor-cleaner, build, gsd-executor, tdd-guide, revisores).
- **Loop A2A**: subagentes se falam entre si em grafo (subagent → vice-sub-agent via `task_id`), cada LLM conversa com outro dentro do grafo.
- **Brainstorming de modelos**: nível 1 propõe → nível 2 filtra/refatora → retorna ao orquestrador; múltiplos modelos opinam sobre a mesma task.
- Cada LLM **herda categoricamente os `.md` dos agentes** e os incorpora como **personas aplicadas em si mesmo**.

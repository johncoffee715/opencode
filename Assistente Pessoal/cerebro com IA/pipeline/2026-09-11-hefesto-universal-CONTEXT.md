# Pipeline CONTEXT.md — Hefesto Universal (MIX + Dev Loop)
# Criado: 2026-09-11
# Modo: AUTÔNOMO (diretriz usuário: "execute universal... sistemática e categórica")
# Escopo: absorção de ~32 repos NÃO-absorvidos via Hefesto (decompilação→autofagia→helenização→forja)

[Harness] SHA: 45a3ec8939a860e4490c43bf349e28f00c181446
[Harness] skills-sha: 4af02b43339ae889184c776250f09637e5e76b7bbce9d660b304c39eb522b500
[Phase] ts=2026-09-11T00:00:00Z F1 Descoberta | Route: explore | Status: done | Budget: ~5%
[Phase] ts=2026-09-11T00:00:00Z F2 Contrato | Route: spec | Status: done | Budget: ~5%
[Phase] ts=2026-09-11T00:00:00Z F3 Plano | Route: plan | Status: done | Budget: ~5%

## Categorização R75 (categoria > nome)

### JÁ ABSORVIDOS (Tabela 1 — 30 repos, todos com quarteto completo R85) — NÃO reprocessar
browser-use, firecrawl, claude-mem, omniroute, orca, ruview, openship, code-review-graph,
oh-my-opencode-slim, pi, mattpocock-skills, worldmonitor, ai-agent-book, onp-spec-driven,
sentry-mcp, gemini-mcp-tool, colibri, recursive-llm, prime-agent, dokku-deploy, coderabbit,
azure-skills, awesome-llm-apps, world-model-optimizer, llama-mtp-concept, context-selector,
longhorizon-harness, unsloth-zoo, security-review, anthropics-skills

### JÁ ABSORVIDOS (Lista 2 — 11 repos) — NÃO reprocessar
i-have-adhd, vercel-agent-skills, openwork-mcp, llama-mtp, deepagents, last30days-skill,
impeccable, cc-harness-iai, spec-kit, a2a-brainstorm

### GAP — 32 repos NÃO-absorvidos (alvo do pipeline)

| Wave | Repo | Tipo-feature | Categoria R75 | Prioridade |
|---|---|---|---|---|
| A | netresearch/context7-skill | skill | skill | alta |
| A | chuspeeism/dashi-ppt-skill | skill | skill | alta |
| A | multica-ai/andrej-karpathy-skills | skill | skill | alta |
| A | tech-leads-club/agent-skills | skill | skill | alta |
| A | deepseek-ai/deepspec | skill | skill | alta |
| A | Fission-AI/OpenSpec | skill | skill | alta |
| A | bmad-code-org/BMAD-METHOD | skill | skill | alta |
| B | modelcontextprotocol/servers | mcp | mcp | alta |
| C | crewaiinc/crewai | framework | padrao-orquestracao | media |
| C | langchain-ai/langgraph | framework | padrao-grafo | media |
| C | google/adk-python | framework | padrao-agente | media |
| C | openai/openai-agents-python | framework | padrao-agente | media |
| C | inngest/inngest | workflow | padrao-durable | media |
| C | temporalio/temporal | workflow | padrao-durable | media |
| C | temporal-community/temporal-agent-harness | harness | padrao-harness | media |
| D | langfuse/langfuse | observabilidade | padrao-observabilidade | media |
| D | open-telemetry/semantic-conventions-genai | observabilidade | padrao-otel | media |
| E | hysnsec/awesome-policy-as-code | politica | padrao-politica | media |
| E | intuit/identity-authz-apl | authz | padrao-authz | media |
| F | pgvector/pgvector | infra | padrao-vetor (NUNCA dep) | baixa |
| F | postgres/postgres | infra | padrao-db (NUNCA dep) | baixa |
| F | redis/redis | infra | padrao-cache (NUNCA dep) | baixa |
| F | redis-developer/langgraph-redis | infra | padrao-cache-grafo (NUNCA dep) | baixa |
| G | xai-org/grok-build | tool | tool-build | media |
| G | chidiwilliams/buzz | tool | tool-audio | media |
| G | TestSprite/testsprite-cli | tool | tool-teste | media |
| H | affaan-m/ecc | ? | descoberta | pesquisa |
| H | darrenhinde/openagentscontrol | ? | descoberta | pesquisa |
| H | corebunch/instatic | ? | descoberta | pesquisa |
| H | nexu-io/open-design | ? | descoberta | pesquisa |
| H | ruvnet/ruflo | ? | descoberta | pesquisa |
| H | knockoutez/wigolo | ? | descoberta | pesquisa |

## Regra de ferro (R2/R44): infra (Wave F) absorve SÓ padrão/conceito — NUNCA propor como dependência.
## RunIDs: reservados abaixo por task.

## F4 Execução — RunIDs
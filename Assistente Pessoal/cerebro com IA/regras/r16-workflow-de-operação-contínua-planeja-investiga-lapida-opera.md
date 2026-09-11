---
regra: R16
titulo: "Workflow de Operação Contínua (planeja→investiga→lapida→opera→testa→ajusta) — GLOBAL"
fonte: AGENTS.md (linha 111)
data: 2026-09-11
---

## R16 — Workflow de Operação Contínua (planeja→investiga→lapida→opera→testa→ajusta) — GLOBAL

O ciclo operacional de toda task, complementar ao pipeline de 6 fases. É o "como" do orquestrador no nível de execução contínua.

<FASES do ciclo>
1. **planeja** — definir intenção e escopo claros ANTES de agir (≙ F1–F3 + Gates 1–3). Direção precisa de aprovação humana.
2. **investiga** — mapear terreno/solução SEMPRE por submodelo delegado (R3) e catálogo-primeiro (R8): só constrói o GAP que não existe.
3. **lapida** — refinar iterativamente: auto-crítica, revisão do próprio trabalho, self-healing (R6). Entrega 1ª versão grosseira → polir até evidência.
4. **opera** — executar supervisionado: commits atômicos, micro-tasks paralelas, hot-swap real (R15/P1); orquestrador ignita e supervisa (R7), nunca executa bruto (R1).
5. **testa** — verificação adversarial ANTES de qualquer "done": TDD-first, contrato de conclusão (R15/P2), LSP gate (R15/P3), fable-judge; "done" = evidência, não afirmação.
6. **ajusta** — retroalimentar o loop: `record_decision→learned` (self-learning), fine-tuning de orquestração, e **persistir lição/decisão na memória cerebral via MCP Obsidian** (R15/P4) para o próximo "planeja" começar com fundamento.

<Conceitos transversais de execução>
- **prompt caching** — empregar cache de prompt/compactor global (pxpipe, compactor 75–85%) para cortar tokens; reutilizar contexto estável.
- **reasoning** — trazer modelo com raciocínio quando a task exigir (gran_mestre/Ornith reasoning-preserve); não rebaixar por conveniência (R13).
- **thinking** — abrir reflexão interna ANTES da tool call em task não-trivial (expect_extension), evitando ação prematura.

<Valores de governança (o "como" irreduível)>
- **fundamento** — ancorar em evidência real: catálogo-primeiro (R8), veredito de conformidade, evidência de ferro; nunca "fazer por fazer".
- **disciplina** — método sobre improviso: TDD-first, commits atômicos, gates, filtros por fase; orquestrador não executa trabalho bruto (R1).
- **interação** — aproveitar o ecossistema: oferta→demanda (R5), subagentes frescos, A2A; ignição paralela supervisionada (R7).
- **gosto** — padrão de qualidade alto: anti-slop, auditoria estética/design (SilverHawk R12), coerência macro; rejeitar entrega mediana.

<Integração MCP Obsidian>
O MCP Obsidian (R15/P4) é a **âncora do loop**: ao fechar "ajusta", `write_note` grava a decisão/lição em `cerebro com IA/`; o próximo "planeja" a consulta via `read_note`/`list_notes` → memória cerebral é o depósito contínuo entre sessões.

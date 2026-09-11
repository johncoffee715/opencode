---
regra: R22
titulo: "Context Window Task Fragmentation & Sequential Merge (Task Manager) — GLOBAL"
fonte: AGENTS.md (linha 242)
data: 2026-09-11
---

## R22 — Context Window Task Fragmentation & Sequential Merge (Task Manager) — GLOBAL

Camada **fundamental do Task Manager**, executada **antes da seleção do subagente**. Nenhuma tarefa deve falhar exclusivamente por exceder a janela de contexto de um subagente: a tarefa primária é **decomposta → enfileirada → executada → validada → consolidada → retomada**. O tamanho da janela do subagente é **restrição de execução, não limitação da tarefa** (`TASK SIZE ≠ CONTEXT WINDOW`).

<Regra irredutível (invariante)>
> Uma tarefa nunca deve ser descartada por excesso de contexto. Ela deve ser decomposta até que cada unidade seja executável dentro da capacidade do agente, mantendo dependências, estado, validação e ordem de execução; ao final, os resultados devem ser semanticamente consolidados antes da continuação do workflow.

<Fluxo obrigatório>
1. **Estimativa de capacidade**: `available_context = window − system_prompt − agent_prompt − tool_definitions − memory − reserved_output_tokens − safety_margin`. Se `task_tokens <= available_context` → EXECUTAR direto. Senão → `TASK_FRAGMENTATION`.
2. **Decomposição semântica (Fatiador)**: cortar **só em fronteiras estruturais** (fim de blocos lógicos — AST para código, parágrafos fechados para texto), **nunca por contagem matemática de tokens**. Fragmentos autossuficientes com `task_id/parent_task/sequence/objective/inputs/constraints/expected_output/validation/state_from_previous_tasks`.
3. **Envelope de task**: cada fragmento carrega envelope mínimo (YAML/JSON) com dependências explícitas, critérios de validação e `output_artifact`.
4. **Fila cronológica com dependências**: scheduler só executa task cujas dependências estejam `COMPLETED + VALIDATED`. Estados: PENDING→QUEUED→RUNNING→BLOCKED→COMPLETED→VALIDATED→FAILED→RETRYING→MERGED.
5. **Motor de Estado (propagação)**: **nunca passar output bruto** de um subagente ao próximo (estoura a janela em cascata). Passar **Rolling Summary + Vetor de Estado (JSON)** — "metas concluídas, entidades globais ativas, contexto pendente" — e **ponteiros lógicos** ao dado bruto. Contexto progressivo: objective + resultados relevantes + decisões + constraints + estado atual (não histórico bruto).
6. **Checkpoint obrigatório** após cada fragmento: `task_id/status/result/decisions/files_changed/tests/errors/unresolved/next_action` — permite interromper/continuar sem perder estado.
7. **Falha de subtask**: RETRY se possível; **REFRAGMENT se contexto insuficiente** (nunca abortar a primária); BLOCK se dependência inválida.
8. **Consolidação (Reducer)**: merge **semântico**, não concatenação — remover duplicações do overlapping, resolver conflitos, preservar decisões, verificar dependências, reconstruir coesão, validar consistência. Conflito detectado → **registrar** (sources/description/resolution/reason), nunca escolher silenciosamente.
9. **Validação final do merge** → se falhar, resolver conflitos → **RETOMAR WORKFLOW** com o resultado consolidado.

<Arquitetura (abaixo do workflow, nível do orquestrador)>
```
ORCHESTRATOR
   ├── WORKFLOW
   └── TASK MANAGER
        ├── CONTEXT MANAGER
        ├── TASK DECOMPOSER
        ├── TASK QUEUE
        ├── CHECKPOINT STORE
        └── RESULT MERGER
```
Qualquer workflow usa a mesma infraestrutura de fragmentação (reuso, R8/R2).

<Overlapping (margem de sangria)>
Task N+1 herda ~15% final do contexto da Task N (sliding window) para garantir escopo imediato das funções/raciocínios em andamento — e o Reducer remove as redundâncias geradas por essa sobreposição na emenda.

<Relação>
- **R20** — janela-curta → nuvem: a fragmentação R22 roda ANTES (decompõe para caber no subagente); se mesmo fragmentada não couber, aí a rota nuvem (R20) se aplica.
- **R21** — VRAM só uso ativo: fragmentos enfileirados não alocam VRAM ociosa; estado vive em disco (`state/tasks/TASK-N/`), não em VRAM.
- **R13/R17** — roteamento por competência: fragmentos podem ser executados por subagentes distintos conforme capacidade; orquestrador supervisa, executor executa.
- Regra promulgada pelo usuário: "regra global camada fundamental do Task Manager, antes da seleção do subagente. se as tasks não couberem dentro da janela de contexto dos subagentes, fragmentar a task primária até caber dentro da janela de contexto dos subagents e enfileirar as tasks cronologicamente até terminar e fundir tudo novamente e seguir workflow".

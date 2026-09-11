---
regra: R47
titulo: "Guardrails de Execução de Regras Globais"
fonte: AGENTS.md (linha 578)
data: 2026-09-11
---

## R47 — Guardrails de Execução de Regras Globais

TODAS as regras globais devem ser validadas automaticamente:

### Checklist de Validação (antes de CADA task)
1. R1: Orquestrador não executa diretamente? → SEMPRE delegar
2. R28: Critério de trânsito categórico? → veredito PASSOU/NAO_PASSOU
3. R29: Teste como usuário final? → evidência fresca
4. R34: Nota 0,0000001–100? → mínimo 97
5. R37: Autonomia total do orquestrador? → pesquisa aplicada
6. R45: Decomposição bite-sized? → ≤3 arquivos por task
7. R46: Orquestrador não executa? → SEMPRE delegar

### Validação Pós-Task
1. Syntax check: node --check
2. Testes: node --test → 36/36
3. QA: qa.mjs → 22/22 PASS
4. Screenshot: evidência visual
5. Scorecard: nota R34 com bugs concretos

### Auto-Correção
Se qualquer regra falhar:
1. Identificar regra violada
2. Corrigir imediatamente
3. Registrar no decision-log
4. Reportar ao usuário

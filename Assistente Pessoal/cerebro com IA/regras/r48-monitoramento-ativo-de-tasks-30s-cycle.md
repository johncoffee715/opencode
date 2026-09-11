---
regra: R48
titulo: "Monitoramento Ativo de Tasks (30s Cycle)"
fonte: AGENTS.md (linha 605)
data: 2026-09-11
---

## R48 — Monitoramento Ativo de Tasks (30s Cycle)

TODAS as tasks delegadas devem ser monitoradas a cada 30 segundos:
- Verificar se estão "running" ou "stalled"
- Acompanhar progresso com métricas de baixo nível
- Se stalled >2min → intervenir (refatorar rota ou cancelar)
- Registrar status no CONTEXT.md

### Métricas de Baixo Nível
1. Duração total da task
2. Última tool call (timestamp)
3. Número de iterações
4. Tamanho do output gerado
5. Erros/warnings

### Ação se Stalled
1. Verificar se modelo está respondendo
2. Se timeout → cancelar e relançar com modelo diferente
3. Se erro → diagnosticar e corrigir
4. Registrar no decision-log

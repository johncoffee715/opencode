---
regra: R18
titulo: "Circuit-Breaker Global (N tentativas OU tempo-box sem progresso) — GLOBAL"
fonte: AGENTS.md (linha 162)
data: 2026-09-11
---

## R18 — Circuit-Breaker Global (N tentativas OU tempo-box sem progresso) — GLOBAL

Resposta ao gap de supervisão: o que acontece quando um loop de TDD NÃO converge após N tentativas de subagente fresco OU fica parado por N segundos sem progresso. Fecha o buraco entre R6 (trava silenciosa por backend morto) e R7 (heartbeat periódico) — aqui o ator é o **subagente vivo mas improdutivo** (repete, gira em círculo, ou silencia sem tool output).

<Princípio>
Um loop de trabalho que não converge em **3 tentativas** de subagente fresco ou **300s sem progresso** dispara a sequência do circuit-breaker: ESCALAR → ABORTAR → ROLLBACK (máx 1/pipeline) → BLOQUEAR com gate humano. Nenhum pipeline passa por um circuito aberto sem intervenção humana ou cooldown decorrido.

<Mecanismo (module `harness/safety/circuit_breaker.py`)>
- Estados: `CLOSED` (ok) → `OPEN` (tripado) → `HALF_OPEN` (cooldown) → `CLOSED` (sucesso) | auto-reset após cooldown.
- Contadores: falhas consecutivas por task; heartbeats de progresso por subagente.
- Ações por nível de falha (1ª/2ª = escalar via Dev Loop N1→N2→N3 + subagente fresco; 3ª = abortar task; se rollback disponível e pipeline já tem evidência parcial → `git reset --hard` máx 1x; rollback já usado → `BLOCK` com gate humano).
- Health-Gate herança de R9: nunca pular para backend morto/corrompido na abertura do circuito.

<Contrato>
- o orquestrador NUNCA "tenta de novo" manualmente um loop tripado (R17 — polo pensante não empurra a pedra);
- o `CircuitBreaker` registra 1 linha em `harness/logs/circuit-breaker.jsonl` por transição de estado;
- a integração no harness.py verifica o disjuntor em `_run_wave` (antes de delegar cada sub-tarefa) e nos gates; se OPEN → não delega, devolve ação de supervisão;
- default: `max_failures=3`, `progress_timeout_seconds=300`, `cooldown_seconds=60`, `rollback_max=1` (overrides via `harness.circuit_breaker` no harness-config.json).

<Escopo>
- Aplica a qualquer loop da Fase 1–4 que use subagentes; gate humano obrigatório quando `rollback_max` é atingido (R2 preservation — não estourar recurso único).

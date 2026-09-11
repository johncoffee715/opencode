---
regra: R28
titulo: "Critério de Trânsito Categórico por Métrica (avaliador impressionado) — GLOBAL"
fonte: AGENTS.md (linha 396)
data: 2026-09-11
---

## R28 — Critério de Trânsito Categórico por Métrica (avaliador impressionado) — GLOBAL

Promulgada 2026-08-12 (pedido do usuário). Toda métrica exigida de um subagent
(executor, pesquisador, revisor, juiz, supervisor, gerente) tem critério de
trânsito EXPLÍCITO para a próxima instância: o avaliador/juiz/supervisor/
gerente/revisor da fase seguinte DEVE registrar veredito CATEGÓRICO por métrica
exigida — e o resultado precisa IMPRESSIONAR, não apenas "passar".

<Regra irredutível>
- **Critério de trânsito por métrica**: cada métrica exigida (ex.: cobertura ≥
  80%, zero CRITICAL/HIGH, TDD verde, janela respeitada, evidência fresca) deve
  ter, no plano/contrato (F2/F3), um critério de trânsito escrito que defina o
  que é "entregue" vs "insuficiente" — nunca métrica solta sem critério.
- **Veredito categórico**: o avaliador/juiz/supervisor/gerente/revisor emite,
  por métrica exigida, um veredito binário explícito — `PASSOU_CATEGORICO` ou
  `NAO_PASSOU` — com evidência, antes de liberar a próxima instância do
  subagent. Proibido "passa mas...", "quase lá", veredito condicional.
- **Impressão > aprovação mínima**: resultado que só "cumpre o mínimo" sem
  impressionar (robustez, clareza, elegância, profundidade da evidência) NÃO
  transita — o avaliador deve conseguir declarar, de forma categórica, que o
  resultado impressiona em CADA métrica exigida, ou devolver ao executor com
  apontamento específico.
- **Gate humano quando o avaliador não consegue ser categórico**: se o
  avaliador não consegue emitir veredito categórico (ambiguidade, evidência
  insuficiente, tradeoff aberto) → NÃO avança; escale ao Gran-Mestre com
  gate humano (R18), nunca avance com veredito diluído.
- **Fica registrado**: o veredito categórico por métrica é gravado no
  CONTEXT.md (linha `[Gate] <métrica> → <PASSOU_CATEGORICO|NAO_PASSOU>` +
  evidência de 1 linha) e no decision-log — decisão rastreável, não opinião
  volátil.
- **Vale para toda a cadeia**: executor→revisor (micro), →Atena (macro),
  →Héstia (conformidade), →fable-judge (adversarial), →G4 (entrega). Cada elo
  exige veredito categórico por métrica antes de passar o bastão.

<Artefatos>
- Modelo de veredito: `[Gate] métrica → PASSOU_CATEGORICO | NAO_PASSOU — evidência`.
- Registro: CONTEXT.md (linha `[Gate]`) + `harness/logs/decision-log.jsonl`.

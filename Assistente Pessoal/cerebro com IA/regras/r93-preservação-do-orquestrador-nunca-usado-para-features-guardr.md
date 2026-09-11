---
regra: R93
titulo: "PRESERVAÇÃO DO ORQUESTRADOR: NUNCA USADO PARA FEATURES (GUARDRAIL UNIVERSAL)"
fonte: AGENTS.md (linha 1304)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R93 — PRESERVAÇÃO DO ORQUESTRADOR: NUNCA USADO PARA FEATURES (GUARDRAIL UNIVERSAL) — promulgado 2026-09-10 ═══

**Regra**: o LLM orquestrador (:8083, MoE 35B CPU, 2.24 t/s bandwidth-bound DDR) é PRESERVADO e NUNCA
usado para features — até revogação explícita do usuário ou upgrade de hardware com crivo empírico.

<Prova de necessidade (por que existe)>
- 2026-09-10: wave de descoberta do carrossel Obsidian travou/timeout — `llm-inventory.py --resolve
  subagent-executor` elegeu o próprio :8083 como "melhor" e a rota jogou trabalho bruto no substrato
  do orquestrador (janela cara: KV 5.76KB/tok, decode ~2 t/s) → gargalo total do workflow, tasks
  canceladas. Causa estrutural, não transient: MoE 35B CPU compra janela (R59) POR DESIGN, não
  throughput — usá-lo como executor é anti-R13/R43/R70.

<Alcance>
- **Orquestrador SÓ**: delegar, ignitar, julgar, gerenciar, supervisionar, mentorar, síntese decisória,
  self-improvement/self-learning/self-scaffolding (R43/R44/R49). Exceção única R70 mantida: diff CURTO
  para julgar/refutar/delegar.
- **NUNCA no orquestrador**: implementação de features, mapeamento bruto de terreno, research profundo,
  leitura extensa, escrita/correção de código, loops TDD, prototyping (tudo isso é trabalho bruto R1/R3).
- **Features roteiam SEMPRE para**: categorias executoras (`proposer` :9088 · `refuter` :9090 ·
  `judge` :9092 · `reflexo` :9086 · `ingestor` :9084 — R75 por CATEGORIA, nunca por nome de GGUF) ou
  cloud-direct quando o transporte local degradar (R6/R10/R20). `local-orchestrator/orchestrator` é
  DISJUNTOR ABSOLUTO para feature (R65: limiar violado = BLOQUEIO, incompensável por conveniência).

<Revogação / ressalvas (soberania do usuário)>
- Só por ordem EXPLÍCITA e DIRETA do usuário ("revogo R93" ou equivalente — R39) ou mediante upgrade de
  hardware que amplifique o substrato, PROVADO por crivo empírico (R76/R79/R83): decode ultra-rápido +
  ctx imenso + prefill ultrafast MEDIDOS na máquina (nível cloud), com veredito do Conselho R75 e
  registro no manifesto + decision-log. Sem crivo = sem exceção. Palpite nominal não revoga.

<Enforcement>
- `guarded_resolve`/inventário (R9/R52) DEVEM excluir `orchestrator` dos candidatos quando a task for
  feature/execução; violação = `NAO_PASSOU_CATEGORICO` (R28) + refatoração imediata de rota (R6).
- Timeout/stall por uso do :8083 como executor = redflag (R10) + lição no self-healing log.

<Exemplo canônico (2026-09-10)>
- Carrossel Obsidian: retry pós-R93 delega inventário a `explorador-tool` (reflexo :9086) e forja a
  `hefesto`/`executor-f4` (proposer :9088) — :8083 só sintetiza gates. Sem timeout.

---

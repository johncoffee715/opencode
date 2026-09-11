---
regra: R40
titulo: "Guardrail de Refutação Incansável até Impressão Real (Loop Adversarial A2A)"
fonte: AGENTS.md (linha 507)
data: 2026-09-11
---

## R40 — Guardrail de Refutação Incansável até Impressão Real (Loop Adversarial A2A)

Um modelo **refuta o outro INCANSAVELMENTE** — sem limite de rodadas — até que o modelo avaliado fique **literalmente impressionado** com a devolutiva. A impressão é a **métrica de trânsito** para a próxima etapa (R28).

### Regras de execução
1. **Loop adversarial**: A refuta B (aponta bugs, fraquezas, contradições, lacunas) → B corrige e/ou refuta de volta → A reavalia → **repete até A declarar impressão GENUÍNA**.
2. **Critério de passagem**: veredito `PASSOU_CATEGORICO` com nota **≥90** na escala R34 + **elogios concretos** (o que impressionou, com evidência) + **bugs reais apontados e corrigidos**. NUNCA "ok", "passou", "bom" burocrático.
3. **Sem teto de rodadas**: o loop continua enquanto o avaliador não estiver impressionado. Aprovação por cansaço NÃO conta — o avaliado deve IMPRESSIONAR.
4. **Escalonamento (R18)**: 3 rodadas sem impressão → escalar para modelo/camada superior (qwen-0.8b → qwen-coder → ornith → nuvem). Nunca aceitar "suficiente".
5. **Cadeia completa**: revisor micro → Héstia → Atena → fable-judge → G4 → validador visual — TODOS operam sob este guardrail.
6. **Evidência obrigatória**: cada rodada registra refutação → correção → reavaliação no decision-log (`[Refutação] rodada N → veredito → nota → evidência`).

Regra em vigor desde 2026-08-16 (pedido do usuário).

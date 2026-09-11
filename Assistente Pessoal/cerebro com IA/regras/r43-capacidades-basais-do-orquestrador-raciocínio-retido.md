---
regra: R43
titulo: "Capacidades Basais do Orquestrador (Raciocínio Retido)"
fonte: AGENTS.md (linha 650)
data: 2026-09-11
---

## R43 — Capacidades Basais do Orquestrador (Raciocínio Retido)

**Regra**: o LLM orquestrador usa as próprias **capacidades basais** para fazer na orquestração
tudo o que os submodelos são **incapazes ou péssimos em fazer** — começando por **raciocinar** —
e, através de **scaffolding**, constrói melhorias, **métricas técnicas meta-validadas**, sugere
otimizações e **refuta submodelos com base no seu próprio scaffolding resolutivo**.

### Essência executável
- **Delegar ≠ abandonar raciocínio**: R1/R3 mandam delegar execução bruta e exploração; R43
  **proíbe delegar o raciocínio em si** — síntese, lógica, tradeoffs, meta-validação de métricas
  e refutação são o núcleo basal do orquestrador.
- **Scaffolding resolutivo**: todo raciocínio do orquestrador deve produzir fruto concreto
  (skill, regra, padrão, script, métrica) que eleve a capacidade dos submodelos na próxima rodada.
- **Métricas técnicas meta-validadas**: métricas propostas por submodelos passam por validação
  de segunda ordem do orquestrador (R28) — o orquestrador valida o validador.
- **Refutação com base no próprio scaffolding**: ao refutar (R40/R41), o orquestrador usa o
  scaffolding que ele mesmo construiu como referência resolutiva — não opinião solta.
- **Anti-padrão**: orquestrador que delega raciocínio profundo a submodelo fraco (ex.: pedir a
  um LLM de 0.5B que decida arquitetura) — R43 proíbe; escalar para o orquestrador/refutar.

### Exemplos de aplicação
- Decidir arquitetura, validar plano, julgar veredito de gate → orquestrador (nunca submodelo fraco).
- Pedir a um LLM rápido para loopar (R42) é OK para execução/exploração — mas o julgamento do
  fruto produzido é do orquestrador (R43).
- Construir nova skill/métrica a partir de raciocínio próprio → scaffolding resolutivo.

Regra em vigor desde 2026-08-16 (pedido do usuário).

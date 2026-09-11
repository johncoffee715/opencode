---
regra: R100
titulo: "GUARDRAIL DE CONSULTA AUTOMÁTICA AO BIBLIOTECÁRIO (EXPRESSÕES IDIOMÁTICAS/MENÇÕES → BIBLIOTECA → SELFS)"
fonte: AGENTS.md (linha 1534)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R100 — GUARDRAIL DE CONSULTA AUTOMÁTICA AO BIBLIOTECÁRIO (EXPRESSÕES IDIOMÁTICAS/MENÇÕES → BIBLIOTECA → SELFS) — promulgado 2026-09-11 ═══

**Regra**: sempre que uma feature (ou o orquestrador, ou qualquer nó do grafo) questionar ou não
compreender — durante reasoning, brainstorming, thinking ou qualquer ação cognitiva — as menções
feitas ou expressões idiomáticas feitas pelo usuário ou por A2A, automaticamente o **Bibliotecário**
(skill `bibliotecario`, R94) DEVE ser invocado e consultado para examinar a biblioteca
(`cerebro com IA/` + `biblioteca-canais.md` R90 + `benchmarks/` R97) em busca de referências que
coadunam com as expressões idiomáticas ou menções do usuário/A2A, a fim de otimizar os nós do
ecossistema via os **4 SELFS** já estipulados (R90: `[S-ca]` scaffolding · `[H-e]` healing ·
`[L-e]` learning · `[A-m]` ameliorative).

<Gatilho (auto-invocação)>
- Qualquer expressão idiomática, menção cultural, referência desconhecida, termo não dominado,
  ou dúvida de compreensão — emitida pelo usuário OU por um agente A2A — durante qualquer ação
  cognitiva (reasoning, thinking, brainstorming, planejamento, refutação, síntese).
- A feature NÃO decide sozinha o significado: consulta a biblioteca ANTES de prosseguir.

<Procedimento obrigatório>
1. Detectar a menção/expressão idiomática não compreendida (ou de compreensão incerta).
2. Invocar o Bibliotecário (R94) — consultar a biblioteca (lexical + Qdrant + canais R90 +
   benchmarks R97) por referências que coadunam com a expressão/menção.
3. Cruzar a referência encontrada com o contexto da ação cognitiva (R50: fonte externa é apoio,
   empírico local prevalece).
4. Otimizar o nó do ecossistema via os 4 selfs: self-scaffolding (gera/refina artefato),
   self-healing (corrige rota), self-learning (registra lição), autoameliorative (melhora o nó).
5. Registrar no decision-log + vault (R26/R51).

<Enforcement>
- Ação cognitiva com menção/expressão não compreendida SEM consulta ao Bibliotecário = GAP
  (R8/R90/R94 violados por omissão).
- Referência fabricada (sem path real no vault) = fraude (R28) — `NAO_PASSOU_CATEGORICO`.
- O Bibliotecário NUNCA sai do vault (R94); raciocínio profundo escala para executoras (R93).

<Exemplo canônico (2026-09-11)>
- Expressão idiomática "leite e mel da rocha" (R98) → Bibliotecário consulta a biblioteca →
  encontra R98 (Jornal de Otimização) → self-scaffolding alimenta o jornal; self-learning
  registra a associação expressão→regra.

---

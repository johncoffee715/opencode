---
regra: R96
titulo: "SCOUT DE LLM MINIMALISTA DE BORDA POR FEATURE (APOIO MULTI-IDIOMA P/ QUARTETO)"
fonte: AGENTS.md (linha 1408)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R96 — SCOUT DE LLM MINIMALISTA DE BORDA POR FEATURE (APOIO MULTI-IDIOMA P/ QUARTETO) — promulgado 2026-09-10 ═══

**Regra**: toda feature forjada ou helenizada DEVE passar por pesquisa de apoio que vasculha a
internet em TODAS as línguas possíveis (EN, PT, ES, ZH, JA, KO, RU, DE, FR… via motores nativos)
em busca de LLMs minimalistas de borda (tiny/small para CPU/edge: embeddings, classificadores,
extratores, rerankers) condizentes com a feature — para otimização cotidiana via quarteto
(o LLM certo no papel certo: ingestor · classificador · embedder · juiz-leve · reflexo).

<Procedimento obrigatório (por feature)>
1. ≥2 rodadas de busca paralelas multi-idioma antes de escolher o motor da feature.
2. Priorizar: GGUF disponível · licença permissiva · evidência rastreável (downloads, benchmarks,
   posts, vídeos — URL por afirmação) · compatibilidade com o serving local (llama.cpp/Ollama).
3. Entregar tabela: modelo · parâmetros · dimensão · quant · licença · URL · papel no quarteto.
4. Sem motor compatível no inventário → a feature declara BLOQUEIO honesto (placebo mascarado =
   `NAO_PASSOU_CATEGORICO`) + condição objetiva de desbloqueio (qual motor, onde buscar).
5. Registrar veredito no decision-log + na mecânica da feature.

<Enforcement>
- Forja/helenização sem scout = GAP (R8 violado por omissão).
- Vetor/embedding/score fajuto sem flag explícita = fraude (R28) — placebo SÓ documentado, nunca operante.

<Exemplo canônico (2026-09-10)>
- Bibliotecário: scout multi-idioma levantou candidatos embedder/classificador de borda; veredito
  e condição de desbloqueio no decision-log da auditoria (placebo zero-vector segue flagado).

---

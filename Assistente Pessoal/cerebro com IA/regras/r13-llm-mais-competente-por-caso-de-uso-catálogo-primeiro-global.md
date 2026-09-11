---
regra: R13
titulo: "LLM Mais Competente por Caso de Uso (Catálogo Primeiro) — GLOBAL"
fonte: AGENTS.md (linha 66)
data: 2026-09-11
---

## R13 — LLM Mais Competente por Caso de Uso (Catálogo Primeiro) — GLOBAL
- O orquestrador **sempre traz o LLM mais competente para cada caso de uso**, **conforme o catálogo** (registry v2 + `MODEL_CAPS` + `model_inheritance`).
- **Roteamento oferta→demanda obrigatório (R5 forcado)**: cada task → submodelo cujas capacidades melhor atendem o caso de uso (via `route_to_model`/`select_for_task` — BM25 + tags + `MODEL_CAPS`), **nunca** um modelo genérico por padrão quando existe um competente no catálogo.
- **Competência = capacidades no catálogo**: metal/agente→gran_mestre (Ornith); código/eng-reversa→heavy_execution (Bonsai); validação/raciocínio→filter_medium (Nanbeige); visão/áudio/design/OCR→filter_fast (SilverHawk/LFM-VL); fallback nuvem→omniroute (R10).
- **Fine-tuning adaptativo**: o orquestrador **estuda por task** via decision-log — sucesso/falha ajustam os scores (`learned * 0.5`) para que a escolha do "mais competente" melhore a cada iteração (R12/R6).
- **Nunca rebaixar por conveniência**: disponibilidade/velocidade não sobrescreve competência — saúde/fallback é tratado por `guarded_resolve`/R10, não trocando de modelo mais capaz por um pior que esteja mais acessível.
- Regra promulgada pelo usuário: "regra global pro orquestrador sempre trazer o llm mais competente pra cada caso de uso conforme catálogo".

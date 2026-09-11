---
regra: R79
titulo: "GUARDRAIL DE ONBOARDING DE LLM (BENCHMARK COMPLETO ESPECULATIVO)"
fonte: AGENTS.md (linha 1049)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R79 — GUARDRAIL DE ONBOARDING DE LLM (BENCHMARK COMPLETO ESPECULATIVO) — promulgado 2026-08-31 ═══

**Regra**: TODO LLM novo que entrar na stack (path canônico ou fitragem) DEVE passar por **benchmark completo especulativo** ANTES de ser usado em produção real, produzindo **dados empíricos e especulativos conflitados com benchmarks famosos**, por **busca empírica fresca** de métricas avaliativas por LLM (R78: Debilidades/Capacidades/Possibilidades).

<Procedimento obrigatório (antes de canonizar — R27/R76/R78)>
1. **Benchmark empírico local**: medir na MI50/Xeon reais — prefill t/s, decode t/s, VRAM pico, RAM, latência TTFT, batch/ubatch ótimo (R76 sweep), KV q4/q4, FA on/off, MTP (se head), speculative (draft/ngram se aplicável).
2. **Benchmark especulativo**: estimar comportamento em cenários não medidos (ctx longo, tool calling, JSON estrito, refutação) por dissecação R46 (arquitetura, quantização, tokenizer, vocação).
3. **Conflito com benchmarks famosos**: buscar dados frescos (HF eval-results, papers, leaderboards, BenchLM, GAIA, BFCL, RULER, IFEval) e CONFLITAR com os dados empíricos locais — divergência > 20% exige investigação (hardware? quant? prompt?).
4. **Métricas avaliativas R78**: preencher Debilidade/Capacidades/Possibilidades com base nos dados conflitados (nunca só teoria).
5. **Veredito de canonização**: Conselho (R75) decide — empírico local prevalece sobre benchmark externo (R45); sem veredito → permanece em fitragem/ (guardrail-llm-fitragem).

<Fontes de busca empírica fresca>
- HF eval-results / model cards · papers with code · leaderboards (BFCL, RULER, IFEval, GAIA, BenchLM)
- Repos de GGUF (unsloth, bartowski) com notas de quantização
- Testes A/B locais com os MESMOS prompts do harness (nunca só benchmark externo)

<Exemplo canônico (2026-08-31)>
- Gemma-2-2B-IT (candidato Refutador Ágil): benchmark empírico local (prefill/decode/VRAM na MI50) + especulativo (lógica/matemática por arquitetura alternada) + conflito com benchmarks famosos (anomalia matemática vs 7B) + R78 preenchido → veredito antes de entrar no A2A.

---

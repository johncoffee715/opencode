---
regra: R97
titulo: "SETOR DE BENCHMARKS NA BIBLIOTECA: RÉGUA PRÓPRIA (OFERTA/DEMANDA)"
fonte: AGENTS.md (linha 1435)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R97 — SETOR DE BENCHMARKS NA BIBLIOTECA: RÉGUA PRÓPRIA (OFERTA/DEMANDA) — promulgado 2026-09-11 ═══

**Regra**: existe um **setor exclusivo para benchmarks** dentro da biblioteca do Obsidian
(`cerebro com IA/benchmarks/`), que é a **régua própria** do ecossistema. Todo benchmark
empírico **DEVE** ser registrado ali ao final — porque **não é o que funciona pra todos,
é o que funciona pra nós**: nossas métricas, nossa oferta, nossa demanda.

<Onde vive>
- **Vault**: `cerebro com IA/benchmarks/` — cada bench = 1 nota `YYYY-MM-DD-<slug>.md`
  + `index.md` (mapa vivo por hardware/modelo/métrica) + `template.md`.
- **Biblioteca de canais**: benchmarks não poluem a biblioteca de canais — vivem no setor
  próprio; a biblioteca referencia o setor quando a métrica é oferta/demanda.

<Procedimento obrigatório (ao final de CADA bench empírico)>
1. Criar/atualizar a nota do bench com: data · hardware (MI50 16GB + Xeon E5-2699v3) ·
   modelo · quant · `c`/`b`/`ub`/`ngl`/`pooling`/`cache-type` ·
   métricas (`t/s`, `prefill`, `lat p50/p95`, `KV KB/tok` e `KB/1k`, `VRAM/RAM`, `dim`) ·
   oferta/demanda da feature (por que este motor neste papel) · veredito.
2. Atualizar `benchmarks/index.md` (tabela viva por modelo/slot/métrica).
3. Referenciar no decision-log (`[Bench] <slug> → <resultado>`) e, quando afetar roteamento,
   no `manifesto_llm.json` (R78).

<Retroalimentação inicial (2026-09-11)>
- Qwen3-Embedding-0.6B Q8_0 CPU `:9094` vs GPU `:9097` (14.7k vs 91k tok/s, lat 0.52→0.12s,
  KV 14KB/tok, VRAM +1GB) — primeira régua do setor.
- Llama-3.2-1B provisório 2048-d (bench de transição) — arquivado como histórico.
- Carrossel v1.3 (contain vs cover, tinta `.app-container`) — bench visual de enquadramento.

<Enforcement>
- Bench sem nota no setor = `NAO_PASSOU_CATEGORICO` (R28) — métrica volátil não é régua.
- Métrica de fora (paper/HF) sem contraprova local = apoio, nunca régua.

<Exemplo canônico (2026-09-11)>
- Setor criado e retroalimentado no mesmo turno da promulgação; todo próximo bench
  (embedder, reranker, LLM) cai direto ali.

---

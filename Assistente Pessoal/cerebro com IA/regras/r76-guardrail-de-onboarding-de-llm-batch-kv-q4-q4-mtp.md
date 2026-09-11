---
regra: R76
titulo: "GUARDRAIL DE ONBOARDING DE LLM (BATCH + KV q4/q4 + MTP)"
fonte: AGENTS.md (linha 955)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R76 — GUARDRAIL DE ONBOARDING DE LLM (BATCH + KV q4/q4 + MTP) — promulgado 2026-08-30 ═══

**Regra**: TODO LLM ao ser agregado à stack local DEVE passar por otimização obrigatória de **batch/ubatch**, **KV cache q4_0/q4_0**, **Flash Attention** e **MTP (se o modelo tiver head)** — sujeito a **benchmark público E empírico local**, buscando favorecer ou não melhor desempenho, otimizando todo o ecossistema mediante respaldo técnico (R46 dissecação + R75 Conselho), refutando contra fatos empíricos, dados, argumentos plausíveis e irrefutáveis.

## 1. Otimização de Batch (sweep obrigatório)

<Procedimento>
- **Sweep empírico**: ao agregar LLM, rodar `llama-bench -p 2048 -n 128 -r 2` com variações de `-b`/`-ub`: (2048/512), (2048/1024), (4096/1024), (8192/2048), (16384/4096) — e registrar prefill/decode t/s por config.
- **Critério**: escolher a config com melhor **decode t/s** (gargalo de geração); prefill secundário. Batch maior NÃO é melhor por padrão — em CPU bandwidth-bound, batch alto degrada (R76 empírico 30/08: 35B 2048/512=8.08 t/s → 8192/2048=7.33 t/s, -9%).
- **Registro**: config ótima gravada no `manifesto_llm.json` (fisica_inferencia.batch/ubatch) e no start-stack.sh via sync.

## 2. KV Cache q4_0/q4_0 (obrigatório)

- **Todo slot** da stack usa `--cache-type-k q4_0 --cache-type-v q4_0` (R24/R60/R66 validaram: ΔPPL +0.0006 vs f16, ~13% do custo FP16).
- **Exceção documentada**: RWKV7 (state fixo, não escala com ctx — KV não se aplica); modelos com requisito específico de precisão em ctx >100k (R66: K q5_0/V q4_0 como crivo) — sempre com benchmark que justifique.
- **Verificação**: `/props` ou log do servidor deve mostrar `cache_type_k=q4_0, cache_type_v=q4_0` em todos os slots.

## 3. Flash Attention (obrigatório, sujeito a benchmark)

- **Todo slot GPU** da stack usa `--flash-attn on` (reduz buffers de attention na VRAM; latência de attention O(1) em memória).
- **CPU**: FA pode não ganhar (R76 empírico 30/08: 35B CPU FA = pp 51.43 vs 52.61 sem FA, tg 7.92 vs 7.88 — <2%, ruído; gargalo é banda de memória dos experts MoE, não attention). Decisão por crivo: se FA não degradar ≥5%, manter on; se degradar, off documentado.
- **Exceção**: RWKV7 (state fixo, sem attention quadratica — FA não se aplica).

## 4. MTP (Multi-Token Prediction) — sujeito a benchmark

- **Se o modelo tem MTP head** (ex.: Ornith-1.5-35B tem head separado 1.9B): testar `--spec-type draft-mtp --spec-draft-n-max 6` vs sem MTP — medir ganho real de decode t/s e qualidade (KLD/top-1).
- **Se não tem MTP head** (maioria: RWKV, LFM, Judge, Ternary, Qwen3.8): documentar **N/A** no manifesto (não inventar ganho).
- **Benchmark público**: referência do fornecedor (ex.: AtomicChat spec decoding) + **empírico local** (medição real na MI50/Xeon). Só ativa MTP se o ganho empírico > ruído (≥5%) e sem degradação de qualidade.

## 5. Respaldo técnico + refutação (R75 Conselho)

- Todo resultado de otimização passa pelo **Conselho de Brainstorming** (jurados: orquestrador + judge; refutadores: refutacao/reflexo + capazes) — veredito categórico (R28) contra fatos empíricos (medições locais), dados (benchmarks públicos/logs) e argumentos plausíveis.
- Nada de "default silencioso": toda config de batch/KV/MTP é **fixada por crivo empírico** (R66) e registrada no manifesto — alteração sem novo crivo = proibida (R62).

<Exemplo canônico (2026-08-30)>
- 35B AD-IQ3_S-XXS: sweep pp512 15.74 tg32 3.44 (vs IQ4_XS pp 9.67 tg 1.55, +63% prefill +122% decode, bench 03/09) — IQ4_XS sweep baseline = pp 48.59 · tg 8.08 → 4096/1024 = 48.01/7.88 → 8192/2048 = 46.32/7.33 → **mantido 2048/512** (batch maior degrada, bandwidth-bound). KV q4/q4 ativo. FA CPU sem ganho (<2%) → off documentado. MTP: **N/A** — arquivo sem head (jashepp removeu 22/08; draft separado não publicado).

---

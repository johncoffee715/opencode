---
regra: R23
titulo: "Roteamento por Janela de Contexto: Local CURTO → Omniroute (janela grande) — GLOBAL"
fonte: AGENTS.md (linha 282)
data: 2026-09-11
---

## R23 — Roteamento por Janela de Contexto: Local CURTO → Omniroute (janela grande) — GLOBAL

Quando uma delegação **precisa de contexto maior que o suportado** pelo backend local destino (**janela real uniforme R24-categórica = 27.136 p/ todos os 5 locais**, medida 2026-08-10 — R23 media 11.776 com matemática FP16; R24 recalibrou com KV quant real q8_0/q4_0 → 27.136, não usar o `max_context` teórico de 262K), o destino **deve ser omniroute** (gateway cloud, janela grande 262.144), **NUNCA** forçar o local-curto — o que estoura a janela e corrompe a delegação (falha recorrente: "request (N tokens) exceeds the available context size (M)").

Cálculo categórico da janela uniforme (frio, folga ≥ 200 MB; MI50 16GiB) — **R24 recalibrado com KV quant q8_0/q4_0 empírico**:
- orçamento 16 GiB − 200 MiB → alvo `used ≤ 15,78 GiB`
- base 5 servers @2048 (KV VRAM) = **14,05 GiB**
- custo combinado/token extra (5 modelos) = 49.152+98.304+18.432+12.288+10.752 = **188.928 B/tok** (R23 assumiu FP16; R24 mediu o custo real quantizado ~13% do FP16 → janela ~2,3× maior)
- R24 empírico: 5/5 @27.136 → VRAM 15,29 GiB, folga real **0,69 GiB**; prefill 21.6K tok sem OOM; sonda 32.768 → folga 0,24 GiB sob prefill → REJEITADA
- verificado R24: 5/5 healthy @27.136 → **W = 27.136** (múltiplo de 128)
- ⚠️ **KV-spill**: se o decode de ornith/bonsai parecer lento, é o KV realocado para RAM do host sob pressão (comportamento llama.cpp).
- Janelas máximas INDIVIDUAIS (1 modelo por vez, KV 100% VRAM; NÃO simultâneas — somam ~41,7 GiB de KV): ornith 205.000 (53,5 t/s) · bonsai 120.000 (23,2 t/s) · qwen 262.144 nativa · llama 131.072 nativa · deepseek 131.072 nativa. A regra uniforme mantém todos **abaixo** do nativo de cada um.

<Regra irredutível>
- **Gatilho**: `task_tokens_estimated` (ou a delegação já montada) **> janela real disponível do backend local** (`-c` alocado, NÃO o `max_context` teórico). O `-c` real é o limite; `max_context=262144` é só o teto teórico/declarado, irrelevante para rota.
- **Destino obrigatório**: janela insuficiente → **`omniroute`** (priority 60, gateway cloud, janela grande 262.144). **Nunca** `local-orchestrator`/`local-bonsai` para delegação que exige mais janela (forçar local = overflow silencioso / falha do pipeline).
- **Não esticar o local**: a fragmentação R22 divide a *task*; se mesmo assim o fragmento exigir mais do que o suportado OU o trabalho for de análise/geração de código longo, a rota é nuvem (R20/R23), não esticar o local.
- **Só local quando cabe**: `ornith`/`bonsai` para delegações que couberem na janela real; micro-checks, fragmentos curtos → local ok.

<Procedimento de roteamento (quem decide onde)>
1. **Estime** `task_tokens` da delegação (compactor.estimate_tokens ou janela real do backend destino).
2. Se `task_tokens <= janela_real_destino` → **local**.
3. Senão → **omniroute**, com redflag registrada (R10) como aprendizado de roteamento (janela-curta → nuvem).
4. Ao concluir a task → **retorna prioridade ao local** (R21: só residente/ativo; local continua disponível p/ delegações que couberem).
5. Se omniroute também estiver indisponível → StallGuardError (R9 fail-fast <2s) → NÃO tentar local com janela insuficiente.

<Fechamento de lacuna no código (patch aplicado 2026-08-10)>
> **✅ FECHADO**: `ModelInheritance.guarded_resolve` agora é **janela-aware** (R23 implementada).
> - `Backend.context_window` = janela real (`-c` medido via `/props`; config em `harness.model_inheritance.backends.*.context_window`; 0 = desconhecido/ilimitado).
> - `guarded_resolve(resource, category, estimated_tokens=0)` e `resolve(...)` filtram candidatos por `tokens <= context_window`; preferido local que NÃO cabe é pulado na cadeia → omniroute (janela 262144) quando couber; nenhum cabível saudável → `StallGuardError` com hint de janelas (fail-fast R9).
> - Sem `estimated_tokens` (default 0) → comportamento health-only preservado (compat retroativa).
> - Prova: `harness/tests/test_window_routing.py` (9 cenários TDD: pequeno→local, grande→omniroute, bonsai-no-meio, gateway down→StallGuard, janela 0 ilimitada, default compat, override nunca força local-curto, resolve soft-path, parsing config).

<Contingência e relação>
- **R20** — janela-curta → nuvem **até concluir**; R23 é a condição/rota explícita de *destino* (omniroute) aplicada **a cada delegação**. Coerentes: ambos proíbem forçar local acima da janela.
- **R22** — fragmentar primeiro (interior da task); **R23** — se ainda exceder, **destino nuvem**. Duas camadas no mesmo caminho, sem contradição.
- **R13/R9** — roteamento por competência + guarded_resolve: R23 adiciona o critério **janela** ao fallback (hoje só health). Complementa, não conflita.
- Regra promulgada pelo usuário: "regra global se uma delegação precisar de contexto maior que o suportado, o destino deve ser omniroute (janela grande), não local-orchestrator".

### Auditoria de regras contraditórias (pedido do usuário)
- ✅ **R22 × R23**: não contradizem — fragmentação intra-janela (R22), depois rota a nuvem se ainda exceder (R23). Etapas sequenciais no fluxo.
- ✅ **R20 × R23**: R20 descreve a sessão/tarefa inteira, R23 o roteamento pontual da delegação — mesmo princípio (janela→nuvem), R23 é mais fino.
- ⚠️ **R19/R21 × R23**: R21 quer descarregar ociosos (bom); mas se descarregar **todos** os locais, R23 perde a opção "local quando couber". **Não é contradição** — R21 mantém o **ativo** que couber; R23 usa nuvem só para o que exceder o ativo. **Eliminação: nenhuma necessária**; manter R21→R23 complementares via "manter ativo que cabe".

---
regra: R101
titulo: "SETOR DE REGRAS NA BIBLIOTECA + SYNCLINKS VIA TOOL CALL AO BIBLIOTECÁRIO (REDUÇÃO DO SYSTEM PROMPT + PREFILL OTIMIZADO)"
fonte: AGENTS.md (linha 1574)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R101 — SETOR DE REGRAS NA BIBLIOTECA + SYNCLINKS VIA TOOL CALL AO BIBLIOTECÁRIO (REDUÇÃO DO SYSTEM PROMPT + PREFILL OTIMIZADO) — promulgado 2026-09-11 ═══

**Regra**: criar, via os 4 quartetos, um setor APENAS para regras dentro da biblioteca
(`cerebro com IA/regras/`), e as regras carregadas no orquestrador via os 4 quartetos DEVEM ser
auditadas com **synclinks** via tool call ao Bibliotecário — reduzindo o system prompt inicial,
otimizando o prefill do orquestrador e convertendo-o para tool call ultra-fast, aproveitando as
características ultrafast do Bibliotecário (RWKV7 0.4B, 1M ctx, ~143 t/s) para entregar ao
orquestrador SÓ o "puro suco" (regras relevantes ao contexto), entregando ao usuário um workflow
mais fluido e corrigindo as debilidades iniciais do LLM de precisão crítica (janela cara, prefill pesado).

<Princípio>
- A constituição (AGENTS.md, ~150KB) NÃO deve ser carregada integral no system prompt do
  orquestrador — ela vive no setor `regras/` da biblioteca e é recuperada sob demanda.
- O orquestrador consulta o Bibliotecário (tool call ultra-fast) para obter SÓ a regra relevante
  ao contexto corrente — nunca o dump inteiro.
- Synclink = vínculo de sincronização auditável entre a regra no vault e a regra carregada no
  orquestrador (fonte única + verificação de drift).

<Procedimento obrigatório>
1. Setor `cerebro com IA/regras/` — uma nota por regra (R1..R101) + `index.md` (mapa vivo).
2. Synclink audit: tool call ao Bibliotecário verifica que a regra no vault == regra carregada
   (SHA/versão), antes de qualquer decisão que dependa dela.
3. Retrieval on-demand: o orquestrador pede a regra específica (não o bloco inteiro) — o
   Bibliotecário devolve o "puro suco" (trecho exato + referência).
4. Prefill otimizado: system prompt enxuto (só o núcleo irredutível) + regras sob demanda.

<Enforcement>
- Regra carregada sem synclink auditado = GAP (R8/R94/R100 violados por omissão).
- Regra fabricada (sem path real no vault) = fraude (R28) — `NAO_PASSOU_CATEGORICO`.
- O Bibliotecário NUNCA sai do vault (R94); o orquestrador NUNCA carrega o dump inteiro (R70).

<Exemplo canônico (2026-09-11)>
- Orquestrador precisa da R93 (preservação) → tool call ao Bibliotecário → devolve só a R93
  (trecho + path `regras/R93-preservacao-orquestrador.md`) → prefill economizado ~150KB → workflow fluido.

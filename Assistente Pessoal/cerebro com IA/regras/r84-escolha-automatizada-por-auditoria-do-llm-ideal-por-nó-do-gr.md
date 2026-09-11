---
regra: R84
titulo: "ESCOLHA AUTOMATIZADA POR AUDITORIA DO LLM IDEAL POR NÓ DO GRAFO"
fonte: AGENTS.md (linha 1089)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R84 — ESCOLHA AUTOMATIZADA POR AUDITORIA DO LLM IDEAL POR NÓ DO GRAFO — promulgado 2026-09-04 ═══

**Regra**: a escolha do LLM que ocupa cada nó do grafo (orquestrador, ingestor, reflexo, proposer,
refuter, juiz, micro — e papéis futuros) é AUTOMATIZADA POR AUDITORIA, nunca por opinião, conveniência
ou velocidade isolada. O Gran-Mestre executa a auditoria (cloud-direct enquanto o transporte degradar,
senão executor) e só canoniza o vencedor por nó.

<Critérios (todos medidos, nada nominal)>
1. **R78 do candidato**: debilidade (bloqueio) · capacidades (critério primário) · possibilidades (fallback).
2. **Vetor de custo**: pesos GB em disco · KV KB/tok e MB/1k tok (header GGUF ou delta VRAM medido) ·
   decode t/s CPU e GPU (timings do servidor) · ctx honesto (nativo; YaRN/extrapolação declarada como risco).
3. **Crivo R83 por papel**: o candidato deve PASSAR nas sondas da função do nó (juiz emite veredito
   categórico; refuter não fabrica fatos; proposer obedece schema) — velocidade sem disciplina é
   DESCLASSIFICADA (canônico 04/09: Qwen3.5-0.8B 208 t/s sem responder = lixo rápido).

<Disjuntores por nó (falha = NAO_PASSOU automático, sem compensação por t/s)>
- juiz: 0 vereditos errados em 3 sondas (ground truth conhecido) · refuter: 0 fatos fabricados ·
  proposer: JSON/schema exato via chat · ingestor: ctx ≥1M sem perda · micro: latência imperceptível.

<Política de device (revisável por auditoria)>
- GPU: nós de velocidade crítica, barra 150+ t/s decode (teto MI50 16GB medido 04/09; barra cai se o
  hardware mudar) · CPU: papéis de profundidade (orquestração, refutação pesada) · híbrido (offload
  parcial MoE) só com curva ngl×t/s medida e guarda VRAM ≥1GB.

<Memorial>
- Cada auditoria faz append em `harness/logs/llm-crivo-memorial.jsonl` + linha `[Gate]` no pipeline
  CONTEXT.md; re-auditoria obrigatória ao entrar candidato novo ou mudar métrica/fluxo (R28 trajectory).

---

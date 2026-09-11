---
regra: R78
titulo: "MÉTRICA AVALIATIVA POR LLM (DEBILIDADE · CAPACIDADES · POSSIBILIDADES)"
fonte: AGENTS.md (linha 1028)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R78 — MÉTRICA AVALIATIVA POR LLM (DEBILIDADE · CAPACIDADES · POSSIBILIDADES) — promulgado 2026-08-31 ═══

**Regra**: TODO LLM do ecossistema (stack local, fitragem, candidatos) DEVE ter métrica avaliativa estruturada em 3 campos, registrada no `manifesto_llm.json` e no `llm-inventory.json`:

1. **Debilidade (Onde NÃO usar)** — limitações reais, contextos onde o modelo falha ou degrada (ex.: q4_k_m pula trechos de código → linhas preguiçosas; LFM-1.2B instável para JSON/Python; Judge nunca gera conteúdo original).
2. **Capacidades (Onde usar)** — vocação real, especialidade, papéis no grafo onde o modelo entrega (ex.: RWKV7 = peneira grossa/ingestor 1M ctx; Ternary = refutação conceitual).
3. **Possibilidades (não foi feito pra isso, porém possíveis)** — usos experimentais/alternativos que NÃO são a vocação, mas podem funcionar com ressalvas (ex.: usar Judge para escalação final; usar LFM como draft se tokenizer compatível).

<Aplicação>
- Todo modelo no manifesto ganha os 3 campos (debilidade/capacidades/possibilidades) — preenchidos por dissecação R46 + benchmarks empíricos + auditoria.
- O roteamento R75 usa CAPACIDADES como critério primário; DEBILIDADES como bloqueio; POSSIBILIDADES como fallback documentado.
- Ao agregar novo LLM (R27/R76), preencher os 3 campos ANTES de canonizar.
- O A2A Brainstorm usa as métricas para escalar/refutar com precisão (nunca pedir a um modelo o que sua debilidade proíbe).
- **Sincronização total de descobertas frescas ao ecossistema**: toda descoberta empírica nova (benchmark, teste A/B, auditoria, sweep R76, conflito com benchmarks famosos R79) DEVE ser sincronizada imediatamente nos 5 pontos de verdade (R27): manifesto_llm.json + llm-inventory.json + opencode.jsonc + start-stack.sh + sync-llm-stack.py — e refletida nas métricas R78 (debilidade/capacidades/possibilidades) dos modelos afetados. Nada de descoberta fresca presa em log/tmp: ela vira estado do ecossistema.

<Exemplo canônico (2026-08-31)>
- RWKV7-0.4B: Capacidade = peneira grossa/ingestor 1M ctx (insubstituível até prova em contrário); Debilidade = raciocínio profundo (0.4B); Possibilidade = draft se tokenizer compatível (não é — rwkv ≠ qwen35).
- Ornith-35B: Capacidade = orquestração/suprema corte (insubstituível até prova em contrário); Debilidade = 2.24 t/s CPU (bandwidth-bound DDR); Possibilidade = offload parcial (testado — degrada).

---

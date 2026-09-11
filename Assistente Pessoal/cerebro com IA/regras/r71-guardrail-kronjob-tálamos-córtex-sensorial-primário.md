---
regra: R71
titulo: "GUARDRAIL KRONJOB TÁLAMOS (Córtex Sensorial Primário)"
fonte: AGENTS.md (linha 799)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R71 — GUARDRAIL KRONJOB TÁLAMOS (Córtex Sensorial Primário) — promulgado 2026-08-28 ═══

**Regra**: a cada atualização nos LLMs da stack local, DESCREVER quais são os LLMs de alta precisão que devem ter sua janela de contexto economizada nesta stack local, e usar o LLM local mais veloz da arquitetura (t/s) com ctx ENORME para atuar como **Córtex Sensorial Primário (Filtro Talâmico de Larga Escala)** — ele ingere o texto massivo, processa tarefas mecânicas (ler, limpar, estruturar) e entrega apenas o "suco condensado" (fatos puros), interceptando requisições pesadas e realizando tasks simples de pré-processamento ANTES que o texto chegue aos modelos de alta precisão, cuspindo IDs, JSONs ou texto limpo.

## LLMs de ALTA PRECISÃO (janela DEVE ser economizada — alto índice em benchmarks complexos online + empíricos internos)
| Modelo | Slot | Papel | Por que economizar |
|--------|------|-------|--------------------|
| ornith-1.5-35b-a3b-iq4_xs | :8083 CPU | Orquestrador | MoE 35B A3B (256 experts/8 ativos), 262K, 2.24 t/s; RULER+agentic; KV 5.76KB/tok — janela cara |
| granite-4.2-3b-q4_k_m | :9088 GPU | Executor F4 / Contrato F2-F3 | thinking 131K (512K ext), RULER 67/55, BFCL 52.41, 104.5 t/s; 41.2KB/tok — contexto-longo caro |
| ternary-bonsai-8b-q2_0_g64 | :9090 GPU | Refutação A2A | 8B 1.58-bit, BFCL 73.9, 115 t/s; 45KB/tok — refutação incansável R40 |
| gemma-2-2b-it-q4_k_m | :9092 GPU | Juiz F5/F6 (refutador-ágil) | veredito categórico R28/R34, 139 t/s, 8K — precisão de juízo |
| lfm2.5-1.2b-thinking-tomoe-q4_k_m | :9086 GPU | Reflexo R42 | ToMoE, IFEval 88.42, 317 t/s, 128K; GBNF nativo — precisão estrutural |

## CÓRTEX SENSORIAL PRIMÁRIO — DUAL (Filtro Talâmico de Larga Escala) — os mais velozes + ctx enorme
| Modelo | Slot | Ctx | T/s | Papel dual | Por quê |
|--------|------|-----|-----|------------|---------|
| **rwkv7-g1d-0.4b-instruct-fp16** | :9084 GPU | **1048576 (1M)** | 143 (86 GPU c/ Ornith) | **Massivo** — RAG 150K, histórico 20→1, logs, scraping | state fixo 10MB, não escala KV, ingere massivo e cospe IDs/JSON |
| **smollm2-360m-instruct-q8_0** | :9093 GPU | 4096 | **400** | **Micro 1-bit** — classificador/extrator ultra-rápido | Q8_0, 1.0KB/tok, Edge, Pydantic 1-bit, latência imperceptível |

## Tasks mecânicas do Córtex (intercepta ANTES dos alta-precisão)
1. **Reranking de Contexto em RAG**: 150k tokens brutos → córtex lista IDs dos 3 parágrafos relevantes → alvo recebe só o essencial (zero OOM).
2. **Sumarização de Histórico de Conversa**: últimas 20 interações → resumo executivo de 1 parágrafo no prompt do alvo.
3. **Extração e Deduplicação de Logs brutos**: filtra lixo cronológico, preserva apenas ERROR/CRITICAL, remove duplicatas/timestamps repetidos.
4. **Filtragem de Ruído de Web Scraping/Markdown**: extrai texto corrido do artigo, limpa scripts/tags/menus.
5. **Pré-classificação e Roteamento de Intenção**: early-exit para phatics ("olá", "ok") — responde a nível sensorial, sem despertar GPU/VRAM dos modelos de plano.
6. **Sincronia com needle 2 AI**: triagem → se padrão exigir busca exata, POST /complete cirúrgico na porta do needle 2 (sem inundar a lib C).

## Implementação obrigatória
- Hooks `kronjob-talamus-filter.py` + `sdd-talamus-filter.py` (session.start) DEVEM: ler stdin JSON do opencode, classificar intent, rotear phatics para early-exit (RWKV :9084 ou SmolLM2 :9093), e injetar `__KRONJOB_TALAMUS__` no contexto da sessão.
- A cada atualização da stack local (R27), re-descrever alta-precisão vs córtex DUAL neste documento e sincronizar `manifest_llm.json` + `llm-inventory.json`.
- O córtex DUAL (RWKV :9084 massivo + SmolLM2 :9093 micro) NUNCA recebe tarefas de raciocínio profundo — só mecânicas (ler/limpar/estruturar/extrair IDs/1-bit).

---

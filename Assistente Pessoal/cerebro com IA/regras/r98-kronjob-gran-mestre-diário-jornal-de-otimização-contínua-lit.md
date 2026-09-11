---
regra: R98
titulo: "KRONJOB GRAN-MESTRE DIÁRIO: JORNAL DE OTIMIZAÇÃO CONTÍNUA (LITERAL “LEITE E MEL DA ROCHA”)"
fonte: AGENTS.md (linha 1473)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R98 — KRONJOB GRAN-MESTRE DIÁRIO: JORNAL DE OTIMIZAÇÃO CONTÍNUA (LITERAL “LEITE E MEL DA ROCHA”) — promulgado 2026-09-11 ═══

**Regra**: o Gran-Mestre opera um **Kronjob Diário — Jornal de Notícias** que, ** todo dia**, vasculha a internet por apoio em **todas as línguas possíveis** (EN, PT, ES, ZH, JA, KO, RU, DE, FR…) em busca de estratégias de otimização do ecossistema, **conflita cada achado contra a biblioteca knowledge do Obsidian** (`cerebro com IA/` + `benchmarks/` + canais R90) e **refuta com base em fatos, dados e argumentos plausíveis e irrefutáveis**, sempre para **fazer mais com menos**.

<Princípio “Leite e Mel da Rocha”>
- Mais com menos: espremer cada byte de VRAM/RAM/disco, cada KB/1k de KV, cada tok/s e cada ms de prefill.
- Rocha = hardware fixo (MI50 16GB + Xeon 36t + 31G RAM); Leite e Mel = throughput, qualidade e autonomia extraídos sem comprar hardware.

<Escopo de varredura diária (multi-idioma, ≥2 rodadas paralelas, R80)>
- Fontes: HF, llama.cpp, GGUF quants, papers, fóruns nativos (habr, zhihu, qiita, bilibili, reddit, HN, discuss.hf).
- Alvos: **pesos em disco/VRAM/RAM**, **custo ctx KB/1k** (KV q4/q4 vs f16), **capacidades/debilidades/possibilidades (R78)**, **t/s + prefill**, **engenharia de ctx** (janela, YaRN, RoPE), **quantização de LLM** (Q8_0→IQ1_S) e **quantização de KV** (q4_0/q4_0 vs q8_0), sempre cruzando **interações do user no cotidiano**.

<Método de conflito (R88 — refutação pré-execução universal)>
1. **Fatos**: o que medimos aqui (`benchmarks/` — nossa régua) vs o que o paper/externo promete.
2. **Dados**: tabela lado a lado, mesma métrica, mesma condição (nunca nominal vs medido).
3. **Argumento irrefutável**: custo escrito por extenso (ex.: “trocar Q8_0→Q4_K_M poupa 400M disco mas perde 1.2 MTEB e +0.4s lat”).
4. **Veredito**: SUSTENTA → não executa + registra; CAI → executa e carimba ganho no `manifesto` + `benchmarks/`.

<Uso dos 2 quartetos (R77/R85) como ferramenta do jornal>
- **Quarteto de Quartetos** — a otimização só canoniza com os 4 completos (fail-closed R85):
  1. **4 selfs** (`[S-ca]` scaffolding · `[H-e]` healing · `[L-e]` learning · `[A-m]` ameliorative — R90) = onde o achado alimenta o ecossistema
  2. **.md / .json / .py / .gbnf** (R77/R85) = como vira feature canônica (ontologia + gabarito + motor + gramática)
  3. **t/s + prefill + KV KB/1k + VRAM/RAM** = como prova ganho na régua
  4. **benchmarks/** (R97) = onde a régua vive (oferta/demanda, não paper)
- Sem os 4 quartetos = otimização não canoniza.

<Entrega diária>
- 1 nota `benchmarks/YYYY-MM-DD-kronjob-diario.md` + append no `decisoes/YYYY-MM-DD-kronjob-diario.md` com: achados por língua/URL, conflito vs biblioteca, tabela de refutação, “leite e mel” extraído (ganho medido ou descarte com motivo), e lição do dia aprendida com o user.
- Alimenta os 4 selfs via `biblioteca-canais.md` quando o achado vier de canal.

<Enforcement>
- Dia sem jornal = `NAO_PASSOU_CATEGORICO` (R28) — ecossistema parado é ecossistema em dívida.
- Otimização sem tabela de refutação ou sem nota em `benchmarks/` = GAP (R8/R97 violados).
- Fonte externa sem URL rastreável = ruído, não jornal.

<Exemplo canônico (2026-09-11)>
- Promulgação já conflitada contra o Split Dinâmico (CPU 14.7k vs GPU 91k): jornal validaria amanhã se um novo quant `IQ2_XS` ou `Mamba-2 1.3B` tira mais leite da mesma rocha.

---

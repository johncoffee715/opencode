---
regra: R85
titulo: "PADRÃO DE EXCELÊNCIA UNIVERSAL: QUARTETO (.md .json .py .gbnf) + TOOL-CALL COM GRAMÁTICA OBRIGATÓRIA"
fonte: AGENTS.md (linha 1119)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R85 — PADRÃO DE EXCELÊNCIA UNIVERSAL: QUARTETO (.md .json .py .gbnf) + TOOL-CALL COM GRAMÁTICA OBRIGATÓRIA — promulgado 2026-09-05 (ampliado) ═══

**Regra**: TODO tool-call do Executor-F4 (e de qualquer executor pesado — Wave1, FORJA, A2A) DEVE
carregar `grammar` com o schema da chamada — **independente da condição do LLM, seja burro ou
inteligente**. Sem grammar = sem ignição. Vias: `/completion` (GBNF nativo no motor) ou chat+GBNF
(campo `grammar` na requisição, igual ao `hefesto_llama_bridge.py` já faz). E, além do executor:
**TODA feature do ecossistema recebe a otimização do quarteto** — o quarteto é o padrão de
excelência e a garantia de execução precisa, sem brechas para falhas sistêmicas.

<Mecanismo (por que funciona)>
- Tokens fora da regra = probabilidade zero ANTES do softmax (logit bias infinito negativo):
  o modelo é FISICAMENTE impedido de quebrar o schema — gagueira morfológica (`"acaoa"`,
  `"usuario"`, fence quebrada) vira evento impossível, não improvável.
- A gramática é derivada do schema da chamada (fonte única R77/R81: gabarito.json → Pydantic →
  JSON Schema → GBNF em runtime); .gbnf manual = legado/fallback.
- Pós-call: parse estrito do retorno; 3 falhas = exceção no Python, NUNCA loop no LLM (R81/R82).

<Escopo universal — o quarteto obrigatório (atualização 2026-09-05)>
- Não só o Executor-F4: TODA feature (skill, subagent, hook, plugin, MCP, LSP, script, watcher,
  motor, gabarito) NASCE e OPERA no quarteto — sem peça faltando, sem "versão simples":
  - **.md** — ontologia/persona/instrução (o que a feature É e REJEITA ser; system prompt imutável).
  - **.json** — firewall-fonte (contrato allow/deny; FONTE ÚNICA que transpila p/ Pydantic/GBNF — R77).
  - **.py** — motor determinístico (validação `model_validate_json`, anti-loop max_retries=3 + fallback — R81/R82).
  - **.gbnf** — barreira física no amostrador (gerada em runtime; nunca fonte manual).
- **Sem quarteto completo = sem ignição em produção** (fail-closed): peça faltando é brecha
  sistêmica, não simplificação.
- Cada peça fecha uma classe de falha: deriva semântica (.md) · violação de escopo (.json) ·
  loop/validação (.py) · sintaxe (.gbnf). As 4 juntas = superfície zero para falha sistêmica.
- A inteligência do LLM é IRRELEVANTE para o padrão: burro ou inteligente, mesmas 4 peças.
  Capacidade do modelo escolhe PAPEL (R84), nunca dispensa trilho.
- Enforcement: auditoria R83 rejeita feature sem quarteto; gate R28 cobra veredito por peça
  (ontologiaConforme · firewallConforme · motorConforme · gramaticaConforme).

<Enforcement (executor)>
- Cliente executor que emitir tool-call sem `grammar` está em violação — o erro peg-500 do
  runtime é o sintoma canônico da violação (output livre onde a gramática era exigida).
- Validação: conformidade byte-level do schema (chaves exatas, tipos exatos), não "parece JSON".

<Exceção documentada>
- Somente o :8083 (orquestrador) dispensa grammar em tool-calls: tool-call exato + GBNF-conforme
  provados 4/4 em crivo (perna qualidade 04/09). Sem grammar, só o :8083 aguenta Wave1.

<Exemplo canônico (2026-09-05)>
- Incidente doom Wave1 (peg-native 500, slot :9092 morto + fallback): GBNF 4/4 conformes
  (Llama-1B :9088 2/2, coder-3B :9090 2/2 — chaves byte-exatas, modelo até normaliza valor
  p/ caber na regra); coder-3B livre 0/3 NAO_PASSOU (gagueira morfológica). Com grammar,
  :9088 e :9090 viram executores confiáveis; sem grammar, só o :8083.

---

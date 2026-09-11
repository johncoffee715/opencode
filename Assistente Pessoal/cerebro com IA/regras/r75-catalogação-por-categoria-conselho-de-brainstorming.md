---
regra: R75
titulo: "CATALOGAÇÃO POR CATEGORIA + CONSELHO DE BRAINSTORMING"
fonte: AGENTS.md (linha 904)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R75 — CATALOGAÇÃO POR CATEGORIA + CONSELHO DE BRAINSTORMING — promulgado 2026-08-30 ═══

**Regra**: em TODO o ecossistema (bindings de agentes/skills, providers, manifesto, scripts, docs, hooks), LLMs são referenciados por **CATEGORIA** (papel no grafo), NUNCA por nome de modelo/GGUF. Troca de LLM = editar APENAS o manifesto/slot — zero quebra de bindings. E o **Conselho de Brainstorming** (jurados + refutadores) é formado por CATEGORIA, não por modelo específico.

## 1. Catalogação por Categoria (modularização anti-quebra)

<Princípio>
- **Binding = categoria**: `provider/categoria-neutra` (ex.: `local-forge/forge`, `local-judge/judge`, `local-orchestrator/orchestrator`). NUNCA `provider/nome-do-gguf`.
- **Roles funcionais fixos** (ROLE_KEYS no sync-llm-stack.py) — o roteamento busca **porta + flag de competência (role)**, nunca nome de instância:

| Role | Perfil exigido | Slot atual (exemplo) |
|---|---|---|
| `orchestrator` | síntese macro, supervisão do grafo, decisão final em escalações | Ornith-35B (CPU) |
| `judge` | validação neutra, pontuação emparelhada, arbitrar refutações | LLMJudge-3B |
| `refuter` | base conceitual profunda, auditar/refutar com dados empíricos e arquitetura | Ternary-8B |
| `proposer` | alta precisão de sintaxe, tool calling nativo, código pragmático | Qwen3.8-4B |
| `ingestor` | processamento rápido, fatiamento/compressão de dados brutos (Filtro Talâmico) | RWKV7-0.4B |
| `reflexo` | refutação de alta velocidade (acerto-e-erro R42) | LFM-1.2B |

- **Inversão de dependência (DIP)**: agentes .md acoplam a roles abstratos (`model: local-forge/proposer`), nunca a instâncias. O SubAgente/Orquestrador NÃO procura "Ternary-8B" — busca qualquer nó de inferência ativo na porta designada com a flag de competência referenciada. Troca de LLM no slot = editar manifesto + `--apply`; bindings intactos (auto-curável).
- **Fonte única**: `manifesto_llm.json` (path canônico) mapeia categoria→slot→arquivo. Troca de modelo = atualizar o manifesto + `sync-llm-stack.py --apply`; bindings de agentes/skills permanecem intactos.
- **Proibido**: referenciar `Ornith-1.5-35B`, `LLMJudge-3B`, `Qwen3.8-4B` etc. em agentes .md, skills, hooks, scripts ou docs operacionais. O nome do modelo vive SÓ no manifesto/inventário (metadata).
- **Exceção**: documentação histórica/benchmarks (relatórios, decision-log) podem citar nomes — são registros, não bindings.

<Mecanismo>
- `sync-llm-stack.py` gera providers com IDs neutros (JUMPER_KEYS) + `model`/`small_model` neutros.
- Agentes .md usam `model: <provider>/<categoria>` — resolvido pelo runtime contra o provider.
- Ao trocar o LLM de um slot: editar manifesto (model_id/arquivo/ctx) → `--apply` → restart do slot. Nenhum .md muda.

## 2. Conselho de Brainstorming (jurados + refutadores por categoria)

<Princípio>
- O **Conselho de Brainstorming** é a entidade de julgamento/refutação do ecossistema: **jurados** (emitem vereditos categóricos R28/R34) + **refutadores** (refutação incansável R40/R41 contra fatos empíricos, dados, argumentos plausíveis e irrefutáveis).
- **Membros por CATEGORIA**: `orquestrador` (Gran-Mestre) e `judge` (LLMJudge) são os jurados/refutadores NÚCLEO. **TODO e qualquer LLM capaz de exercer a função** (mediante respaldo técnico — capacidade de raciocínio/refutação verificada) pode integrar o Conselho, independente de nome/modelo.
- **Respaldo técnico**: um LLM entra no Conselho se demonstrar (a) veredito categórico com evidência (R28), (b) refutação baseada em fatos/dados (R40), (c) nota ≥90 na escala R34 em avaliação adversarial. A entrada é por CATEGORIA, não por identidade.
- **Refutação contra**: fatos empíricos (medições locais), dados (benchmarks, logs, decision-log), argumentos plausíveis e irrefutáveis — nunca opinião solta (R43: scaffolding resolutivo como referência).
- **Quórum**: decisões de alto impacto (canonização, troca de GM, mudança de arquitetura) exigem veredito do Conselho (orquestrador + judge + refutadores disponíveis), registrado no decision-log.

<Fluxo>
1. Task/entrega → jurado (categoria judge) emite veredito categórico por métrica (R28).
2. Refutadores (categoria refutacao/reflexo + qualquer membro capaz) refutam contra dados empíricos (R40/R41) até impressão real (nota ≥90 + elogios concretos + bugs corrigidos).
3. Orquestrador (categoria orquestrador) valida o veredito (R43 — valida o validador) e decide.
4. Tudo registrado no decision-log com evidência.

<Exemplo canônico (2026-08-30)>
- GM trocado 9B→35B: bindings NÃO quebraram porque agentes usam `local-orchestrator/orchestrator` (role), não o nome do GGUF. Taxonomia roles aplicada 2026-08-30: proposer/refuter/ingestor/judge/orchestrator/reflexo.
- Conselho: orquestrador (35B) + judge (3B) + refutador (ternary 8B) + reflexo (LFM 1.2B) — todos por categoria; qualquer um pode ser substituído sem tocar nos .md.


---

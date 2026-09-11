# Regra Universal — Tabela de Auditoria Obrigatória

> Promulgada pelo usuário 2026-09-11. Status: ATIVA (guardrail universal).

## Regra

SEMPRE entregar os dados para auditoria do usuário em **tabela**, de forma
**explícita**, com **todas as informações críticas** para uma auditoria fidedigna.
Sem tabela = sem veredito.

## Colunas obrigatórias (nenhuma pode faltar; lacuna = `n/d` com motivo)

| Coluna | O que é | Fonte |
|---|---|---|
| Candidato | model_id + quant | arquivo GGUF |
| Tam. | GB em disco | `stat` |
| Arch | string `general.architecture` | header GGUF (512B) |
| Origem | repo HF | URL rastreável |
| Ctx | `-c` do teste | flags do slot |
| Device/Endpoint | CPU/GPU + chat/raw | flags + método |
| KV KB/tok | efetivo (híbridos: só layers attn!) | header GGUF |
| Prefill / Decode | t/s medianos | `timings` dos probes |
| T1·T2·T4·T6·T8·T10 | notas 0–1 por métrica | crivo-padrão |
| Placar/6 | soma | — |
| Veredito | multi-perspectiva (regra 2026-09-10) | juiz (GM valida) |
| Destino | em produção / quarentena+path / APAGADO | filesystem |
| Evidência | evento decision-log | JSONL |

## Regras irmãs
- Multi-perspectiva (2026-09-10): pró/contra por métrica antes do veredito.
- R98: tabela comparativa entre candidatos.
- R97: mesmo método p/ todos (fidelidade comparativa).
- Skill `crivo-padrao`: motor que gera os dados da tabela.

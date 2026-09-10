# Regra Universal — Julgamento Multi-Perspectiva de Métricas Empíricas

> Promulgada pelo usuário 2026-09-10 (sessão doom, crivo KAT-Coder).
> Status: ATIVA — vale para TODO veredito de LLM/feature no ecossistema.

## Regra

Todo julgamento baseado em métricas empíricas DEVE apresentar **todas as perspectivas
(prós e contras)** antes do veredito — julgamento preciso e embasado em números, nunca
unilateral.

## Formato obrigatório (tabela por métrica)

| Métrica | Pró | Contra | Peso no julgamento |
|---|---|---|---|
| <métrica empírica> | <o que impressiona> | <o que custa/bloqueia> | <como pesa: bloqueante/neutro/benefício> |

## Exemplo canônico (KAT-Coder-V2.5-Dev IQ3_XXS, 2026-09-10)

- **Schema 1.0 + Code 1.0**: pró = precisão perfeita; contra = se fosse menor (≤3B),
  caberia num nó específico do grafo com o mesmo resultado → custo > benefício.
- **CPU 0.8–1.2 t/s**: contra = gargalo de decode brutal; falha disjuntor R65 (F4 ≥100 t/s)
  por 100× → bloqueante.
- **Poison 0.0**: pró = contornável via R78 (debilidade documentada, rotear ao redor);
  contra = só resgataria se as outras métricas apontassem para um nó → neutro dado o resto.
- **13.85GB**: contra = falha nas métricas de retenção e custo → bloqueante.
- **Veredito**: DESCONTINUADO E APAGADO — precisão perfeita não compensa custo de
  retenção + gargalo de decode.

## Relação com regras existentes

- **R78** (debilidade/capacidades/possibilidades): a regra nova alimenta o R78 —
  cada métrica ganha pró/contra antes de virar campo do manifesto.
- **R83/R84** (crivo/auditoria): o veredito categórico agora exige a tabela
  multi-perspectiva como evidência.
- **R88** (refutação pré-execução): mesma família — números na mesa antes de decidir.
- **R98** (tabela comparativa sempre): a tabela de perspectivas complementa a
  tabela comparativa entre candidatos.

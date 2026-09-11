# Decisão 2026-09-11 — Gran-Mestre v9.2 Quarteto + R100

## Contexto
- Ordem do usuário: pesquisa multi-idioma sobre agentes IA/orquestrador → conflito R88 contra
  Gran-Mestre v9.1 → refutação com biblioteca empírica → Hefesto otimiza via 4 quartetos.
- Intervenção de permissão (`df/free/ls`) flagada pelo usuário como "não deve ocorrer no modo autônomo".

## R88 (refutação pré-execução)
- SUSTENTA 5 GAPs: (1) allowlist diagnóstico read-only; (2) quorum de refutação (Aegean 2512.20184);
  (3) action memory (MOBIMEM 2512.15784); (4) single-writer (IntelliCode 2512.18669);
  (5) auto-quarteto (tríade sem .gbnf).
- CAI: troca de LLM/slot (R93 preserva orquestrador — nada a trocar).

## Decisões
1. Quarteto v9.2 forjado em `skills/gran-mestre/` (conceito.md + gabarito.json + mecanica.py + schema.gbnf).
2. R100 promulgado no AGENTS.md (consulta automática ao Bibliotecário p/ expressões idiomáticas/menções).
3. Bibliotecário: gatilho R100 codificado (conceito + SKILL + mecanica.detect_trigger).

## Evidência
- Smoke quarteto: 4/4 PASSOU_CATEGORICO, converged=true.
- Smoke R100: "leite e mel da rocha" → consultar_bibliotecario + 4 selfs; "4 quartetos" → idem;
  "consulta nota carrossel" → nenhuma (sem trigger).
- py_compile 2/2 OK · gabarito.json JSON Schema válido · AGENTS.md hardlink intacto (inode 4354678).
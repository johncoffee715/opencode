# Aprendizado: relaunch de config stale derruba a stack (2026-09-08)

## Sintoma
Executor-F4 (:9088) a ~25 t/s em vez de ~229 t/s. Auditoria revelou regressão
geral: 8083 em hybrid-ngl36 sem draft + 9086/9088/9090/9092 em CPU.

## Causa-raiz
Relaunch externo (PIDs sequenciais 16635–16671 = launcher em lote) a partir de
fonte STALE — com flags idênticas ao `manifesto_llm.json` desatualizado
(ngl36-hybrid + smalls-CPU). Não foi deriva gradual nem corrupção: foi fidelidade
à fonte errada. O manifesto divergia da produção desde o cenário-B e ninguém
tinha um guard no caminho do relaunch.

## Evidência
- `ss -ltnp` + `/proc/PID/cmdline` por porta (ngl/dev/ctx/batch reais).
- Curva: 9088 25→229 t/s pós-restauração; 8083 hybrid→CPU+draft (accept 1.0).
- 8/8 UP, VRAM 13G pós-restauração 1-a-1.

## Fix (anti-recorrência)
- `opencode/config/opencode/reference/stack-final-flags.json` — fonte canônica nova.
- `opencode/config/opencode/scripts/guarda-deriva-stack.sh` — check default,
  `--fix` humano; validado: SINCRONIZADO 8/8.
- `opencode/config/opencode/scripts/restart-stack.sh` — relançamento total
  idempotente (8 slots + 2 needles), validado por sintaxe.
- Pendente humano: sync do manifesto (kit entregue) + bloco R96 no AGENTS.md.

## Lição
Config viva sem guard é incidente agendado: quem relança do lugar errado com
as melhores intenções quebra tudo. Fonte canônica + verificação no caminho.

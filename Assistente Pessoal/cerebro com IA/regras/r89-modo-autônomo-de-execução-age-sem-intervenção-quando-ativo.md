---
regra: R89
titulo: "MODO AUTÔNOMO DE EXECUÇÃO (AGE SEM INTERVENÇÃO QUANDO ATIVO)"
fonte: AGENTS.md (linha 1237)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R89 — MODO AUTÔNOMO DE EXECUÇÃO (AGE SEM INTERVENÇÃO QUANDO ATIVO) — promulgado 2026-09-05 ═══

**Regra**: existe um **modo autônomo** (skill `modo-autonomo`, estado em
`opencode/state/modo-autonomo.json`, default `false` fail-closed) em que o orquestrador
**age sem intervenção do usuário**: gates auto-aprovados com registro, retry/escalação
automáticos, amadurecimento em loop (R16) até done. **Pausa SÓ por**: conclusão com
evidência · intervenção do usuário (qualquer mensagem) · circuit-breaker OPEN (parqueia
a task, pipeline segue) · operação irreversível (pede humano sempre).

<Ativação e soberania>
- Ativação SOMENTE por ordem explícita ("ativa modo autônomo" + escopo); nada se
  auto-ativa. Desativação: ordem, conclusão geral ou intervenção contrária.
- R88 continua valendo no modo autônomo: refuta antes, mas o veredito vira ação
  imediata sem perguntar (sustenta→não executa+registra; cai→executa).
- Transporte morto 3× = rota cloud-direct (R6), nunca 4ª tentativa; "aprovação por
  cansaço" continua proibida (R40).

<Linhas que o modo NUNCA cruza sozinho>
- `rm -rf` · `trash --empty` · `git reset --hard` (só via R18 + humano) · matar o
  :8083 (substrato próprio = suicídio de sessão) · sudo/senha · edições fora de
  governança/skills sem R88 prévia. Ver `gabarito.json` da skill (allow/deny).

<Observabilidade>
- Toda decisão autônoma: `[Authorize] auto` + `[RunID]` no CONTEXT e decision-log;
  relatórios carimbam `modo: autonomo ON/OFF`.

<Exemplo canônico (2026-09-05)>
- Transporte Hefesto cancelou 3× → modo executaria HF-A/B cloud-direct sem perguntar
  (foi o que ocorreu manualmente: hash-cut + consistência + 73→11 gabaritos + 15 testes).

---

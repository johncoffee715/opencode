---
regra: R99
titulo: "GARI: FAXINEIRO AUTOMÁTICO PÓS-VEREDITO ZERO PENDÊNCIAS"
fonte: AGENTS.md (linha 1513)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R99 — GARI: FAXINEIRO AUTOMÁTICO PÓS-VEREDITO ZERO PENDÊNCIAS — promulgado 2026-09-11 ═══

**Regra**: ao detectar o par exato `user: "posso reiniciar ou ainda existem pendencias"` → `assistant: "Pode reiniciar — zero pendências."`, o **Gari** (`skills/gari/`) dispara automaticamente `Salvar → Armazenar → Limpar` para liberar a session com as pérolas a salvo.

<Workflow (fail-closed, idempotente)>
1. **Salvar:** flush Qdrant WAL + `sync-llm-stack.py --check` sincronizado + snapshot `decisoes/YYYY-MM-DD-sessao-encerrada.md` existente.
2. **Armazenar:** pérolas **quantitativas** (`t/s`, `prefill`, `KV KB/1k`, `VRAM/RAM`, `pesos`, `c/b/ub`) + **qualitativas** (vereditos R28, canais, lições) em `benchmarks/` + `decisoes/` — cada uma com evidência.
3. **Limpar:** só voláteis (`patch_*.py`, `__pycache__`, `/tmp/opencode/*.tmp`) — **nunca** vault/Qdrant/manifesto/start-stack.

<Gatilho>
- Literal, case-insensitive, semântica exata. Outro veredito (`ainda existem pendências`) → **não dispara** (fail-closed).

<Enforcement>
- `gabarito.json` deny: limpar-antes-de-salvar / apagar-canônico / pérola-sem-evidência = `NAO_PASSOU_CATEGORICO`.
- `mecanica.py` valida `trigger` + `verdict` byte-level via GBNF (`schema.gbnf`).

<Exemplo canônico (2026-09-11)>
- Pergunta do user + resposta `Pode reiniciar — zero pendências.` → Gari salvou `vault+Qdrant+manifesto`, armazenou `benchmarks 3 notas + decisoes`, limpou `patch_*.py` — session liberada.

---

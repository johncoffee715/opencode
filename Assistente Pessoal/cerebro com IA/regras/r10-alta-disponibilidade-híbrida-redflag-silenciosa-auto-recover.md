---
regra: R10
titulo: "Alta Disponibilidade Híbrida (redflag silenciosa + auto-recovery) — GLOBAL"
fonte: AGENTS.md (linha 52)
data: 2026-09-11
---

## R10 — Alta Disponibilidade Híbrida (redflag silenciosa + auto-recovery) — GLOBAL
- Sempre que detectar que a **stack local caiu** (llama-server :8081-8084 down), o orquestrador:
  1. Gera uma **redflag INTERNA e SILENCIOSA** (não polui o usuário) como aprendizado de **predição, prevenção e correção** — registrada em `harness/logs/redflags.jsonl`.
  2. Em seguida **torna o stack local online de novo** (relançamento automatizado via `start-all-models.sh`/`start-llama.sh`, com re-probe e verificação), pois o ecossistema é **híbrido local + nuvem** — enquanto locals sobem, a nuvem (omniroute) cobre; quando sobem, volta a prioridade local.
- Mecanismo: `harness/safety/self_heal.py` (redflag + recovery) integrado ao `StallWatchdog`; auditoria de transição up→down (evita spam de redflag por tick).

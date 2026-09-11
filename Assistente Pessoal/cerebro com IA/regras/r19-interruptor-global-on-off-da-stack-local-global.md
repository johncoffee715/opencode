---
regra: R19
titulo: "Interruptor Global On/Off da Stack Local — GLOBAL"
fonte: AGENTS.md (linha 184)
data: 2026-09-11
---

## R19 — Interruptor Global On/Off da Stack Local — GLOBAL

O stack local (4 `llama-server` na MI50 16GB, Vulkan, ports 8081–8084) é descrito por um **interruptor on/off espelhado e irredutível**: ligar e desligar passam SEMPRE pelos scripts canónicos — nunca por `pkill -9 -f llama-server` solto/global. É o par de controle do recurso único global (R2).

<Semântica do interruptor>
- **LIGAR**  → `harness/start-all-models.sh` (religamento) — sobe os 4 modelos de forma **idempotente**: faz health-check (`curl /health`) e **reusa o que já está no ar**, subindo apenas os ausentes; nunca reinicia servidor saudável.
- **DESLIGAR** → `harness/stop-all-models.sh` (desligamento) — derruba os 4 de forma **graceful-first**: SIGTERM → grace period (~10s) → SIGKILL **apenas** para resíduos pós-grace; idempotente (health-check pré-kill, só lida com o que está no ar).

<Regras irredutíveis>
- **Autoridade única**: o orquestrador NUNCA usa `pkill -9 -f llama-server` / `pkill -9 -x llama-server` solto/global para "desligar" a stack — usa SEMPRE `stop-all-models.sh` (graceful, idempotente, auditável, com lock cooperativo `/tmp/stop-all-models.sh.lock`).
- **Exceção documentada**: emergência real em que o `stop-all-models.sh` falhou → o kill manual é permitido, porém registrado como redflag (R10) e reportado ao usuário.
- **Par espelhado**: ambos os scripts têm lock cooperativo idêntico ao do start (`/tmp/start-all-models.sh.lock`/`/tmp/stop-all-models.sh.lock`), reportam estado por porta e VRAM (detecção de card com fallback `card1→card0→card2`), e se espelham em portas lfm 8081 | nanbeige 8082 | ornith 8083 | bonsai 8084.
- **Casos de uso**: "liberar a stack local para reparo rápido/manutenção" = desligar com `stop-all-models.sh` (libera ~16GB VRAM) e religar com `start-all-models.sh` quando o reparo terminar.
- Regra promulgada pelo usuário: "regra global interruptor on/off = start-all-models.sh (religamento) stop-all-models.sh (desligamento)".
- **Execução desanexada obrigatória (2026-08-08)**: `start-all-models.sh`/`start-llama.sh` devem SEMPRE ser lançados **desanexados do terminal** — `setsid nohup <script> > /tmp/<script>.out 2>&1 < /dev/null & disown` — ou por um wrapper/serviço (`systemd --user`/`tmux`/`screen`). Jamais rodar o script "solto" no shell do agente/orquestrador: quando o shell em foreground expira (timeout) ou é encerrado, o sistema mata o **grupo de processos** e derruba os 4 `llama-server` junto (guardam o flock herdado se não forem desanexados). Após o launch, sempre re-probe por porta (`curl /health`) — o log pode reportar "no ar" antes do health-check real estar estável.

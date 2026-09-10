#!/usr/bin/env bash
# post-install-watchdog.sh — WD-PI: watchdog pós-reinstalação do opencode (2026-09-05)
# Restaura as pendências da reinstalação v1.18.29 no SSD slave de IA (sdb):
#   1) binário oficial em bin/opencode (bin/opencode.real não existe mais — portátil removido)
#   2) cérebro XDG: symlink ~/.config/opencode -> config do harness (governança guard-gap-p5)
#   3) watchers vivos: config-watcher (código novo) + stack-guard — relançados desanexados (R19)
#   4) slots ESSENTIAL (:8083/:9084) healthy — revive via start-stack.sh (idempotente)
#   5) 1ª passada = restauração forçada completa (flag .post-install-first-done)
# Fail-open: nunca bloqueia; loga em state/watcher/post-install.log
set -u
ROOT="/mnt/dados/Assistente Pessoal/opencode"
STATE="$ROOT/state/watcher"
LOG="$STATE/post-install.log"
FIRST_FLAG="$STATE/.post-install-first-done"
EXPECTED_VERSION="1.18.29"
INTERVAL="${1:-60}"
mkdir -p "$STATE"

log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

slot_up() { curl -sf -m 3 "http://127.0.0.1:$1/health" >/dev/null 2>&1; }

ensure_watcher() { # $1=nome $2=script
  pgrep -f "$1[.]sh" >/dev/null 2>&1 && return 0
  log "$1 DOWN -> relançando desanexado (R19)"
  setsid nohup "$2" 60 > /dev/null 2>&1 < /dev/null & disown || true
}

check_binary() {
  if [ ! -x "$ROOT/bin/opencode" ]; then
    log "CRITICO bin/opencode ausente — reinstalação comprometida"
    return 1
  fi
  local v
  v=$("$ROOT/bin/opencode" --version 2>/dev/null || echo "?")
  if [[ "$v" != "$EXPECTED_VERSION" ]]; then
    log "WARN versao inesperada: $v (esperado $EXPECTED_VERSION)"
    return 1
  fi
  log "binario OK: $v"
}

check_brain() {
  local target
  target=$(readlink "$HOME/.config/opencode" 2>/dev/null || echo "")
  if [ -L "$HOME/.config/opencode" ] && [ "$target" = "$ROOT/config/opencode" ]; then
    log "cerebro XDG OK (symlink -> harness)"
    return 0
  fi
  log "WARN ~/.config/opencode nao aponta para o harness ($ROOT/config/opencode) — pendencia: exports XDG no ~/.bashrc ou restaurar symlink"
}

check_slots() {
  local down=0 p
  for p in 8083 9084; do
    if slot_up "$p"; then
      log "slot ESSENTIAL :$p UP"
    else
      log "slot ESSENTIAL :$p DOWN"
      down=1
    fi
  done
  if [ "$down" -eq 1 ]; then
    log "revivendo stack (start-stack.sh idempotente, desanexado)"
    setsid nohup bash "$ROOT/scripts/start-stack.sh" >> "$LOG" 2>&1 < /dev/null & disown || true
  fi
}

first_pass() {
  [ -f "$FIRST_FLAG" ] && return 0
  log "===== 1a passada pos-instalacao: restauracao forcada ====="
  check_binary
  check_brain
  # config-watcher antigo roda com codigo velho (check opencode.real) — restart cirurgico
  pkill -f "config-watcher[.]sh" 2>/dev/null
  sleep 1
  ensure_watcher "config-watcher" "$ROOT/scripts/watchers/config-watcher.sh"
  ensure_watcher "stack-guard" "$ROOT/scripts/stack-guard.sh"
  check_slots
  log "1a passada concluida — modo residente (intervalo ${INTERVAL}s)"
  touch "$FIRST_FLAG"
}

first_pass
while true; do
  check_binary
  ensure_watcher "config-watcher" "$ROOT/scripts/watchers/config-watcher.sh"
  ensure_watcher "stack-guard" "$ROOT/scripts/stack-guard.sh"
  check_slots
  sleep "$INTERVAL"
done

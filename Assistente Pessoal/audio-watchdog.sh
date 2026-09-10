#!/bin/bash
# Audio Watchdog - Script de recuperação de áudio
# Resolve problemas de áudio onde apenas Bluetooth está funcionando

set -e

LOG_FILE="/tmp/audio-watchdog.log"
ALSA_CONF="/etc/asound.conf"
USER_ASLA_CONF="$HOME/.asoundrc"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Audio Watchdog Iniciado ==="

# Verificar se há módulos de som carregados
log "Verificando módulos ALSA..."
if lsmod | grep -q snd_hda_intel; then
    log "Módulo snd_hda_intel já carregado"
else
    log "Carregando módulo snd_hda_intel..."
    sudo modprobe snd_hda_intel
fi

# Verificar dispositivos de som
log "Verificando dispositivos de som..."
if aplay -l 2>/dev/null | grep -q "PLBACK"; then
    log "Dispositivo de áudio detectado!"
else
    log "Nenhum dispositivo de áudio detectado. Tentando recuperação..."
    
    # Tentar recarregar módulos ALSA
    log "Recarregando módulos ALSA..."
    sudo modprobe -r snd_hda_intel
    sleep 1
    sudo modprobe snd_hda_intel
    sleep 2
    
    # Verificar novamente
    if aplay -l 2>/dev/null | grep -q "PLBACK"; then
        log "Dispositivo de áudio detectado após reload!"
    else
        log "ALERTA: Dispositivo de áudio ainda não detectado"
        log "Isso pode indicar um problema de hardware/BIOS"
    fi
fi

# Verificar PipeWire
log "Verificando PipeWire..."
if systemctl --user is-active pipewire >/dev/null 2>&1; then
    log "PipeWire está ativo"
else
    log "Reiniciando PipeWire..."
    systemctl --user restart pipewire pipewire-pulse wireplumber
    sleep 2
fi

# Verificar sinks disponíveis
log "Sinks PipeWire disponíveis:"
pactl list short sinks 2>/dev/null || echo "PulseAudio não disponível"

# Listar dispositivos
log "Status do sistema de áudio:"
wpctl status 2>/dev/null | head -30 || echo "WirePlumber não disponível"

# Verificar se há apenas Bluetooth
BLUETOOTH_SINKS=$(pactl list short sinks 2>/dev/null | grep -c bluez || echo "0")
TOTAL_SINKS=$(pactl list short sinks 2>/dev/null | wc -l || echo "0")

log "Bluetooth sinks: $BLUETOOTH_SINKS"
log "Total sinks: $TOTAL_SINKS"

if [ "$TOTAL_SINKS" -eq "$BLUETOOTH_SINKS" ] && [ "$BLUETOOTH_SINKS" -gt "0" ]; then
    log "ALERTA: Apenas áudio Bluetooth disponível!"
    log "O dispositivo de áudio interno pode estar desabilitado no BIOS ou ter problema de hardware"
    
    # Tentar solução com module-udev-detect
    log "Tentando solução alternativa..."
    pactl unload-module module-udev-detect 2>/dev/null || true
    pactl load-module module-udev-detect 2>/dev/null || true
fi

# Criar configuração ALSA padrão se não existir
if [ ! -f "$USER_ASLA_CONF" ]; then
    log "Criando configuração ALSA padrão..."
    cat > "$USER_ASLA_CONF" << 'EOF'
# Configuração ALSA padrão
pcm.!default {
    type plug
    slave.pcm "hw:0,0"
}

ctl.!default {
    type hw_card 0
}
EOF
    log "Configuração ALSA criada em $USER_ASLA_CONF"
fi

log "=== Audio Watchdog Concluído ==="
echo ""
echo "Para verificar manualmente, execute:"
echo "  wpctl status"
echo "  pactl list sinks"
echo "  aplay -l"

# Disk Watchdog - Sistema de Monitoramento de Disco

## Visão Geral
Sistema automático para monitorar espaço em disco, controlar snapshots e alertar sobre uso excessivo.

## Componentes
- `disk-watchdog.py` - Script principal de monitoramento
- `disk-watchdog.json` - Configuração do sistema
- `watchdog.gbnf` - Regras de validação de gramática

## Políticas de Limpeza
- Snapshots: Manter no máximo 2 por diretório
- Banco de dados SQLite: VACUUM automático quando > 1GB
- Cache: Limpeza semanal
- Alertas: Email/logs quando uso > 80%

## Instalação
```bash
pip install watchdog
python disk-watchdog.py
```

## Configuração
Edite `disk-watchdog.json` para personalizar:

```json
{
  "max_snapshots": 2,
  "warning_threshold": 80,
  "critical_threshold": 90,
  "check_interval": 300,
  "paths_to_watch": [
    "/mnt/dados/Assistente Pessoal/opencode/data/opencode/snapshot",
    "/mnt/dados/Assistente Pessoal/opencode/data/opencode"
  ]
}
```
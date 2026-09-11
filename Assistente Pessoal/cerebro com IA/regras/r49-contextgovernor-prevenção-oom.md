---
regra: R49
titulo: "ContextGovernor (Prevenção OOM)"
fonte: AGENTS.md (linha 626)
data: 2026-09-11
---

## R49 — ContextGovernor (Prevenção OOM)

MCP JSON-RPC que calcula janela antropofágica antes de dispatch:
- Extrair metadados do .gguf (camadas, cabeças, dimensões)
- Calcular Custo_KV = camadas × cabeças × dimensões × 2 × bytes × contexto
- Verificar VRAM disponível (16GB - reserva - fragmentação)
- Aprovar/rejeitar dispatch antes de executar
- Retornar janela segura alocada

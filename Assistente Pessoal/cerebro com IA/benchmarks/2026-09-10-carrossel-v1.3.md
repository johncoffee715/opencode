---
data: 2026-09-10
hardware: Obsidian 1.13.7 (Electron) — vault cerebro com IA
artefatos: {fundo: snippets/fundo.css (AnuPpuccin custom-background, AGPLv3), preferencia: snippets/carrossel-fundo.css}
---

# 2026-09-10 — Carrossel Fundo v1.3 (enquadramento)

## Métricas

- **cover** (default do autor): preenche tudo, recorta bordas, sem distorção se imagem ~viewport.
- **contain** (`carrossel-fundo.css`): imagem **inteira, centralizada, sem distorção**, barras em `var(--background-primary)` (letterbox).

## Oferta / demanda

- Demanda: 8 PNGs `maromba grego` verticais em viewport wide → cover distorce/corta.
- Veredito do usuário (bingo): **contain** ficou perfeito; manter `fundo` (tinta) + `carrossel-fundo` (preferência).

## Veredito

**CANÔNICO v1.3** — `manifest 1.3.0` nos 2 paths + pacote `deploys/carrossel-fundo-v1.3.tar.gz` (6.5K, sha 410d386d).

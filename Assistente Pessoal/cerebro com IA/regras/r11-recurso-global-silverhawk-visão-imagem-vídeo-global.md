---
regra: R11
titulo: "Recurso Global SilverHawk (Visão / Imagem / Vídeo) — GLOBAL"
fonte: AGENTS.md (linha 45)
data: 2026-09-11
---

## R11 — Recurso Global SilverHawk (Visão / Imagem / Vídeo) — GLOBAL
- A **skill SilverHawk** integra ao harness capacidades de **áudio, vídeo e imagens** (Visão, Imagem e Vídeo) baseadas no **LFM2.5-VL-1.6B** (Liquid AI) — mesmo modelo do `filter_fast` do harness.
- É um recurso **totalmente global** (R2): invocável de qualquer instância/local via `~/.config/opencode/skills/silverhawk/` (SKILL.md com frontmatter: visão/OCR/vídeo/multimodal/captioning/grounding).
- **Binding de recurso→submodelo** (R9): `silverhawk → local-lfm` (LFM 2.5-VL-1.6B em :8081), com fallback omniroute quando o local cair (R10, hot-swap non-stop).
- **Oferta→Demanda** (R5): registry v2 cataloga `silverhawk` com tags `visao, imagem, video, ocr, multimodal, captioning, grounding, raciocinio-visual` — surfando no top-1 para tasks de visão/OCR/vídeo.
- Regra promulgada pelo usuário: "skill silverhawk integra ao harness capacidades de audio video e imagens Visão, Imagem e Vídeo".

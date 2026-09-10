# Prática Padrão de Ingestão de Transcrições (vigor 2026-09-09)

> Padrão operacional do RAG cerebral (R86/R90): todo vídeo ATIVO com digestão pendente passa por este
> pipeline. Fonte: guia do usuário helenizado + piloto GlRHi8SmmQ0 (evidência abaixo). Cloud-direct
> enquanto o transporte local estiver morto; com a stack no ar, delegar ao Bibliotecário/Hefesto.

## Pipeline padrão (5 passos)
1. **Baixar legenda**: `yt-dlp --write-auto-sub --sub-lang "es,en,pt" --sub-format vtt --skip-download -o "/tmp/opencode/subs/%(id)s.%(ext)s" <URL>` (PT pode dar 429 — graceful, usa o idioma original; `youtube-transcript-api` é opcional).
2. **Limpar**: drop WEBVTT/timestamps/tags, unescape HTML, dedupe linhas consecutivas, agrupar em parágrafos (~8 cues). Só leitura, saída em stdout.
3. **Gravar no vault**: `cerebro com IA/textos, pdf e esquemas/<VIDEOID>-transcricao-<LANG>.md` com frontmatter (video_id, título, URL, canal, etiquetas 4-selfs, origem, data). O watcher do Bibliotecário reindexa no Qdrant.
4. **Chunking p/ vetorial**: 500–1000 tokens, overlap 10–15%; metadados por chunk (video_id, título, URL, etiqueta).
5. **Log**: decision-log + atualizar fila no staging; marcar vídeo como INGERIDO na §7.

## Checklist por ingestão
- [ ] Legenda baixada (idioma registrado; 429 = graceful, nunca bloqueia)
- [ ] Texto limpo (sem timestamps, sem tags, sem duplicatas)
- [ ] Frontmatter completo no vault (rastreabilidade p/ citação)
- [ ] Fila atualizada (pendente → ingerido)

## Evidência do piloto (2026-09-09)
GlRHi8SmmQ0: ES+EN ok (~100KB cada), PT 429; 337 cues → 43 parágrafos →
`textos, pdf e esquemas/GlRHi8SmmQ0-transcricao-ES.md`.

## Fila
- Feito: GlRHi8SmmQ0 (PÉROLA, parte 1).
- Pendente: 0LtdXQ_deUA (classificar pós-transcrição) · demais vídeos §7 sob demanda · série do livro 182p (Nichonauta) conforme sair.

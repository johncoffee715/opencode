---
regra: R95
titulo: "AUTO-CADASTRO DE CANAIS DE VÍDEO NA BIBLIOTECA (GUARDRAIL UNIVERSAL)"
fonte: AGENTS.md (linha 1384)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R95 — AUTO-CADASTRO DE CANAIS DE VÍDEO NA BIBLIOTECA (GUARDRAIL UNIVERSAL) — promulgado 2026-09-10 ═══

**Regra**: todo vídeo cujo canal AINDA NÃO estiver na biblioteca do Obsidian
(`skills/bibliotecario/biblioteca-canais.md`) DEVE ser cadastrado automaticamente —
sem pedir, sem adiar para "depois".

<Procedimento obrigatório (a cada vídeo usado como apoio/scout)>
1. Extrair canal: `yt-dlp --print channel --print uploader_url <url>` (evidência rastreável).
2. Conferir presença na biblioteca (grep pelo nome/handle).
3. Ausente → append imediato na seção por missão com: handle · foco útil (do que o vídeo entregou) ·
   etiqueta(s) de self ([S-ca]/[H-e]/[L-e]/[A-m]) · status (`NOVO` + estado do transcrito) + log.
4. Presente → sem duplicata; atualiza o status se o vídeo agregou (ex.: transcrito feito).

<Limites>
- Vale para vídeos trazidos pelo usuário OU levantados em survey (R80/R90) — a biblioteca só cresce.
- Descarte segue R90 (motivo escrito); nunca re-survey sem mudança de grade.
- Registro julgado depois: canal novo entra como NOVO e amadurece por uso, não por palpite.

<Enforcement>
- Pesquisa de apoio sem passo de cadastro = GAP (R8/R90 violados por omissão).
- Prova canônica (2026-09-10): vídeo `u325wOUMgiQ` teve o canal cadastrado no mesmo turno (R90+R95).

---

---
regra: R80
titulo: "PESQUISA COMUNITÁRIA MULTI-IDIOMA OBRIGATÓRIA"
fonte: AGENTS.md (linha 1070)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R80 — PESQUISA COMUNITÁRIA MULTI-IDIOMA OBRIGATÓRIA — promulgado 2026-08-31 ═══

**Regra**: toda pesquisa na internet (busca de LLM candidato, substituição de modelo, benchmarks
comunitários, apoio de decisão R50) DEVE: (1) cobrir sites/fóruns em TODAS as línguas possíveis
(EN, PT, ES, ZH, JA, KO, RU, DE, FR, IT…) via motores nativos (habr, zhihu, qiita, bilibili, clien,
reddit, HN, discuss.huggingface, yandex…); (2) usar TODOS os subagentes disponíveis correspondentes à
task em paralelo (waves); (3) priorizar opções MoE não-oficiais da comunidade com evidências de
desempenho/eficácia (downloads, likes, benchmarks, posts, vídeos — yt-dlp) quando o caso for
substituir/melhorar LLM; (4) evidência rastreável (URL) para cada afirmação; (5) sintetizar e registrar
no decision-log + reference. Fonte externa é APOIO — empírico local e veredito do pipeline prevalecem (R45).

---

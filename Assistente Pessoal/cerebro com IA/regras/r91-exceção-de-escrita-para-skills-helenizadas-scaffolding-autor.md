---
regra: R91
titulo: "EXCEÇÃO DE ESCRITA PARA SKILLS HELENIZADAS (SCAFFOLDING AUTORIZADO POR CATEGORIA)"
fonte: AGENTS.md (linha 1269)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R91 — EXCEÇÃO DE ESCRITA PARA SKILLS HELENIZADAS (SCAFFOLDING AUTORIZADO POR CATEGORIA) — promulgado 2026-09-10 ═══

**Regra**: o Gran-Mestre PODE escrever/editar diretamente em `skills/<nome>/**` quando a escrita for
**helenização/scaffolding de skill** (R14/R74/R77) — sem precisar de exceção linha-a-linha por skill.
O deny-by-default do `agent/gran-mestre.md` permanece para TODO o resto (código produtivo, config de
runtime, agentes, hooks, plugins — esses continuam negados e delegados).

<Alcance>
- **ALLOW**: `**/skills/**` — criar/atualizar SKILL.md, tríplice/quarteto R77 (conceito/gabarito/
  mecânica/schema), references/, templates/, LICENSE, e registrar a skill no `opencode.jsonc`
  (bloco `skills`, objeto `{}` — nunca array).
- **CONTINUA DENY**: `agent/*.md` (exceto as exceções já promulgadas), `hooks/`, `plugins/`,
  `opencode.jsonc` fora do bloco `skills`, código produtivo de projetos, e qualquer path fora de
  `~/.config/opencode/skills/**`.
- **Registro de skill nova no opencode.jsonc**: permitido SOMENTE o bloco `skills` (append de
  `"nome": {}`), com validação JSON pós-edit (strip comments preservando URLs) e verificação de
  que hooks/permission/agents ficaram intactos (diff de campos críticos).

<Prova de necessidade (por que existe)>
- 2026-09-09/10: helenizações bibliotecario (biblioteca R90) e unlazy exigiram exceção cirúrgica
  linha-a-linha aplicada pelo usuário (soberania 3x) — atrito desnecessário para trabalho de
  scaffolding legítimo. Esta regra elimina o atrito SEM abrir o código produtivo.

<Guardrails>
- Toda escrita sob R91 carrega provenance no artefato (frontmatter origin/source_commit/license).
- Skill nova = quarteto R85 completo ou não ignita (fail-closed).
- Auditoria R83 pós-forja (testes reais, smoke) antes de declarar done.
- Abuso (usar R91 para tocar código produtivo) = violação registrada + revogação da regra.

<Exemplo canônico (2026-09-10)>
- unlazy helenizado com exceção individual; R91 generaliza o padrão: próxima skill (ex.: do
  scout R87) nasce sem gate humano de permissão — só os gates de qualidade (R28/R83).

---

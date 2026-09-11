---
regra: R26
titulo: "Memória Obsidian para TODOS os modelos (trigger curto, janela preservada) — GLOBAL"
fonte: AGENTS.md (linha 339)
data: 2026-09-11
---

## R26 — Memória Obsidian para TODOS os modelos (trigger curto, janela preservada) — GLOBAL

Promulgada 2026-08-11 (autofagia global / pedido do usuário). O cérebro Obsidian
(`/mnt/dados/Assistente Pessoal/cerebro com IA`) NÃO é privilégio do Gran-Mestre — qualquer modelo,
em qualquer instância, pode consultar memória de longo prazo.

<Regra irredutível>
- **Acesso universal**: TODOS os modelos/agentes têm acesso ao vault via skill
  `memory-recall` (trigger: prefixo de turno `memória: <tema>` ou perguntas de
  retomada "o que já fizemos?", "lembra de...", "contexto anterior").
- **Janela preservada**: o bloco de memória injetado é SEMPRE curto (≤ 200
  tokens) — referência de trigger, nunca dump de arquivos inteiros do vault.
- **Hook automático**: `session.start` roda `harness/hooks/memory_inject.py`
  (registrado em opencode.json) — injeta índice do cérebro + estado do pipeline
  + aprendizados recentes no início de cada sessão, com falha silenciosa.
- **Escrita disciplinada**: escrita/atualização do vault segue o fluxo de
  ingestão Obsidian (memory-keeper), nunca escrita ad-hoc desestruturada.
- **Fontes em ordem**: `wiki/index.md` → `pipeline/contexto-atual` →
  `aprendizados/` → `decisoes/` → profundidade sob demanda (Read com offset).
- **Nunca inventar**: consulta vazia responde `[MEMORIA] sem registros para
  "<tema>"` — jamais fabricar memória inexistente.

<Artefatos>
- Skill: `~/.opencode/skills/memory-recall/SKILL.md` (protocolo de consulta).
- Hook: `harness/hooks/memory_inject.py` + registro `hooks.session.start` no
  opencode.json.
- Camada vetorial complementar: skill `memory-local` (mem0 helenizada).

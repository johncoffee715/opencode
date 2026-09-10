---
titulo: "Helenização unlazy — disciplina de conclusão com gates executáveis"
tags: [helenizacao, unlazy, gates, R14, R74, R77, R28, fable-judge]
data: 2026-09-10
origem: https://github.com/Leonxlnx/unlazy (MIT, commit 1667149)
status: FORJADO-E-COMMITADO
---

# Helenização unlazy (Hefesto modo MIX, 2026-09-10)

## O que foi absorvido (autofagia)
- **Proteína lógica**: ledger de gates escritos ANTES da execução; `CHECK:`/`EXPECT:` como código com aprovação vinculada (ledger+gate+comando+CWD+shell+timeout+PATH); digest de definição versionado (evidência antiga = stale-unmet); `--reverify` como re-verificação de pai (`--status` NÃO é re-verificação); `ABANDON:` como handoff terminal (nunca sucesso); waves de dispatch seladas antes de esperar; leases `OWNS:` disjoint com claim/release atômicos; 4 passadas por folha (implementar→reler→caçar defeitos→polir).
- **Expurgado**: stop-hook Claude Code (host-specific), adapters Codex/Claude no dispatch.md (mantidos como referência histórica, não operacionais), install-hooks.mjs (fora da skill de propósito).

## O que foi forjado (helenização)
- `skills/unlazy/` global: SKILL.md pt-BR + tríplice R77 (conceito.md, gabarito.json, mecanica.md) + motor zero-dep preservado (scripts/, 188 testes verdes) + references/ + templates/ + LICENSE MIT.
- Registrado no opencode.jsonc (17 skills), sync --check sem divergências, hooks/permission preservados.
- Permission: `**/skills/unlazy/**: allow` (soberania usuário 2026-09-09, após exceção bibliotecario).
- Commit atômico: `203f36299`.

## Integração harness
- **Gate R28**: o ledger unlazy É o acceptance_criteria executável do Task Packet.
- **fable-judge**: `--reverify` = re-execução adversarial determinística e barata.
- **Dispatch**: waves registradas via dispatch-check; launch nativo = tool `task` (task_id como `--handle`).
- **Leases**: complementam zero-trust/downscope (coordenação, não sandbox).

## Lição (R44)
- O paradoxo do freio próprio se resolve por exceção cirúrgica por categoria de skill (bibliotecario, unlazy) — deny-by-default intacto. **RESOLVIDO EM DEFINITIVO (2026-09-10): R91 promulgada** — escrita GM em `skills/**` autorizada por categoria; exceções individuais consolidadas; próxima skill nasce sem gate de permissão, só gates de qualidade (R28/R83).
- unlazy fecha o GAP entre "gate de entrega" (política) e "gate executável" (mecânica): a partir de agora, pipelines SIMPLE+ podem carregar GATES.md como contrato de conclusão.

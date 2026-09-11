---
regra: R44
titulo: "Refinamento Contínuo do Harness + Grafo (Scaffolding Resolutivo Global)"
fonte: AGENTS.md (linha 678)
data: 2026-09-11
---

## R44 — Refinamento Contínuo do Harness + Grafo (Scaffolding Resolutivo Global)

**Regra**: o objetivo da operação/monitoramento não é só esperar delegações — é **refinar o
harness e o grafo continuamente** (R43 + R14 + R41). O orquestrador **raciocina, audita,
encontra GAPs e constrói scaffolding resolutivo** — e todo scaffolding produzido DEVE ser
**GLOBAL em TODAS as sessões** (R2: Recurso Único Global).

### Essência executável
- **Monitorar ≠ esperar**: monitoramento serve para descobrir GAPs (rotas mortas, hooks não
  registrados, catálogo impreciso, config divergente) e refinar.
- **Scaffolding global**: skills, agentes, hooks, comandos, regras, scripts, watchers →
  instalados em `~/.config/opencode/`/`~/.opencode/`, registrados no registry, invocáveis de
  qualquer instância. NUNCA em /tmp ou sessão isolada.
- **Fluxo obrigatório**: auditar (registry/config/hooks/ctx-catalog/health) → identificar GAP →
  construir scaffolding resolutivo → registrar globalmente → validar empiricamente →
  arquivar na memória cerebral (R26).
- **Ciclo de vida**: o refino é contínuo — cada ciclo de auditoria deve encontrar ≥1 GAP ou
  provar que o harness está íntegro (0 GAPs = estado ideal a manter, com evidência).

### Exemplos de aplicação
- GAP: hook documentado mas não registrado no config → registrar + validar (ex.: R33).
- GAP: watcher em /tmp (volátil) → mover para ~/.opencode/scripts/ + registrar.
- GAP: registry com classificação imprecisa → corrigir catálogo (R8/R-catalog).

Regra em vigor desde 2026-08-16 (pedido do usuário).

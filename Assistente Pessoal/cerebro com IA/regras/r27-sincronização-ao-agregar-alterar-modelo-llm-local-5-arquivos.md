---
regra: R27
titulo: "Sincronização ao agregar/alterar modelo LLM local (5 arquivos + re-probe) — GLOBAL"
fonte: AGENTS.md (linha 367)
data: 2026-09-11
---

## R27 — Sincronização ao agregar/alterar modelo LLM local (5 arquivos + re-probe) — GLOBAL

Promulgada 2026-08-11 (autofagia global / pedido do usuário). Adicionar um novo
modelo local (ou mudar porta/ctx/janela) exige atualização coordenada em TODOS
os pontos de verdade — um só desatualizado quebra o harness silenciosamente.

<Regra irredutível>
- Ao agregar/alterar modelo local, atualizar OBRIGATORIAMENTE:
  1. `harness/ctx-catalog.json` — catálogo de janelas/portas (fonte de R23/R24).
  2. `~/.config/opencode/opencode.json` — provider + model + baseURL + limit ctx.
  3. `~/.config/opencode/oh-my-openagent.json` — remapeamentos de agentes/roles.
  4. Scripts de subida: `start-all-models.sh` / `stop-all-models.sh` (R19) —
     porta, modelo, args (--ctx-size, --parallel, --backend vulkan).
  5. `harness/llama_budget.py` — UNIFORM_CTX/HEADROOM (R24) + AGENTS.md §13.
- **Re-probe obrigatório**: após qualquer mudança, validar health 5/5 nas portas
  e conferir VRAM (rocm-smi, folga ≥ 200 MB) — nada de "só editei o config".
- **Janela uniforme W=27136** (R24): delegação que exige mais → omniroute (R23),
  nunca forçar local-curto.
- **Verificação de referências**: buscar TODAS as menções ao modelo antigo
  (grep `:808X` e nome do modelo) antes de declarar o sync completo.

<Verificação do fix 2026-08-11>
- opencode.json: 5 providers locais (`local-orchestrator` :8083, `local-bonsai` :8084,
  `local-qwen` :8085, `local-llama` :8086, `local-deepseek` :8087) + omniroute;
  remoção de providers mortos (nanbeige/lfm); ctx 27136 uniforme.
- oh-my-openagent.json: agentes apontando para `local-bonsai/bonsai-27b` +
  fallback omniroute. ctx-catalog.json: portas 8083-8087 coerentes.
- Stack local: 5/5 UP (llama-server :8083-8087, backend vulkan, janela 27136).

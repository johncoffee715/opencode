---
regra: R21
titulo: "VRAM Só Com Conteúdo Ativamente Utilizado — GLOBAL"
fonte: AGENTS.md (linha 220)
data: 2026-09-11
---

## R21 — VRAM Só Com Conteúdo Ativamente Utilizado — GLOBAL

A VRAM da GPU (**MI50 16GB**) **nunca** deve armazenar informação (pesos, KV cache, buffers) que não esteja **sendo utilizada ativamente**. É regra de **economia de recurso único** (R2) e combina com a R20 (janela-curta → nuvem).

<Regra irredutível>
- **Só residente = ativo**: um modelo/cache só ocupa VRAM enquanto um workflow/task estiver de fato o invocando. Nada carregado "por segurança" ou "por conveniência" se não houver uso real no momento.
- **Trabalho parado libera VRAM**: se uma task não estiver usando os pesos, o orquestrador **descarrega ou hot-swap** (R9) → libera espaço para quem está ativo — nunca mantém 4 modelos residindo quando 1–2 resolvem o que está rodando.
- **Contexto/armazenamento não utilizado** (inferência ociosa, agregações sem task pendente) → **não residente**: mantém-se só a infraestrutura mínima ativa.

<Procedimento de gestão>
1. **Antes de carregar**: pergunta "este uso é ativo agora?" — se não, adiar o load; carregar sob demanda.
2. **Quando uso acaba**: liberar o slot/VRAM do modelo não mais ativo (hot-swap drain/um off → subs-layout).
3. **Contraste com os limites**: com 4 modelos residentes (95% VRAM) e 1 task ativa, descarregar o não-ativo (R9 swapper / `stop-all`/`start-all` por modelo) antes de forçar outros.
4. **Insuficiência de janela de contexto** (R20) → roda para nuvem em vez de esticar VRAM local além do ativo.
5. **Monitor**: VRAM usada deve rastrear o conjunto *ativo*; folga e peso são sintoma de contradição da regra.

<Relação>
- **R2** — VRAM é recurso único global: proteção por uso real.
- **R9** — hot-swap/drain: mecanismo para manter só ativo residente.
- **R10/R20** — queda de janela/down → nuvem em vez de ocupar VRAM sem uso.
- Regra promulgada pelo usuário: "regra global VRAM nunca deve armazenar informação que não esteja sendo utilizada ativamente".

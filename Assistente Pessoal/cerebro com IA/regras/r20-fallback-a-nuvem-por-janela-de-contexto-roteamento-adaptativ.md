---
regra: R20
titulo: "Fallback a Nuvem por Janela de Contexto (roteamento adaptativo) — GLOBAL"
fonte: AGENTS.md (linha 200)
data: 2026-09-11
---

## R20 — Fallback a Nuvem por Janela de Contexto (roteamento adaptativo) — GLOBAL

Quando uma task esbarra em **insuficiência de janela de contexto** dos modelos **locais** (llama-server :8081–8084), o orquestrador **roteia para a nuvem** (omniroute/cloud-MoE) **até concluir a task**, e **ao final retorna a prioridade à stack local**. É o complemento de janela-vs-local do R10 (híbrido) e do R13 (mais competente).

<Regra irredutível>
- **Gatilho**: qualquer mensagem/evidência de "janela de contexto menor que o necessário" — contexto estourado, truncamento, loss de cobertura, ou task cuja janela exigida supera a do modelo local selecionado → **NÃO forçar o local** (falha recorrente documentada em self-healing #3 e decision-log).

<Procedimento (disparo → conclusão → retorno)>
1. **Detecte a janela curta** (erro/timeout/hallucination por cobertura, ou análise explícita do orquestrador sobre a exigência vs a janela do local).
2. **Roteie para fallback nuvem** (omniroute/MoE — janela grande) e **registre redflag** (R10) como aprendizado — interno e silencioso.
3. **Conclua a task na nuvem** (a janela grande cobre a análise completa; local não é derrubado, apenas despriorizado para aquela task — hot-swap R9).
4. **Ao concluir**, **retorna a prioridade à stack local** (religando `start-all-models.sh` se os locais tiverem caído, ou apenas re-equilibrando o roteamento para local — re-probe R10).
5. **Não trocar o local pelo local**: se o local caiu por janela, subir **não resolve** — a nuvem resolve; religar o local é para o *próximo* ciclo de charges que couberem.

<Relação com outras regras>
- **R10** — redflag + auto-recovery híbrido: R20 é o gatilho de janela; R10 é o gatilho de queda (down) — ambos caem na nuvem e religam local no fim.
- **R13** — mais competente: nuvem tem janela grande; quando a janela é o fator competente, nuvem > local. Manter Héstia/fable-judge validando (R15) mesmo em rota nuvem.
- **R17/R18**: o circuito-breaker permanece — a nuvem também pode travar; limites aplicam-se à rota cloud igualmente.
- Regra promulgada pelo usuário: "regra global após mensagem de janela de contexto menor do que o necessário rotear para fallback nuvem até concluir a task e no final ao concluir retornar a stack local".

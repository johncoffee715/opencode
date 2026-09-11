---
regra: R41
titulo: "Refutação Aplicada a TODOS os LLMs Locais + Scaffolding + Self-Learning"
fonte: AGENTS.md (linha 521)
data: 2026-09-11
---

## R41 — Refutação Aplicada a TODOS os LLMs Locais + Scaffolding + Self-Learning

O guardrail R40 (refutação incansável até impressão real) aplica-se a **TODOS os LLMs disponíveis no path canônico** `/mnt/dados/Assistente Pessoal/modelos LLM/` (R32):

| Modelo | Porta | Janela | Papel |
|--------|-------|--------|-------|
| ornith-1.0-9B | :8083 | 65.536 | Gran-Mestre (primário, R39) |
| Bonsai-27B | :9083 | 16.384 | refutador pesado / brainstorming |
| Qwen3.5-0.8B | :9084 | 262.144 | Nível 1 (exploração/plano) |
| qwen2.5-coder-1.5b | :9087 | 131.072 | Nível 2 (filtro/refatorador) |
| DeepSeek-R1-Distill-0.5B | :9085 | 32.768 | refutação rápida / sanidade |
| LFM2.5-230M | :9086 | 128.000 | verificação de sanidade leve |

### Mecânica
1. **Rodadas adversariais entre todos**: cada LLM refuta/é refutado pelos demais, em qualquer par (A→B, C→D...), sem limite de rodadas, até impressão real (nota ≥90 R34 + elogios concretos + bugs corrigidos).
2. **Scaffolding a partir de cada ciclo**: skills, agents, regras, padrões e configurações novas são criados/atualizados no harness a partir do aprendido (R14 — autofagia + helenização). Nada de refutação "no vácuo": todo veredito vira artefato.
3. **Self-learning contínuo**: cada veredito alimenta `decision-log` + scores adaptativos (`record_decision` → `_scores_from_log()` → boost em `select_for_task()`) + fine-tuning do oráculo local quando aplicável.
4. **Inventário vivo**: a lista acima é lida do path real (R32) — se um modelo for adicionado/removido, entra/sai automaticamente do ciclo de refutação (R35).

Regra em vigor desde 2026-08-16 (pedido do usuário).

---
regra: R42
titulo: "Loop de Alta Velocidade (Acerto-e-Erro) para LLMs Rápidos"
fonte: AGENTS.md (linha 542)
data: 2026-09-11
---

## R42 — Loop de Alta Velocidade (Acerto-e-Erro) para LLMs Rápidos

LLMs com alta taxa de tokens/s **PODEM loopar** (ciclos de acerto-e-erro) — desde que a velocidade de entrega se auto-justifique com entrega **qualitativa E quantitativa**.

### Mecânica
1. **Loop permitido**: mesmo que o modelo rápido falhe ou alucine, podem ser feitas "infinitas requisições de refatoração de acerto e erro" até produzir **frutos concretos de scaffolding** (skills, agentes, regras, scripts, padrões — R14).
2. **Avaliador que acompanha o ritmo**: cada iteração é avaliada SEMPRE por outro modelo capaz de acompanhar a velocidade de requisições do loop (ex.: refutador qwen-coder/or NITH avaliando ciclos do lfm/deepseek/qwen).
3. **Vantagem dos pequenos**: a verdadeira vantagem de LLMs menores e menos inteligentes é loopar em altíssima velocidade, quase imperceptível ao usuário final — o custo do erro é baixo, o throughput é alto.
4. **Velocidade justifica a qualidade**: o loop só é aceito se a velocidade de entrega se auto-justifica com a entrega qualitativa E quantitativa resultante (R28: veredito categórico por evidência).

### Throughput real (medição 2026-08-16, 300 tokens, mesma carga)
| Modelo | Porta | predict | prompt |
|--------|-------|---------|--------|
| lfm-230m | :9086 | 399 tok/s | 141 tok/s |
| deepseek-0.5b | :9085 | 240 tok/s | 183 tok/s |
| qwen-0.8b | :9084 | 162 tok/s | 127 tok/s |

→ ciclo de refutação ~800 tokens em **2-5s** nos rápidos (vs. dezenas de segundos em orchestrator-9b/bonsai-27b).

Regra em vigor desde 2026-08-16 (pedido do usuário).

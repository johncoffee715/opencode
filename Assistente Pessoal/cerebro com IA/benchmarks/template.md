# Template — Nota de Benchmark

Copie este arquivo para `YYYY-MM-DD-<slug>.md` e preencha.

```yaml
---
data: 2026-09-11
hardware: MI50 16GB + Xeon E5-2699v3 (36 threads)
modelo: Qwen3-Embedding-0.6B-GGUF
quant: Q8_0 610M
slot: :9094
params: {c: 2048, b: 256, ub: 256, ngl: 0, pooling: last, cache_type_k: q4_0, cache_type_v: q4_0}
---
```

## Métricas
- `t/s` por batch: 1→, 2→, 4→, 8→, 16→, 32→
- Lat p50/p95 (b1, b8, b32):
- `KV KB/tok` → `KB/1k`:
- VRAM Δ / RAM slot / dim:
- Norma / média / primeiros3 (sanidade vetorial):

## Oferta / demanda
Por que este motor neste papel? Qual trade (VRAM vs lat vs qualidade vs licença)?

## Veredito
CANÔNICO / BURST / HISTÓRICO / REPROVADO + condição de desbloqueio se reprovar.

## Logs
Comandos + outputs (curl /props, bench, rocm-smi).

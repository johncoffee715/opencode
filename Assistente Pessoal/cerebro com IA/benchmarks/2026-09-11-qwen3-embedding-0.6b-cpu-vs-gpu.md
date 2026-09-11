---
data: 2026-09-11
hardware: MI50 16GB + Xeon E5-2699v3 (36 threads, DDR4)
modelo: Qwen3-Embedding-0.6B-GGUF Q8_0 610M (28 layers, 1024 hidden, 1024-d MRL)
quant: Q8_0
slots: {cpu: ":9094 -ngl 0", gpu: ":9097 -ngl 99 Vulkan0"}
params: {c: 2048, b: 256, ub: 256, pooling: last, cache_type_k: q4_0, cache_type_v: q4_0}
colecao: bibliotecario_1024 (631 pts, Cosine, 1024-d, 631/631 reais)
---

# 2026-09-11 — Qwen3-Embedding-0.6B Q8_0 — CPU `:9094` vs GPU `:9097`

> Primeira régua do setor. **Não é o que o paper promete, é o que medimos aqui.**

## Métricas

| Batch | CPU `:9094` (s) | CPU tok/s | GPU `:9097` (s) | GPU tok/s | Speedup |
|---|---|---|---|---|---|
| 1 (512 tok) | 0.52 | 984 | 0.12 | 4 184 | 4.2× |
| 2 (1024) | 0.08 | 12 789 | 0.02 | 48 006 | 3.7× |
| 4 (2048) | 0.14 | 14 509 | 0.03 | 62 680 | 4.3× |
| 8 (4096) | 0.29 | 14 185 | 0.06 | 74 116 | 5.2× |
| 16 (8192) | 0.56 | 14 545 | 0.10 | 81 919 | 5.6× |
| 32 (16384) | 1.11 | 14 702 | 0.18 | **90 982** | **6.1×** |

- Lat p50 (b1): CPU 0.52s → GPU 0.12s (-77%).
- Batch 16×512 (8192 tok) em GPU: 0.10s.
- Sanidade vetorial (CPU, `curl /v1/embeddings`): DIM 1024, norma 1.0, média ~0.000279 — saudável.

## Custo

- **KV q4/q4**: ~14 KB/tok → **14 336 KB/1k** → ~28 MB @2048 (28 layers × 512 kv_dim × 2 × 0.5B).
- **VRAM**: 14062M → 15109M com GPU = **+1047M** para o slot GPU (pesos 610M + KV + overhead Vulkan).
- **RAM**: CPU 809M vs GPU 326M (pesos em VRAM).
- **Disco**: 610M GGUF.

## Oferta / demanda

- **Oferta**: MI50 com 1.3G livre (88% usado) + Xeon 36 threads. GPU tem folga para 1 slot embedder.
- **Demanda (Bibliotecário)**: PT multilíngue 32k, Apache-2.0, retrieval fraseado, query esporádica (latência > throughput).
- **Trade**: GPU dá 6× tok/s mas custa 1G VRAM. Para query única, ganho é 0.4s. Para backfill 631 notas, GPU economizaria ~2min (3m33s → ~35s).

## Veredito

- **CANÔNICO CPU `:9094`** — primário estável (sem VRAM, lat 0.52s aceitável).
- **CANÔNICO GPU `:9097` BURST** — para backfills/lotes; desliga quando VRAM apertar (`kill :9097` libera 1G).
- Pré-requisito R96 cumprido: Qwen3-0.6B em `filtragem/` → slot → 631 reais (batch 8 com divisão de lote, 43s finais).

## Logs

```bash
hf download Qwen/Qwen3-Embedding-0.6B-GGUF --include "Qwen3-Embedding-0.6B-Q8_0.gguf" --local-dir ".../filtragem" # 610M
LD_LIBRARY_PATH=.../bin setsid nohup llama-server.real -m ...Q8_0.gguf --port 9094 -c 2048 -np 1 -b 512 -ub 256 -ngl 0 --embedding --pooling last
LD_LIBRARY_PATH=.../bin setsid nohup llama-server.real -m ...Q8_0.gguf --port 9097 -c 2048 -np 1 -b 512 -ub 256 -ngl 99 -dev Vulkan0 --embedding --pooling last
python3 tooling/backfill.py --collection bibliotecario_1024 --dim 1024 --embed-url http://127.0.0.1:9094/v1/embeddings --batch 16 # 631/631
rocm-smi --showmeminfo vram # 14062M → 15109M
```

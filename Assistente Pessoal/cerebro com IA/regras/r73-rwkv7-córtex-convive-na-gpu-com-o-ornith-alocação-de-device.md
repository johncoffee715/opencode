---
regra: R73
titulo: "RWKV7 CÓRTEX CONVIVE NA GPU COM O ORNITH (alocação de device)"
fonte: AGENTS.md (linha 851)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R73 — RWKV7 CÓRTEX CONVIVE NA GPU COM O ORNITH (alocação de device) — promulgado 2026-08-28 ═══

**Regra**: o RWKV7-G1d-0.4B-Instruct-FP16 (:9084, Córtex Sensorial R71) pode e DEVE conviver na GPU MI50 junto com o Ornith (:8083) — **desde que a VRAM permita** (verificação via rocm-smi antes do launch).

## Por que é viável (R46 dissecação)
- **Arquitetura RWKV v7 (DeltaNet + attention hybrid)**: state linear FIXO (~10MB), o ctx 1M **NÃO** custa KV cache extra — diferente de transformers (KV cresce com ctx).
- Pesos FP16: 0.91GB + state 0.01GB + buffers 0.5GB ≈ **1.42GB total**.
- Medição real: Ornith@258K + apps = 12.40GB → + RWKV7 = **13.82GB** de 17.16GB (folga 3.34GB).

## Ganho medido (2026-08-28)
| Métrica | CPU (-ngl 0) | GPU (-ngl 999) |
|---------|-------------|----------------|
| RWKV7 decode | 14-20 t/s | **86.82 t/s** (4-6×) |
| RWKV7 simultâneo c/ Ornith | — | 67.05 t/s |
| Ornith solo | 53.76 t/s | 54.48 t/s |
| Ornith simultâneo c/ RWKV7 | — | **54.53 t/s** (queda ~0%) |

## Implementação
- `start-stack.sh` :9084: `-c 1048576 -np 1 -b 512 -ngl 999 -dev Vulkan0 --cache-type-k q4_0 --cache-type-v q4_0 --jinja`
- Guarda: antes de subir, `rocm-smi --showmeminfo vram` → se folga < 1.5GB, manter RWKV7 em CPU (`-ngl 0`).
- O Ornith permanece primário: se houver contenção de compute, o córtex (tarefas curtas) cede naturalmente.

---

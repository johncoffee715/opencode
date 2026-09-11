---
regra: R72
titulo: "GUARDRAIL CPU: NÃO LIMITAR RECURSOS DE CPU PARA LLMs LOCAIS"
fonte: AGENTS.md (linha 833)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R72 — GUARDRAIL CPU: NÃO LIMITAR RECURSOS DE CPU PARA LLMs LOCAIS — promulgado 2026-08-28 ═══

**Regra**: NUNCA limitar artificialmente recursos de CPU para LLMs locais (slots CPU da stack) — exceto quando o usuário solicitar explicitamente. As **36 threads** do Xeon E5-2699v3 ficam **totalmente disponíveis**, escalonadas **conforme oferta e demanda** (o scheduler do SO + llama.cpp fazem o escalonamento natural).

## Princípios
1. **Sem `-t` fixo por slot**: remover `-t 18`/`-t N` arbitrários dos launches CPU — deixar o llama.cpp auto-detectar (default) e o CFS do Linux escalonar entre processos.
2. **Oferta e demanda**: quando um slot está ativo, ele usa as threads que precisar; quando ocioso, libera para os demais. Nenhum slot tem reserva artificial.
3. **Exceção**: somente se o usuário pedir explicitamente (ex.: "limita 9088 a 4 threads") — nunca por decisão do orquestrador.
4. **Escalonamento**: a contenção real (vários slots simultâneos) é resolvida pelo scheduler do SO — não por limitação preventiva no launch.
5. **Benchmark como evidência**: medições SOLO vs SIMULTÂNEO (2026-08-28) mostraram que `-t 18` × 9 slots = 162 threads configuradas causava oversubscription severa (timeouts no simultâneo). A correção é remover a limitação, não aumentá-la.

## Implementação
- `start-stack.sh`: slots CPU SEM `-t` fixo (default llama.cpp).
- GPU: Ornith (:8083) permanece `-ngl 999 -dev Vulkan0`; slots CPU permanecem `-ngl 0` (R62 — nunca vazar VRAM).
- Exceção documentada: RWKV7 Córtex (:9084) pode conviver na GPU com o Ornith se VRAM permitir (R73) — mas isso é decisão de alocação de device, não de CPU.

---

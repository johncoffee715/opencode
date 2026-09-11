---
regra: R12
titulo: "SilverHawk: Função de Interpretação + Reporting de Feedback + Fine-tuning (Design) — GLOBAL"
fonte: AGENTS.md (linha 58)
data: 2026-09-11
---

## R12 — SilverHawk: Função de Interpretação + Reporting de Feedback + Fine-tuning (Design) — GLOBAL
- A **skill SilverHawk** tem a **função de interpretação de imagens, vídeo e áudio** no harness: traduz outputs multimodais (visão/imagem/áudio/vídeo) para o orquestrador.
- **Reporting de feedback ao orquestrador para o scaffold**: todo output interpretado pelo SilverHawk gera **feedback traduzido** (sucesso/falha + descrição) que alimenta o scaffold via `record_decision()` → `_scores_from_log()` → boost `learned * 0.5` em `select_for_task()` — o orquestrador **aprende** qual recurso/modelo entrega para cada tipo de task multimodal.
- **Fine-tuning em tarefas de design**: quando a task é de **design** (visual, estética, layout, UI, estilo), o feedback do SilverHawk é usado como **fine-tuning** — reforça/penaliza os scores do scaffold para que iterações futuras de design roteiem melhor (oferta→demanda R5 adaptativa).
- **Roteamento**: tasks com `design, áudio, estética, estilo, layout, visual, feedback` → SilverHawk/LFM 2.5-VL-1.6B (`filter_fast`, local-lfm :8081), fallback omniroute (R10).
- Mecanismo: skill `~/.config/opencode/skills/silverhawk/` + tags `design, audio, estetica, estilo, layout, ui, feedback` + `MODEL_CAPS.filter_fast` em `harness/core/integration.py` + decision-log `harness/decision-log.jsonl`.
- Regra promulgada pelo usuário: "silverhawk função de interpretação de imagens, vídeo, áudio reportando feedbacks de outputs traduzido pro orquestrador para scaffold no harness e fine tuning quando relacionado a tarefas de design".

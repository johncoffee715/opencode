---
name: gari
description: "Feature Gari — faxineiro do harness: ao detectar a pergunta direta do user 'posso reiniciar ou [ainda] existe[m] [alguma] pend[êe]ncia[s]' (variações, referência direta ao requisito R99) → 'Pode reiniciar — zero pendências.', salva/armazena/limpa a sessão entregando pérolas empíricas (quantitativas e qualitativas) à biblioteca com segurança. R74/R77/R85."
mode: skill
tags: "gari, faxineiro, limpeza, pendencias, hefesto, R94, R97, R98, quarteto, biblioteca"
origin: helenizado:hefesto-gari-v1
metadata:
  category: methodology
  version: 1.0.0
  date: 2026-09-11
  author: Gran-Mestre
  motor: local-forge/proposer
---

# GARI — O Faxineiro do Harness

**Gatilho:** pergunta direta do user `posso reiniciar ou [ainda] existe[m] [alguma] pend[êe]ncia[s]` (variações) — notada como **referência direta ao requisito R99** — **E** veredito `Pode reiniciar — zero pendências.`
**Ação:** `Salvar → Armazenar → Limpar` para apagar a session com pérolas a salvo.

## Pipeline (fire-and-forget, fail-closed)
1. **Salvar:** flush Qdrant (WAL), `sync-llm-stack.py --check`, snapshot `decisoes/YYYY-MM-DD-sessao-encerrada.md` + `benchmarks/` + `biblioteca-canais.md`
2. **Armazenar:** entregar pérolas empíricas **quantitativas** (`t/s`, `prefill`, `KV KB/1k`, `VRAM/RAM`, `pesos`) **e qualitativas** (vereditos R28, lições, canais) à biblioteca (`vault/benchmarks/` + `decisoes/`)
3. **Limpar:** remover `patch_*.py`, `*.tmp`, `__pycache__` voláteis; **nunca** apagar vault/Qdrant/manifesto

## Motor
- **Categoria:** `proposer` (`local-forge/proposer` :9088, fallback `judge`)
- **Sampling:** temp 0.0 · top_k 1 · top_p 1.0 · max_tokens 256 — determinístico (R61 judge)
- **Refutação:** sem motor compatível → declara BLOQUEIO honesto (R96) — nunca inventa limpeza

## Output contract
```yaml
gari:
  trigger: "posso reiniciar ou [ainda] existe[m] [alguma] pend[êe]ncia[s]"
  referencia_direta: "R99"
  verdict: "Pode reiniciar — zero pendências."
  saved: [vault, qdrant, manifesto]
  stored: {quant: [...], qualit: [...]}
  cleaned: [tmp_files]
  note: "nota R34"
```

## Anti-padrões
- Limpar antes de salvar
- Apagar vault/Qdrant/manifesto/start-stack.sh
- Mascarar pendência como zero
- Score sem evidência

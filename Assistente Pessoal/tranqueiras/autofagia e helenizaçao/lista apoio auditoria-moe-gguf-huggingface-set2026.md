# Auditoria de Modelos MoE em GGUF — HuggingFace (Setembro/2026)

## Metodologia e escopo

Levantamento feito via busca ativa (HuggingFace + blogs oficiais + PRs do llama.cpp), não da memória do modelo — esse espaço mudou muito desde o corte de treinamento (Qwen já em 3.6, DeepSeek em V4, GLM em 5.2). Cobre lançamentos **nativos** de MoE (arquitetura treinada assim desde o início) com pelo menos uma conversão GGUF confirmada.

Modelos **FrankenMoE** (merges comunitários de modelos densos fingindo ser MoE — ex. coleção `DavidAU`, `mradermacher/*-MoE-GGUF`) ficam de fora da tabela principal: são centenas de repos, sem curadoria de qualidade consistente. Ponteiro no final.

Tamanhos de arquivo são os que apareceram nos cards reais — onde não achei um valor confirmado, deixei "ver repositório" em vez de estimar.

**Seu hardware** (do perfil): MI50 16GB (gfx906) + 32GB RAM DDR4 = **48GB combinados** (VRAM+RAM, útil para MoE com offload de experts via `--cpu-moe`/`--n-cpu-moe` no llama.cpp). Guia de compatibilidade no final do documento.

---

## Alibaba / Qwen

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| Qwen1.5-MoE-A2.7B | ~14B / 2.7B | 8K | IQ3_XS 6.52GB | `RichardErkhov/Qwen_-_Qwen1.5-MoE-A2.7B-gguf` | Apache 2.0 | Legado (2024), mas ainda o menor MoE "de verdade" da família |
| Qwen3-30B-A3B | 30B / 3B | 262K (YaRN) | ver repositório | vários (unsloth, bartowski) | Apache 2.0 | Geração original Qwen3, ainda muito usada |
| Qwen3-235B-A22B | 235B / 22B | 128K | ver repositório | vários | Apache 2.0 | Flagship original — precisa de ~140GB+ mesmo em Q4 |
| Qwen3-Coder-30B-A3B | 30B / 3B | 256K | ver repositório | vários | Apache 2.0 | Mesma arquitetura do 30B-A3B, treinado em 7.5T tokens de código |
| Qwen3-Coder-480B-A35B | 480B / 35B | 256K | ver repositório | vários | Apache 2.0 | Monstro agêntico — território de datacenter (250GB+) |
| Qwen3.5-35B-A3B / 122B-A10B / 397B-A17B | 35B–397B / 3B–17B | — | ver repositório | vários | Apache 2.0 | Lançado fev/2026, três tamanhos MoE |
| **Qwen3.6-35B-A3B** | 35B / ~3B | 262K nativo (YaRN até ~1M) | UD-IQ1_M **10GB** / UD-Q4_K_M 22.1GB | `unsloth/Qwen3.6-35B-A3B-GGUF` | Apache 2.0 | Abr/2026, o "atual" da comunidade — melhor custo-benefício ativo/tamanho da família toda |

## DeepSeek

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| DeepSeek-V2.5 | 236B / 21B | 128K | Q2_K ~86GB | `bartowski/DeepSeek-V2.5-GGUF` | deepseek license | Legado, ainda referência de tamanho médio |
| DeepSeek-V3 | 671B / 37B | 128K | Q2_K_L (ver repo) / Q4_K_M ~405GB | `unsloth/DeepSeek-V3-GGUF` | MIT | Bem maduro no llama.cpp mainline |
| DeepSeek-V3.2 / V3.2-Speciale / V3.2-Exp | 672B / ~37B | 128K | Q4_K_M 405GB | `createthis/DeepSeek-V3.2-GGUF`, `sszymczyk/DeepSeek-V3.2-nolight-GGUF` | MIT | **Experimental**: llama.cpp ainda não suporta a Sparse Attention nova, roda com atenção "antiga" da V3.1 |
| DeepSeek-V4-Flash | 284B / 13B | 1M | Q2_K_S 98.6GB | `ggml-org/DeepSeek-V4-Flash-GGUF`, `unsloth/DeepSeek-V4-Flash-GGUF` | MIT | Mais viável dos V4, mas ainda pesado |
| DeepSeek-V4-Pro | 1.6T / 49B | 1M | Q2_K-XL (ver repo) | `batiai/DeepSeek-V4-Pro-GGUF`, `teamblobfish/DeepSeek-V4-Pro-GGUF` | MIT | **Early access** — exige fork específico do llama.cpp (não roda no mainline ainda) |

## Moonshot AI (Kimi)

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| Kimi-K2.6 | 1T / 32B | 256K (YaRN) | Q2_K 644GB / IQ3_XXS-IQ4_XS (ver repo) | `unsloth/Kimi-K2.6-GGUF`, `bartowski/moonshotai_Kimi-K2.6-GGUF`, `ubergarm/Kimi-K2.6-GGUF` | Modified MIT | Multimodal nativo (texto+imagem no GGUF; vídeo ainda não suportado no llama.cpp) |
| Kimi-K3 | 2.8T / ver repo | ver repo | ver repositório | `6block/Kimi-K3-GGUF`, `unsloth/Kimi-K3-GGUF` | ver repo | **Muito recente / suporte imaturo** — há relatos na comunidade de quants quebrados/incompletos |

## Zhipu / Z.ai (GLM)

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| GLM-4.5 | 355B / ~32B | 128K | ver repositório | vários | MIT | |
| GLM-4.6 | 357B / ~32B | 200K | ver repositório | `unsloth/GLM-4.6-GGUF` | MIT | |
| GLM-4.6V | 107B / ver repo | ver repo | Q4_K_M 70.4GB / Q8_0 114GB | `ggml-org/GLM-4.6V-GGUF` | MIT | Variante de visão |
| **GLM-4.7-Flash** | 30B / ver repo | ver repo | MXFP4_MOE **17.3GB** | `noctrex/GLM-4.7-Flash-MXFP4_MOE-GGUF` | MIT | O GLM "pequeno" — candidato forte para sua VRAM |
| GLM-5 | 754B / ver repo | ver repo | Q4_K_M 465GB | `unsloth/GLM-5-GGUF`, `AesSedai/GLM-5-GGUF`, `ubergarm/GLM-5-GGUF` | MIT | Integra DeepSeek Sparse Attention (DSA); GGUF exige PR específico do llama.cpp |
| GLM-5.2 | 744B / ~40B | 1M | ver repositório | ver repo | MIT | Flagship atual (jun/2026), líder entre os open-weight em vários benchmarks |

## Meta (Llama 4)

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| Llama 4 Scout | 109B / 17B (16 experts) | 10M (nominal) | Q2_K ~36.8GB (merged) | `unsloth/Llama-4-Scout-17B-16E-Instruct-GGUF`, `bartowski/meta-llama_Llama-4-Scout-17B-16E-Instruct-GGUF` | Llama 4 Community License (custom) | Multimodal nativo (texto+imagem) |
| Llama 4 Maverick | ~400B / 17B (128 experts) | 1M (nominal) | ver repositório | `unsloth/Llama-4-Maverick-17B-128E-Instruct-GGUF` | Llama 4 Community License (custom) | Sem atualização confirmada além do Maverick/Scout nesta pesquisa |

## OpenAI (gpt-oss)

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| **gpt-oss-20b** | 21B / 3.6B | 128K (YaRN) | nativo MXFP4 (cabe em ~16GB) | `unsloth/gpt-oss-20b-GGUF`, vários | Apache 2.0 | Peso nativo já em MXFP4 4-bit — não precisa requantizar muito |
| gpt-oss-120b | 117B / 5.1B | 128K (YaRN) | nativo MXFP4 (~65GB) | `unsloth/gpt-oss-120b-GGUF`, `gabriellarson/gpt-oss-120b-GGUF` | Apache 2.0 | Projetado para caber em 1x H100 80GB — passa dos seus 48GB combinados |

## MiniMax

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| MiniMax-M2 | 230B / 10B | 196K | MXFP4_MOE 124GB | `unsloth/MiniMax-M2-GGUF`, `noctrex/MiniMax-M2-MXFP4_MOE-GGUF`, `cturan/MiniMax-M2-GGUF` | MIT | #1 em score composto entre open-source (Artificial Analysis, na época do lançamento) |
| MiniMax-M2.1 | 456B / 45.9B | ver repo | ver repositório | `unsloth/MiniMax-M2.1-GGUF` | MIT | Suporte GGUF chegou via PR no transformers em mar/2026 |
| MiniMax-M2.5 | ~230B / ver repo | 196K | F16 master 457GB (quants derivados menores) | `ox-ox/MiniMax-M2.5-GGUF`, `noctrex/MiniMax-M2.5-MXFP4_MOE-GGUF` | MIT | |
| MiniMax-M2.7 | ~228B / 10B | ver repo | ver repositório (Q4_K_M relatado com bug de NaN em uma tensor específica, contornável) | `unsloth/MiniMax-M2.7-GGUF`, `AesSedai/MiniMax-M2.7-GGUF`, `Youssofal/MiniMax-M2.7-GGUF` | MIT | Mais recente da linha; arquitetura MiniMax-M2 no llama.cpp "ainda amadurecendo" |

## Tencent

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| Hunyuan-A13B | 80B / 13B | ver repo | ver repositório | `tencent/Hunyuan-A13B-Instruct-GGUF` | Licença comunitária própria da Tencent | GGUF oficial da própria Tencent |
| Hunyuan-Large (A52B) | 389B / 52B | ver repo | ver repositório | busca por conversões comunitárias | Licença comunitária própria da Tencent | Mais antigo (2024), foi o maior MoE open-source da época |
| Hy3-preview | 295B / 21B | ver repo | ver repositório | `tencent` (pesos públicos desde 23/abr/2026) | ver repo | Foco em STEM/coding; avaliação independente (Epoch AI) ainda pendente na época da publicação |

## Baidu (ERNIE)

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| **ERNIE-4.5-21B-A3B** (PT e Thinking) | ~21-22B / 3B | ver repo | Q3_K_M 10.5GB / Q4_K_M **13.2GB** | `lmstudio-community/ERNIE-4.5-21B-A3B-PT-GGUF`, `enacimie/...`, `AmpereComputing/...` | Apache 2.0 | Um dos melhores candidatos para caber inteiro na sua VRAM |
| ERNIE-4.5-A47B (série maior) | ver repo / 47B | ver repo | ver repositório | buscar `baidu/ERNIE-4.5-...-A47B` | Apache 2.0 | Não aprofundei o total exato — o card enfatiza a série A47B e A3B como as duas MoE principais do 4.5 |

> **Atenção:** ERNIE 5.0 e 5.1 (mai/2026) são **fechados** — Baidu não liberou pesos. Não há GGUF possível dessas versões.

## Mistral AI

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| Mistral Large 3 | 675B / 41B | 256K | ver repositório | buscar `mistralai/Mistral-Large-3` conversões GGUF | Apache 2.0 | Lançado dez/2025, primeiro MoE grande da Mistral fora da linha Mixtral |
| Mixtral 8x7B | ~47B / ~13B | 32K | amplamente disponível, poucos GB em Q4 | `TheBloke/Mixtral-8x7B-*-GGUF` e sucessores | Apache 2.0 | O clássico que popularizou MoE em GGUF (2023) |
| Mixtral 8x22B | ~141B / ~39B | 64K | ver repositório | vários | Apache 2.0 | |

## Google DeepMind (Gemma 4)

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| Gemma-4-26B-A4B | 26B / ~4B | 256K | ver repositório | `unsloth/gemma-4-...`, `batiai/Gemma-4-26B-A4B-it-GGUF` | Apache 2.0 (conforme card) | Único tamanho MoE da linha Gemma 4 — E2B/E4B/31B são densos, não MoE |

## NVIDIA (Nemotron 3)

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| Nemotron-3-Nano-30B-A3B | 30B / 3.5B | ver repo | ver repositório | `unsloth/Nemotron-3-Nano-30B-A3B-GGUF` | NVIDIA Open Model License | Híbrido Mamba-2 + MoE (23 camadas Mamba/MoE + 6 de atenção) |
| Nemotron-3-Nano-Omni-30B-A3B | 30B / 3.5B | ver repo | NVFP4 **20.9GB** / FP8 32.8GB | `unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF` | NVIDIA Open Model License | Variante multimodal (visão+áudio) |
| Nemotron-3-Super-120B-A12B | 120B / 12B | ver repo | ver repositório | `unsloth/NVIDIA-Nemotron-3-Super-120B-A12B-GGUF` | NVIDIA Open Model License | Arquitetura "LatentMoE" híbrida com Multi-Token Prediction |

## AI21 (Jamba — híbrido Mamba+MoE)

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| Jamba Mini 1.7 | ver repo | 256K | ver repositório | `bartowski/ai21labs_AI21-Jamba-Mini-1.7-GGUF` | Jamba Open Model License (verificar) | Híbrido Transformer+Mamba+MoE |
| Jamba Large 1.6 | ver repo | 256K | ver repositório | `mradermacher/AI21-Jamba-Large-1.6-GGUF` | Jamba Open Model License (verificar) | |
| Jamba Reasoning 3B | 3B (predominantemente denso+Mamba) | 256K | ver repositório | `ai21labs/AI21-Jamba-Reasoning-3B-GGUF` | Apache 2.0 (verificar) | Pequeno, cabe fácil — mas confirme se a build específica usa camadas MoE ou é só híbrido denso |

## xAI (Grok)

| Modelo | Params (total/ativo) | Contexto | Menor GGUF confirmado | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|---|
| Grok-1 | 314B / MoE (contagem de ativos não confirmada nesta pesquisa) | 8K | ver repositório | `Arki05/Grok-1-GGUF` | Apache 2.0 | Suporte prático fraco — mesmo quantizado pede 4-8 GPUs de datacenter |
| Grok-2 | não confirmado nesta pesquisa | ver repo | ver repositório | `unsloth/grok-2-GGUF` | verificar | Pesos abertos por xAI em 2026; não aprofundei parâmetros exatos |

## Legado / fundacionais adicionais

| Modelo | Params (total/ativo) | Contexto | Repos de referência | Licença | Notas |
|---|---|---|---|---|---|
| DBRX | 132B / 36B | 32K | buscar `databricks/dbrx-instruct` GGUF comunitário | Databricks Open Model License | Databricks, 2024 — pouco atualizado desde então |
| OLMoE-1B-7B | 7B / 1B | 4K | buscar `allenai/OLMoE-1B-7B` GGUF comunitário | Apache 2.0 | Único 100% aberto (pesos + dados + logs de treino); roda em quase qualquer coisa |

---

## Ecossistema FrankenMoE (merges comunitários — fora da lista principal)

Além dos MoE "nativos" acima, existe um ecossistema grande de **merges** que combinam modelos densos já prontos num MoE via `mergekit`/`lazymergekit` (não são pré-treinados como MoE desde o início). Qualidade varia muito, sem curadoria central. Principais pontos de entrada se quiser explorar:

- Coleção `DavidAU` — maior curadoria de MoE/FrankenMoE com foco em reasoning: `huggingface.co/collections/DavidAU/moe-mixture-of-experts-models-see-also-source-cll`
- `mradermacher/*-MoE-GGUF` — quantizações em lote de merges de terceiros (ex. `MultiverseEx26-Neurallaymons-12B-MoE-GGUF`, `Calmex26-10B-MoE-GGUF`)
- Modelos antigos como `TheBloke/PiVoT-MoE-GGUF`, `MaziyarPanahi/MixTAO-7Bx2-MoE-v8.1-GGUF`

## Notas de compatibilidade para seu hardware (MI50 16GB + 32GB RAM)

Sem filtrar nada da lista acima — só para orientar a ordem da sua auditoria:

**Cabem quase inteiros na VRAM da MI50 (Q4 ou nativo, sem depender de offload agressivo):**
ERNIE-4.5-21B-A3B (13.2GB), gpt-oss-20b (nativo MXFP4), GLM-4.7-Flash (17.3GB), Nemotron-3-Nano-Omni-30B-A3B em NVFP4 (20.9GB), Qwen3.6-35B-A3B em IQ1/IQ2 (10-12GB, com perda de qualidade).

**Cabem nos 48GB combinados com offload de experts (`--cpu-moe` / `-ngl` parcial no llama.cpp):**
Qwen3-30B-A3B, Qwen3.6-35B-A3B (Q4, 22.1GB), Nemotron-3-Nano-30B-A3B, Mixtral-8x7B, Llama-4-Scout (em Q2, 36.8GB — Q4 já não cabe), Hunyuan-A13B (só em quant agressivo).

**Passam dos 48GB combinados — armazenamento maior (seu projeto Jarvis/v12) resolve *guardar* o arquivo, mas não resolve *rodar* em velocidade razoável; precisariam de offload em disco (lento) ou upgrade de RAM/VRAM:**
DeepSeek-V3/V3.2/V4 (todos), Kimi-K2.6/K3, GLM-5/5.2, MiniMax-M2 (toda a linha), Qwen3-235B-A22B e maiores, Llama-4-Maverick, Mistral Large 3, GLM-4.6, Hunyuan-Large, Mixtral-8x22B, DBRX, Grok-1/2.

## Nomes que apareceram na pesquisa e não aprofundei (para você investigar se interessar)

MiMo-V2.5-Pro (Xiaomi, ~1T params, avistado de relance); rumor de modelo MoE open-weight da NVIDIA em torno da Computex 2026 (specs não confirmados na época); Inkling e Nemotron 3 "Lightning" (mencionados en passant em artigos, não verifiquei cards).

---
*Levantamento feito em 09/09/2026 via busca web. Dado o ritmo de lançamentos (Qwen, DeepSeek, GLM e Kimi lançaram versões novas em questão de semanas umas das outras), reconfirme tamanhos/licenças antes de baixar algo grande — GGUFs de modelos muito recentes (Kimi-K3, DeepSeek-V4-Pro, GLM-5) ainda têm suporte experimental ou dependem de forks do llama.cpp.*

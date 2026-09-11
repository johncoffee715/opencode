---
title: "Substitutos CPU para LLM"
source: "https://chatgpt.com/c/6aa2f255-2dc4-83e9-9fa5-f361b2ae7883"
author:
published:
created: 2026-09-10
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**Você disse**

me entregue uma lista de possiveis substitutos em cpu do meu llm principal (atual MoE 35B A3B) por ex: Arquiteturas Nativas de Orquestração ou uso geral para dia a dia, MoE (Mixture of Experts) de Alta Precisão ou MoEs de Alta Precisão em Escalas Reduzidas (Compact MoEs), Modelos Densos de Alta Eficiência (Mid-size Lossless/Q4~Q5), Arquiteturas Híbridas ou Recorrentes de Nova Geração (SSM / Mamba-2) e estou aberto a novas sugestoes fora as que ja conflitei em minha stack local conforme a imagem,

---

A melhor linha para substituir o seu **Qwen3.5-35B-A3B atual no CPU** não é simplesmente procurar “outro 35B”. Para seu E5-2699 v3 + 32 GB, eu priorizaria arquiteturas que reduzam **tráfego de memória, KV e custo de inferência**, mantendo capacidade de agente/orquestração.

Hoje, os candidatos realmente interessantes são estes:

| Prioridade | Modelo | Arquitetura | Escala | Papel no seu sistema | Veredito |
| --- | --- | --- | --- | --- | --- |
| **1** | **Nemotron-3-Nano-30B-A3B** | **Mamba-2 + Transformer + MoE** | 30B / 3.5B ativo | GM CPU / orquestração | ⭐⭐⭐⭐⭐ |
| **2** | **Gemma-4-26B-A4B** | **MoE** | 25.2B / 3.8B ativo | GM CPU / uso geral | ⭐⭐⭐⭐⭐ |
| **3** | **Qwen3-Coder-30B-A3B** | MoE | 30.5B / 3.3B ativo | GM especializado em engenharia | ⭐⭐⭐⭐½ |
| **4** | **Devstral-Small-2-24B** | Dense Transformer | 24B | Agente/OpenCode | ⭐⭐⭐⭐½ |
| **5** | **Granite-4.1-8B** | Hybrid SSM/Transformer | 8B | Supervisor rápido | ⭐⭐⭐⭐ |
| **6** | **Granite-4.1-3B** | Hybrid SSM/Transformer | 3B | roteador / planner / pré-processador | ⭐⭐⭐½ |
| **7** | **Gemma-4-31B** | Dense Transformer | 31B | qualidade máxima CPU | ⭐⭐⭐½ |
| **8** | **Magistral-Small-2509** | Dense reasoning | 24B | especialista matemático/raciocínio | ⭐⭐⭐½ |

### 1\. O candidato que eu testaria primeiro: Nemotron-3-Nano-30B-A3B

Esse é exatamente o tipo de arquitetura que estava faltando na sua bateria de testes.

O Nemotron-3-Nano possui **30B totais, aproximadamente 3,5B ativos**, mas não é simplesmente outro MoE Transformer. Ele combina **23 camadas Mamba-2/MoE e 6 camadas de atenção**, com 128 experts + 1 shared expert e 6 experts ativados por token. A NVIDIA o posiciona explicitamente para raciocínio, agentes e uso com ferramentas. [^1]

Isso é importante para seu projeto porque introduz uma variável arquitetural que você ainda não colocou no duelo:

**Qwen3.5 = MoE + arquitetura moderna de atenção**

versus

**Nemotron = MoE + Mamba-2 + atenção esparsa**

Ou seja, não seria apenas trocar pesos. Seria testar **outro paradigma de memória/computação**.

Há uma ressalva importante: houve problemas históricos de execução CPU-only do Nemotron em versões antigas do llama.cpp. Portanto ele merece teste, mas com uma build atual do runtime, não deve ser tratado como “plug-and-play comprovado” apenas por causa da arquitetura. [^2]

**Para seu laboratório, esse é provavelmente o experimento mais interessante de todos.**

---

Este é talvez o substituto mais equilibrado para seu GM.

O Gemma 4 26B-A4B possui aproximadamente **25,2B parâmetros totais e 3,8B ativos**, com **128 experts, 8 ativos + 1 shared**, contexto anunciado de até 256K e suporte multimodal. A própria Google o posiciona para raciocínio, código, function calling e agentes. [^3]

É particularmente interessante porque você consegue colocá-lo aproximadamente no mesmo envelope computacional do seu atual:

```
Qwen3.5-35B-A3B
35B total
~3B active

         VS

Gemma 4 26B-A4B
25.2B total
~3.8B active
```

Mas há uma diferença estratégica:

```
Qwen:
35B de capacidade total
3B ativo

Gemma:
25.2B de capacidade total
3.8B ativo
```

Então o Gemma abre uma pergunta interessante:

> **É melhor ter mais conhecimento representacional total ou maior capacidade ativa por token?**

Isso seria um teste realmente válido para seu meta-orquestrador.

E existe implementação GGUF para llama.cpp; relatos reais mostram o Gemma 4 26B-A4B Q4\_K\_M na faixa de ~16 GB, embora o desempenho dependa brutalmente da largura de banda da memória. [^4]

### Quantização que eu priorizaria

```
Q4_K_M / UD-Q4_K_XL
↓
Q3_K_M
↓
IQ3
```

Não começaria em IQ2.

Você já descobriu no seu próprio histórico que **reduzir demais a precisão pode destruir o papel do modelo no grafo**, mesmo quando a velocidade parece excelente.

---

## 3\. Qwen3-Coder-30B-A3B — extremamente interessante para o seu OpenCode

Esse é um caso diferente.

O Qwen3-Coder-30B-A3B possui:

```
30.5B total
3.3B ativos
128 experts
8 experts/token
256K nativos
```

e foi especificamente treinado para **agentic coding, tool calling e compreensão de repositórios grandes**. [^5]

Ele não seria minha primeira escolha como **GM universal**, porque seu treinamento é fortemente orientado a engenharia de software.

Mas para sua arquitetura:

```
META-ORQUESTRADOR
                  │
      ┌───────────┴───────────┐
      │                       │
   GM/Planner             OpenCode
      │                       │
Gemma/Nemotron         Qwen3-Coder
```

isso é excelente.

Ou seja:

**não precisa substituir o GM. Pode substituir a necessidade do GM fazer tudo.**

Seu meta-orquestrador poderia mandar:

```
raciocínio geral → GM
código → Qwen3-Coder
shell/tool calling → Qwen3-Coder
análise de repositório → Qwen3-Coder
planejamento complexo → GM
```

Isso provavelmente produziria um sistema melhor que simplesmente procurar “um modelo vencedor”.

---

## 4\. Devstral Small 2 24B

Aqui temos outra filosofia.

Devstral Small 2 é **24B denso**, projetado especificamente para agentes de engenharia de software, exploração de código, edição de múltiplos arquivos e uso de ferramentas. A Mistral reporta **68% no SWE-bench Verified** para essa versão. [^6]

O ponto forte dele não é:

> “Sou o modelo mais barato por token.”

É:

> **“Se você me colocar dentro de um agente de programação, eu sei trabalhar como agente.”**

Isso é muito compatível com sua arquitetura OpenCode.

A desvantagem para seu CPU é estrutural:

```
MoE 3B ativo
        ↓
pouco cálculo por token

Dense 24B
        ↓
muito mais cálculo/memória por token
```

Então ele provavelmente perderá em **tok/s** para seus MoEs.

Mas pode ganhar em **qualidade de ação por token**.

Esse é exatamente o tipo de candidato que seu benchmark atual precisa separar.

---

## 5\. Granite 4.1 — candidato experimental de arquitetura

Aqui começa uma linha que eu considero **subestimada para seu sistema**.

O Granite 4.1 é uma família recente da IBM e há variantes pequenas com arquitetura híbrida. O Granite 4.1-3B, por exemplo, foi lançado em abril de 2026, possui foco explícito em **tool calling, instruction following e conversação**, e suporta português. [^7]

Mais interessante ainda: a família Granite 4 utiliza arquiteturas híbridas envolvendo **Mamba e atenção**. [^8]

Isso faz o Granite interessante não como substituto direto do 35B, mas como:

```
META-ORQUESTRADOR
              │
     ┌────────┴────────┐
     │                 │
 Granite           GM principal
3B / 8B             26-35B
     │
routing/planning
```

Um modelo pequeno e rápido pode analisar a tarefa e decidir:

```
GENERAL
CODING
REASONING
RAG
TOOL
VISION
LONG-CONTEXT
```

antes de acordar o modelo pesado.

Isso pode reduzir drasticamente o número de tokens processados pelo seu GM.

---

## 6\. Gemma 4 31B

Também colocaria na bateria.

É o contraponto necessário ao MoE:

```
Gemma 4 26B A4B
25.2B / 3.8B
MoE

vs

Gemma 4 31B
31B
Dense
```

A documentação atual do Gemma 4 confirma as variantes 26B-A4B e 31B, com contexto de até 256K nas variantes médias. [^3]

Para CPU isso normalmente significa:

**muito mais memória movimentada por token.**

Mas se a qualidade cognitiva do 31B compensar, ele pode ser interessante como:

```
"modo precisão"
```

do seu GM.

---

## 7\. Magistral Small 24B

Eu colocaria como **especialista**, não como substituto universal.

É uma versão de raciocínio de 24B baseada na linha Mistral Small. A própria Mistral afirma que a versão quantizada cabe em 32 GB de RAM. [^9]

Arquiteturalmente:

```
Magistral
    ↓
reasoning especializado
    ↓
GM consulta quando necessário
```

Isso combina muito bem com sua filosofia de **task fragmentation + especialistas**.

---

## O ponto mais importante: não trate todos como candidatos ao mesmo cargo

Eu dividiria seu benchmark em **5 classes**.

### Classe A — substituto direto do GM

```
1. Nemotron-3-Nano-30B-A3B
2. Gemma-4-26B-A4B
3. Gemma-4-31B
```

Esses precisam disputar:

```
coerência
raciocínio
planejamento
tool use
memória de contexto
resistência a loops
consistência multi-turno
```

---

### Classe B — GM orientado a agente

```
4. Qwen3-Coder-30B-A3B
5. Devstral-Small-2-24B
```

Aqui o benchmark precisa ser completamente diferente:

```
TASK
↓
PLAN
↓
TOOL CALL
↓
OBSERVAÇÃO
↓
CORREÇÃO
↓
NOVO TOOL CALL
↓
CONCLUSÃO
```

Seu sistema já é essencialmente isso.

---

### Classe C — Compact MoE

Aqui eu procuraria deliberadamente modelos na faixa:

```
10–30B total
2–5B ativo
```

porque essa é provavelmente a região mais interessante para o seu Xeon.

O Gemma 4 26B-A4B é atualmente o exemplo mais óbvio dessa classe. [^3]

---

### Classe D — Hybrid SSM

Aqui a prioridade é:

```
Nemotron 3 Nano
Granite 4.x
```

O objetivo não é somente ganhar qualidade.

É descobrir se:

**SSM/Mamba + pouca atenção**

produz uma vantagem sistêmica no seu ambiente CPU.

Isso é particularmente relevante para o seu projeto de memória porque um modelo híbrido pode mudar completamente a economia do estado de contexto.

---

### Classe E — dense eficiente

Eu testaria:

```
Devstral Small 2 24B
Magistral Small 24B
Gemma 4 31B
Phi-4-reasoning 14B
```

O Phi-4-reasoning é um dense Transformer de 14B, com foco em matemática, ciência e código. [^10]

Ele não é candidato ao mesmo teto de capacidade do 35B-A3B, mas é excelente como **controle experimental**:

```
14B dense
       vs
25B MoE
       vs
30B MoE
       vs
30B Hybrid
```

Isso permitirá medir o que realmente está dando ganho no seu sistema.

---

## Minha shortlist para o seu hardware

Considerando especificamente:

```
Xeon E5-2699 v3
18C / 36T
DDR4-2400 quad-channel
32 GB RAM
MI50 16 GB
GPU reservada para outro LLM
```

eu montaria a fila assim:

```
CPU GM CANDIDATES

             ┌───────────────────────┐
             │  Nemotron 3 Nano     │
             │  30B-A3B Hybrid      │
             └──────────┬────────────┘
                        │
                  PRIMEIRO TESTE
                        │
             ┌──────────▼────────────┐
             │ Gemma 4 26B-A4B       │
             │ 25B / 3.8B            │
             └──────────┬─────────────┘
                        │
                 SEGUNDO TESTE
                        │
       ┌────────────────┴───────────────┐
       │                                │
Qwen3-Coder 30B                  Devstral Small 2
   A3B                              24B Dense
       │                                │
 agente/código                      agente
       │                                │
       └────────────────┬───────────────┘
                        │
             ┌──────────▼───────────┐
             │ Gemma 4 31B         │
             │ Dense                 │
             └──────────┬───────────┘
                        │
             ┌──────────▼───────────┐
             │ Granite 4.x          │
             │ Hybrid SSM            │
             └───────────────────────┘
```

### Meu ranking de interesse para o seu projeto

**Não é ranking absoluto de benchmark; é ranking arquitetural para seu hardware + seu meta-orquestrador.**

**1\. Nemotron-3-Nano-30B-A3B**

**2\. Gemma-4-26B-A4B**

**3\. Qwen3-Coder-30B-A3B**

**4\. Devstral-Small-2-24B**

**5\. Gemma-4-31B**

**6\. Granite-4.1**

**7\. Magistral-Small-2509**

**8\. Phi-4-reasoning-14B**

---

## E existe uma conclusão ainda mais importante

Eu **não substituiria imediatamente o Qwen3.5-35B-A3B atual**.

Seu histórico mostra algo muito valioso:

```
Qwen3.5-35B-A3B IQ3
        ↓
6.0 / 6
        ↓
7 duelos vencidos
```

Então ele não precisa ser derrotado em um benchmark convencional.

O substituto precisa apresentar:

```
QUALIDADE ≥ 6.0/6
AND
VELOCIDADE ≥ atual
AND
TOOL RELIABILITY ≥ atual
AND
LOOP RESISTANCE ≥ atual
AND
LONG-CONTEXT STABILITY ≥ atual
AND
MEMORY COST ≤ atual
```

Esse último conjunto é o verdadeiro **Pareto frontier** do seu GM.

E eu adicionaria um sexto eixo que você ainda não colocou explicitamente na tabela:

```
ARCHITECTURAL EFFICIENCY
```

Porque um:

```
30B-A3B Transformer
```

e um:

```
30B-A3B Mamba2+MoE
```

podem ter o mesmo número de parâmetros ativos e apresentar comportamento radicalmente diferente no CPU.

**Para o seu projeto, o duelo que mais vale a pena realizar agora é:**

```
Qwen3.5-35B-A3B IQ3_XXS  ← atual GM
            VS
Gemma 4 26B-A4B Q4
            VS
Nemotron-3-Nano-30B-A3B Q4/Q5
            VS
Qwen3-Coder-30B-A3B Q4
            VS
Devstral-Small-2-24B Q4
```

Isso finalmente coloca **MoE, Compact-MoE, Hybrid-Mamba e Dense Agentic** dentro do mesmo campo de batalha, sem repetir os modelos que já foram eliminados na sua própria stack.

[^1]

[^1]: [huggingface.co](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16?utm_source=chatgpt.com)

[^2]: [github.com](https://github.com/ggml-org/llama.cpp/issues/18099?utm_source=chatgpt.com)

[^3]: [huggingface.co](https://huggingface.co/google/gemma-4-26B-A4B?utm_source=chatgpt.com)

[^4]: [github.com](https://github.com/ggml-org/llama.cpp/discussions/24222?utm_source=chatgpt.com)

[^5]: [huggingface.co](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct?utm_source=chatgpt.com)

[^6]: [huggingface.co](https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512?utm_source=chatgpt.com)

[^7]: [huggingface.co](https://huggingface.co/ibm-granite/granite-4.1-3b/blob/main/README.md?utm_source=chatgpt.com)

[^8]: [huggingface.co](https://huggingface.co/ibm-granite/granite-4.0-h-small-base/blob/main/config.json?utm_source=chatgpt.com)

[^9]: [huggingface.co](https://huggingface.co/mistralai/Magistral-Small-2509?utm_source=chatgpt.com)

[^10]: [huggingface.co](https://huggingface.co/microsoft/Phi-4-reasoning?utm_source=chatgpt.com)
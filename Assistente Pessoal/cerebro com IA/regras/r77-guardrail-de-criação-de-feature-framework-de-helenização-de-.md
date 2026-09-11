---
regra: R77
titulo: "GUARDRAIL DE CRIAÇÃO DE FEATURE (FRAMEWORK DE HELENIZAÇÃO DE FEATURES COGNITIVAS: ONTOLOGIA · FIREWALL · MECÂNICA)"
fonte: AGENTS.md (linha 994)
data: 2026-09-11
---

# ═══ REGRA GLOBAL R77 — GUARDRAIL DE CRIAÇÃO DE FEATURE (FRAMEWORK DE HELENIZAÇÃO DE FEATURES COGNITIVAS: ONTOLOGIA · FIREWALL · MECÂNICA) — promulgado 2026-08-30 (refinado) ═══

**Regra**: TODA feature nova — inclusive as helenizadas — nasce com 3 camadas obrigatórias, desvinculando a ideação da geração crua de código e impondo controle total de engenharia. A criatividade multiforme humana entra na concepção dos limites e personas; a inteligência artificial entra na execução implacável, processando fluxos complexos sem fadiga cognitiva.

## 1. Ontologia e Âncora Semântica (.md) — CONCEITO/PERSONA

- **Função**: criar o manifesto ontológico da feature — NÃO documentação passiva, mas a matriz comportamental e a persona operacional.
- **Engenharia**: o .md define escopo, persona, vocabulário técnico aceitável e limites contextuais do que a feature É e do que ela REJEITA ser.
- **Aplicação**: serve como System Prompt primário imutável que molda a identidade da feature antes de qualquer inferência.
- **Sweet spot**: 50–100 linhas (.md); até 200 linhas para instrução (máx).

## 2. Firewall Estrutural e Comportamental (.json) — GABARITO ESTRATÉGICO

- **Função**: gabarito estratégico RÍGIDO de permissões e negações — camada determinística de segurança e escopo.
- **Engenharia**: o JSON é um contrato de invariantes: define explicitamente o que o modelo PODE executar (ex.: leitura de arquivos do Vault, chamadas de ferramentas específicas) e o que é VETADO de forma absoluta (ex.: supressão de blocos de código com atalhos preguiçosos, acesso a diretórios fora do sandbox, alucinação de esquemas).
- **Aplicação**: garante que mesmo modelos menores (Qwen 4B, Ternary 8B) permaneçam estritamente dentro dos trilhos operacionais — barreira contra desvios de lógica. A feature NÃO decide o que pode; o gabarito decide.
- **Sweet spot**: 20–50 linhas por objeto/bloco; máx 150–200 linhas por requisição.

## 3. Mecânica de Ignição, Seleção e Refutação de Motores (.md) — MECÂNICA

- **Função**: infraestrutura de execução acoplando a feature ao modelo correto do catálogo — SEMPRE exercendo criticidade: refutar o catálogo atual quando necessário e propor melhorias de setup.
- **Parâmetros de controle (samplers & setup)**: definição precisa de hiperparâmetros de inferência (temperatura, top_p, top_k, penalidades de repetição) otimizados para o comportamento esperado da feature; ganchos de integração com o backend (Vulkan/llama.cpp) para prefill e decode no limite da eficiência do hardware.
- **LLM especializado**: seleção por catálogo (R75) — sempre refutando o catálogo e propondo melhorias.
- **Sweet spot**: Python 30–60 linhas por bloco (1–2 funções focadas); máx 150–200 linhas por arquivo/prompt.

<Template canônico>
- `skills/_template-feature/` — conceito.md (ontologia) + gabarito.json (firewall) + mecanica.md (ignição). Toda feature criada/helenizada DEVE copiar o template e preencher as 3 camadas ANTES de qualquer código.
- Enforcement: o motor/validador da feature recusa ignição se a mecânica violar o próprio gabarito (deny) — a camada 2 é lei, não sugestão.

<Exemplo canônico (2026-08-30)>
- Refatoração Hefesto: 4 skills atômicas (hefesto-decompilacao, hefesto-autofagia, hefesto-helenizacao, hefesto-forja), cada uma com conceito.md + gabarito.json + mecanica.md + SKILL.md; Hefesto vira dispatcher que invoca a skill certa por fase; material existente helenizado/unificado; órfãos apagados.

---

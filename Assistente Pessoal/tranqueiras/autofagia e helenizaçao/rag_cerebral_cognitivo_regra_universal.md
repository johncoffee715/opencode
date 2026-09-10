---
title: "RAG Cerebral Cognitivo — Arquitetura Universal para Home Lab"
description: "Regra universal para implementação de um ecossistema Obsidian + llama.cpp como RAG cerebral local com Self-Scaffolding, Self-Healing, Self-Learning e Self-Ameliorative."
author: "Agente de Arquitetura — Análise Consolidada"
date: 2026-09-05
tags: [rag, llama.cpp, obsidian, homelab, gbnf, self-healing, self-scaffolding, self-learning, self-ameliorative, opencode, cachyos]
status: arquitetura-validada
version: 2.0
context: "Regra universal para ingestão por agente OpenCode em ecossistema local (llama.cpp + Python puro + Obsidian + CachyOS/Linux)."
---

# RAG Cerebral Cognitivo — Arquitetura Universal para Home Lab

> **Escopo:** Implementação de um ecossistema local (bare-metal) onde o Obsidian atua como interface de um RAG (Retrieval-Augmented Generation) pessoal, orquestrado por scripts Python puros e alimentado por inferência local via llama.cpp. O sistema opera sobre o quarteto técnico `.md 🔄 .py 🔄 .json 🔄 .gbnf`, garantindo determinismo, portabilidade total e zero dependência de APIs comerciais.

---

## 1. Visão de Arquitetura

### 1.1. Princípios Fundamentais

1. **Arquivos como fonte da verdade:** Todo conhecimento reside em `.md` puro. Nenhum banco de dados proprietário.
2. **Determinismo via GBNF:** A gramática GBNF do llama.cpp força o modelo a responder em JSON estrito, eliminando alucinações de formatação.
3. **Separação de responsabilidades:** Obsidian é a camada de apresentação (interface + grafo). A "inteligência" reside nos scripts Python e no llama-server.
4. **Zero frameworks pesados:** Sem LangChain, sem LlamaIndex, sem dependências que mudam de API a cada release. Apenas Python stdlib + bibliotecas leves.
5. **Controle bare-metal:** Todo processo é observável, logável e limitado por cgroups do Linux.

### 1.2. O Quarteto Técnico

```
[Seu Cérebro (.md)] ➡️ [Script (.py)] ➡️ [Filtro (.gbnf)] ➡️ [IA Local (llama.cpp)] ➡️ [Resultado (.json)] ➡️ [Atualiza .md]
```

| Componente | Função | Regra de Ouro |
|---|---|---|
| **`.md`** | Fonte da verdade. Notas em Markdown com YAML Frontmatter. | Nunca armazene JSON no corpo do Markdown. Use YAML Frontmatter para metadados. |
| **`.py`** | Motor de orquestração. Watchdog, filas, validação, I/O. | Scripts puros. Sem frameworks de agentes. `watchdog` para eventos, `requests` para llama-server, `sqlite3` para filas. |
| **`.json`** | Contrato de dados. Structured output da IA e schemas de validação. | GBNF garante sintaxe válida; schema JSON garante semântica válida (tags existem, links existem). |
| **`.gbnf`** | Regulador determinístico. Gramática que restringe o sampler do llama.cpp. | Uma GBNF por tipo de tarefa. Nunca reutilize uma gramática genérica para tarefas diferentes. |

---

## 2. As Quatro Propriedades Cognitivas

> **Nota terminológica:** "Cognitivo" aqui significa "automação inteligente com feedback loop", não consciência artificial. O sistema não pensa; ele executa pipelines de ETL (Extract-Transform-Load) sobre conhecimento humano.

### 2.1. Self-Scaffolding (Autoestruturação)

**Objetivo:** Fazer com que notas novas criem seus próprios andaimes de conexão no vault automaticamente.

**Fluxo Técnico:**

1. **Detecção:** `inotify` do kernel Linux monitora o vault, filtrando apenas `IN_CLOSE_WRITE` em arquivos `.md`.
2. **Debounce:** Eventos são enfileirados em SQLite com timestamp. O processador consome a fila a cada 10-15 segundos, consolidando múltiplos saves da mesma nota em uma única inferência.
3. **Inferência:** Script `.py` extrai o texto da nota e envia para `llama-server` (localhost:8080/completion) acompanhado de uma `.gbnf` específica.
4. **Validação:** O JSON retornado é validado contra:
   - `tag_schema.json` (lista controlada de tags válidas — evita poluição taxonômica)
   - `vault_index.json` (lista de notas existentes — evita links quebrados)
5. **Aplicação:** Se aprovado, o script injeta tags e links bidirecionais no YAML Frontmatter da nota `.md`.

**Exemplo de GBNF para Self-Scaffolding:**

```gbnf
root ::= object
object ::= "{" ws tags ws "," ws links ws "}"
tags ::= ""tags"" ws ":" ws "[" ws tag_list ws "]"
tag_list ::= string | string ws "," ws tag_list
links ::= ""links_sugeridos"" ws ":" ws "[" ws link_list ws "]"
link_list ::= string | string ws "," ws link_list
string ::= """ char* """
char ::= [a-zA-Z0-9_\-àáâãéêíóôõúçÇ ] | "\" escape
escape ::= """ | "\" | "n" | "t"
ws ::= [ 	
]*
```

**Exemplo de Resposta JSON (válida e processável):**

```json
{
  "tags": ["infosec", "devops", "homelab"],
  "links_sugeridos": ["Configuração do Servidor Local", "Containers e Virtualização"]
}
```

**Anti-pattern a evitar:** Nunca gere links para notas que não existem no `vault_index.json`. Um JSON sintaticamente válido pode conter links quebrados. A GBNF resolve sintaxe; a validação pós-inferência resolve semântica.

---

### 2.2. Self-Healing (Autorregeneração)

**Objetivo:** Manter a consistência do vault ao longo do tempo, detectando links órfãos, tags obsoletas e notas desconectadas.

**Fluxo Técnico:**

1. **Agendamento:** `systemd timer` aciona o serviço `vault-healer.service` semanalmente (não diariamente — varrer o vault inteiro é custoso).
2. **Isolamento de recursos:** O service roda com cgroups nativos:
   - `CPUQuota=30%` — nunca monopoliza a CPU
   - `MemoryMax=2G` — hard limit de RAM
   - `MemorySwapMax=0` — evita thrashing de disco
   - `IOWeight=10` — prioridade baixa de I/O
3. **Varredura:** Script `.py` executa:
   - Regex em todos `.md` para extrair `\[\[([^\]]+)\]\]` (links)
   - Comparação com `vault_index.json` para detectar órfãos
   - Análise de conectividade (notas com 0 links de entrada são marcadas como `status: orfao`)
4. **Correção sugerida (não automática):** Para cada inconsistência, o script formula um prompt para o llama.cpp com GBNF de correção. O resultado é um JSON com sugestões.
5. **Aplicação condicional:** O script NÃO aplica correções automaticamente. Ele marca a nota com:
   ```yaml
   ---
   status: revisar_healing
   sugestoes_ia: "..."
   ---
   ```
   A decisão final é humana.

**Anti-pattern a evitar:** NUNCA funda notas automaticamente. Duas notas podem tratar do mesmo termo em contextos completamente diferentes (ex: "Docker" em DevOps vs. "Docker" em Engenharia Naval). A fusão automática é perda de conhecimento disfarçada de eficiência.

---

### 2.3. Self-Learning (Autoaprendizado)

**Objetivo:** Identificar lacunas de conhecimento no vault e expandi-las de forma autônoma.

**Fluxo Técnico:**

1. **Detecção de lacunas:** Script `.py` varre o vault procurando por:
   - Tags: `#pesquisar`, `#incompleto`, `#stub`
   - YAML Frontmatter: `status: incompleto` ou `profundidade: rasa`
   - Marcadores no corpo: `???`, `[?]`, `TODO: pesquisar`
2. **Busca de complementos:**
   - **Local:** Busca semântica via FAISS/ChromaDB em outros documentos do vault (PDFs, manuais, outros `.md`).
   - **Remota (opcional):** Se habilitado, consulta SearXNG local ou DuckDuckGo via `curl`.
3. **Síntese:** O material coletado é enviado ao llama.cpp com uma GBNF de resumo estruturado.
4. **Injeção controlada:** O resultado NÃO é mesclado ao corpo da nota original. São criadas notas-filho ou blocos collapsible com metadado de origem:
   ```markdown
   > [!NOTE]- Expansão Automática (2026-09-05)
   > Conteúdo gerado por IA. Revisar antes de incorporar ao conhecimento principal.
   > ...
   ```

**Anti-pattern a evitar:** Nunca deixe o sistema sobrescrever notas humanas com geração automática. Com o tempo, isso dilui o valor do vault, transformando conhecimento humano curado em lixo gerado por IA.

---

### 2.4. Self-Ameliorative (Auto-aprimoramento Crítico)

**Objetivo:** Revisar periodicamente a qualidade das conexões e a validade dos insights antigos.

**Fluxo Técnico:**

1. **Seleção:** Script seleciona notas antigas (última edição > 6 meses) aleatoriamente, respeitando um rate limit diário (ex: máximo 5 notas por dia).
2. **Avaliação:** O llama.cpp recebe:
   - A nota antiga
   - O esquema conceitual atual do vault (extraído de `tag_schema.json` + nuvem de tags mais frequentes)
   - Uma GBNF que força resposta em JSON com campos: `valido`, `obsoleto`, `sugestao_taxonomia`, `confianca`
3. **Ação:**
   - Se `valido: true` — apenas atualiza `ultima_revisao` no Frontmatter.
   - Se `obsoleto: true` — marca com `status: revisar_obsoleto` e adiciona uma seção de "Contexto Histórico" preservando o insight original.
   - Se `sugestao_taxonomia` — registra no `audit_log.json` para análise humana posterior.

**Anti-pattern a evitar:** Não permita que a IA "refute" seus insights. O modelo não tem acesso ao que você aprendeu depois de escrever a nota. Ele pode invalidar um raciocínio válido apenas porque foi expresso de forma que o modelo não compreendeu. A crítica deve ser um **template de perguntas orientadoras**, não uma reescrita automática.

---

## 3. Refinamentos Técnicos Críticos

### 3.1. Controle de Eventos e I/O (inotify + Debounce)

**Problema:** Obsidian usa auto-save agressivo. Watchdog padrão dispara a cada flush de buffer, gerando dezenas de requisições simultâneas.

**Solução:**

```python
import inotify.adapters
import sqlite3
import time
from threading import Timer

# Fila SQLite persistente
conn = sqlite3.connect('/home/user/vault/meta/event_queue.db')
conn.execute('''CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    filepath TEXT,
    filename TEXT,
    timestamp REAL,
    processed INTEGER DEFAULT 0
)''')

i = inotify.adapters.Inotify()
i.add_watch('/home/user/vault/notas/')

debounce_timers = {}

def process_file(filepath, filename):
    # Consome da fila e dispara inferência
    pass

for event in i.event_gen(yield_nones=False):
    (_, type_names, path, filename) = event
    if 'IN_CLOSE_WRITE' in type_names and filename.endswith('.md'):
        filepath = f"{path}/{filename}"
        # Debounce: cancela timer anterior se houver
        if filepath in debounce_timers:
            debounce_timers[filepath].cancel()
        # Agenda novo processamento em 10s
        t = Timer(10.0, process_file, args=[filepath, filename])
        debounce_timers[filepath] = t
        t.start()
```

**Regra:** Um evento por nota a cada 10s, no máximo. Se o usuário está digitando ativamente, a inferência só ocorre após a pausa de escrita.

---

### 3.2. Indexação e Vetorização

**Decisão arquitetural: FAISS + SQLite (ou ChromaDB embutido)**

| Solução | Status | Justificativa |
|---|---|---|
| **FAISS + SQLite** | ✅ Recomendado | Zero servidores. FAISS para similaridade vetorial, SQLite para metadados e filtros. JOIN em 10.000 linhas é sub-milissegundo. |
| **ChromaDB (embutido)** | ✅ Alternativa válida | Modo `Client(Settings(is_persistent=True))` sem servidor HTTP. Suporta metadata filtering nativo. |
| **Qdrant** | ❌ Rejeitado | Adiciona um servidor HTTP/gRPC completo na stack. Contradiz o princípio de leveza bare-metal. Overkill para vault pessoal (< 10.000 notas). |
| **Numpy puro** | ⚠️ Possível | Para vaults muito pequenos (< 500 notas). Não escala para busca aproximada. |

**Pipeline de indexação:**

1. Extrair texto puro dos `.md` (ignorando YAML Frontmatter).
2. Gerar embeddings via `sentence-transformers` (modelo leve tipo `all-MiniLM-L6-v2`).
3. Armazenar vetores no FAISS (`IndexFlatIP` para precisão exata, `IndexIVFFlat` para vaults > 5.000 notas).
4. Armazenar metadados (path, tags, data) no SQLite com índice FTS5 para busca textual rápida.
5. Reindexar sob demanda (após batch de mudanças) ou semanalmente via systemd timer.

---

### 3.3. Determinismo com GBNF e Escolha de Modelos

**Princípio fundamental:** A aderência à GBNF é uma propriedade do **sampler** do `llama.cpp`, não do modelo.

- Qualquer modelo rodando no `llama-server` com `--grammar-file` ou campo `grammar` no JSON da API vai gerar output sintaticamente válido.
- A escolha do modelo afeta **qualidade semântica** (tags fazem sentido, links são relevantes), não **validade sintática**.

**Estratégia de alocação de modelos:**

| Tarefa | Modelo recomendado | Por quê |
|---|---|---|
| Self-Scaffolding (tags, links) | Modelo pequeno e rápido (2B-7B) | Tarefa simples. Latência importa mais que capacidade. |
| Self-Learning (síntese, expansão) | Modelo médio (7B-14B) | Requer compreensão de contexto mais profunda. |
| Self-Ameliorative (crítica, revisão) | Modelo médio-grande (14B+) | Requer raciocínio mais sofisticado. Roda em background, então latência é menos crítica. |

**Nota sobre "modelos de código":** DeepSeek-Coder ou Qwen-Coder são excelentes para estruturação de dados complexos (ex: extrair entidades aninhadas de código-fonte), mas não têm "maior aderência" à GBNF do que modelos conversacionais. Use-os se a tarefa envolve parsing de código ou estruturas aninhadas profundas; caso contrário, prefira modelos menores e mais rápidos.

---

### 3.4. Agendamento de Manutenção com systemd

**Configuração completa para CachyOS / Arch Linux:**

```ini
; /etc/systemd/system/vault-healer.service
[Unit]
Description=Vault Self-Healing Routine
After=network.target llama-server.service
Wants=llama-server.service

[Service]
Type=oneshot
User=%I
ExecStart=/usr/bin/python3 /home/%I/vault/scripts/healer.py
CPUQuota=30%
MemoryMax=2G
MemorySwapMax=0
IOWeight=10
Nice=10

# Logs estruturados no journal
StandardOutput=journal
StandardError=journal
SyslogIdentifier=vault-healer

[Install]
WantedBy=multi-user.target
```

```ini
; /etc/systemd/system/vault-healer.timer
[Unit]
Description=Run vault healer weekly

[Timer]
OnCalendar=Sun *-*-* 03:00:00
Persistent=true
AccuracySec=1h

[Install]
WantedBy=timers.target
```

```bash
# Ativação
sudo systemctl daemon-reload
sudo systemctl enable --now vault-healer.timer

# Monitoramento
systemctl list-timers --all
journalctl -u vault-healer -f
```

**Vantagens sobre cron:**
- Limitação de recursos via cgroups (`CPUQuota`, `MemoryMax`).
- Dependências declarativas (`After=llama-server.service`).
- Logs estruturados no journal.
- Execução manual sob demanda (`systemctl start vault-healer`).

---

## 4. Arquitetura Revisada — Stack Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    CachyOS / Linux Home Lab                  │
├─────────────────────────────────────────────────────────────┤
│  Camada de Apresentação                                     │
│  ├── Obsidian (interface gráfica + grafo de links)          │
│  └── Plugins: Local REST API, Shell Commands (opcional)     │
├─────────────────────────────────────────────────────────────┤
│  Camada de Conhecimento (Fonte da Verdade)                  │
│  ├── ~/vault/notas/        → Arquivos .md com YAML Frontmatter
│  ├── ~/vault/meta/         → Schemas, índices, logs         │
│  │   ├── tag_schema.json   → Tags controladas (whitelist)   │
│  │   ├── vault_index.json  → Índice de notas existentes     │
│  │   ├── audit_log.json    → Log de todas as alterações IA  │
│  │   └── event_queue.db    → Fila SQLite de eventos         │
│  └── ~/vault/scripts/      → Scripts Python puros           │
├─────────────────────────────────────────────────────────────┤
│  Camada de Orquestração (Python puro)                       │
│  ├── watcher.py            → inotify + debounce + enfileiramento
│  ├── queue_processor.py    → Consome fila SQLite            │
│  ├── inferencer.py         → Cliente HTTP para llama-server │
│  ├── validator.py          → Valida JSON contra schemas     │
│  ├── indexer.py            → FAISS + sentence-transformers  │
│  ├── healer.py             → Rotina de Self-Healing         │
│  └── ameliorator.py        → Rotina de Self-Ameliorative    │
├─────────────────────────────────────────────────────────────┤
│  Camada de IA (llama.cpp)                                   │
│  ├── llama-server          → Servidor de inferência local   │
│  ├── modelos/              → GGUFs (2B, 7B, 14B conforme tarefa)
│  └── grammars/             → Arquivos .gbnf por tarefa      │
├─────────────────────────────────────────────────────────────┤
│  Camada de Sistema (systemd + cgroups v2)                   │
│  ├── vault-healer.service  → Serviço de manutenção          │
│  ├── vault-healer.timer    → Agendamento semanal            │
│  └── vault-indexer.service → Reindexação periódica          │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Schemas de Referência

### 5.1. YAML Frontmatter Padrão

```yaml
---
title: "Título da Nota"
date: 2026-09-05
tags: [tag1, tag2]
links: [[Nota Relacionada A], [Nota Relacionada B]]
status: ativo          # ativo | incompleto | orfao | revisar_healing | revisar_obsoleto
profundidade: media    # rasa | media | profunda
ultima_revisao: 2026-09-05
ia_gerada: false       # true se alguma parte foi gerada por IA
---
```

### 5.2. Schema de Validação de Tags (tag_schema.json)

```json
{
  "tags_validas": [
    "devops", "infosec", "homelab", "docker", "kubernetes",
    "linux", "cachyos", "python", "llama.cpp", "obsidian",
    "redes", "hardware", "automacao", "pesquisar"
  ],
  "sinonimos_proibidos": {
    "dev-ops": "devops",
    "infra": "homelab",
    "k8s": "kubernetes"
  }
}
```

### 5.3. Estrutura do Audit Log (audit_log.json)

```json
{
  "entradas": [
    {
      "timestamp": "2026-09-05T09:30:00-03:00",
      "script": "watcher.py",
      "nota": "notas/docker.md",
      "acao": "inseriu_tags",
      "dados": {"tags": ["devops", "docker"]},
      "modelo": "qwen2.5-7b-instruct",
      "confianca": 0.92
    }
  ]
}
```

---

## 6. Anti-Patterns e Armadilhas

| Anti-Pattern | Por que é perigoso | Solução |
|---|---|---|
| **Fundação automática de notas** | Perda de contexto e conhecimento. | Sempre sugira, nunca funda. Marque para revisão humana. |
| **Injeção de JSON no corpo do Markdown** | Quebra renderização do Obsidian e legibilidade humana. | Use YAML Frontmatter para metadados. |
| **Sobrescrita de notas humanas com IA** | Dilui o valor do vault ao longo do tempo. | Crie notas-filho ou blocos collapsible separados. |
| **Ausência de fila/debounce** | DDoS no próprio llama-server. Burst de inferências simultâneas. | SQLite queue + debounce de 10s + rate limiting. |
| **Ausência de cache** | Reprocessamento idêntico gera custo de inferência desnecessário. | Hash do conteúdo → cache de respostas em SQLite. |
| **Ausência de versionamento** | Scripts com bugs corrompem o vault irreversivelmente. | Git obrigatório. Commits automáticos antes de qualquer alteração em lote. |
| **Ausência de logging** | Impossível auditar o que a IA alterou e por quê. | `audit_log.json` com timestamp, script, nota, ação, modelo e confiança. |
| **Confiar cegamente na semântica do LLM** | O modelo pode inventar tags, links inexistentes, categorizações absurdas. | Validação pós-inferência contra schemas controlados. |
| **Usar modelos grandes para tarefas triviais** | Gasta VRAM e energia sem benefício. | Alocação por tarefa: pequeno para scaffolding, médio para síntese, grande para crítica. |
| **Agendamento sem limites de recurso** | Manutenção em background congela o desktop. | systemd + cgroups (`CPUQuota`, `MemoryMax`, `IOWeight`). |

---

## 7. Checklist de Implementação

### Fase 1 — Fundação (Semana 1)
- [ ] Estruturar diretórios: `~/vault/notas/`, `~/vault/meta/`, `~/vault/scripts/`, `~/vault/grammars/`
- [ ] Inicializar Git no vault com `.gitignore` para `meta/event_queue.db` e caches
- [ ] Criar `tag_schema.json` com taxonomia inicial controlada
- [ ] Criar `vault_index.json` com script de varredura inicial
- [ ] Implementar `watcher.py` com inotify + debounce + fila SQLite
- [ ] Implementar `validator.py` com schemas JSON

### Fase 2 — Motor de IA (Semana 2)
- [ ] Configurar `llama-server` com modelo pequeno (2B-7B) para scaffolding
- [ ] Criar `.gbnf` para Self-Scaffolding
- [ ] Implementar `inferencer.py` (cliente HTTP para llama-server)
- [ ] Implementar `queue_processor.py` (consome fila, chama inferencer, valida, aplica)
- [ ] Testar ciclo completo: criar nota → detectar → inferir → validar → aplicar

### Fase 3 — Indexação (Semana 3)
- [ ] Instalar `sentence-transformers` + `faiss-cpu`
- [ ] Implementar `indexer.py` (extrai texto, gera embeddings, armazena em FAISS + SQLite)
- [ ] Implementar busca híbrida (vetorial + textual)
- [ ] Criar systemd service/timer para reindexação semanal

### Fase 4 — Manutenção (Semana 4)
- [ ] Implementar `healer.py` (detecção de links órfãos, notas desconectadas)
- [ ] Implementar `ameliorator.py` (revisão de notas antigas)
- [ ] Criar `vault-healer.service` e `.timer` com cgroups
- [ ] Criar `audit_log.json` e integrar em todos os scripts
- [ ] Testar carga: criar 50 notas em sequência e observar comportamento da fila

### Fase 5 — Hardening (Semana 5)
- [ ] Implementar cache de inferências (hash do conteúdo → resposta)
- [ ] Implementar rollback automático via Git antes de alterações em lote
- [ ] Adicionar rate limiting no queue_processor (máximo X inferências por minuto)
- [ ] Documentar todas as GBNFs e schemas
- [ ] Criar dashboard simples (script Python + terminal) para visualizar estado do vault

---

## 8. Métricas de Sucesso

| Métrica | Meta | Como Medir |
|---|---|---|
| **Latência de scaffolding** | < 3s por nota | Timestamp na fila vs. timestamp de aplicação |
| **Taxa de links quebrados** | < 1% | Regex de `\[\[[^\]]+\]\]` vs. `vault_index.json` |
| **Taxa de tags inválidas** | 0% | Validação contra `tag_schema.json` |
| **Uso de CPU em manutenção** | < 30% | `systemd-cgtop` durante execução do healer |
| **Uso de RAM em manutenção** | < 2GB | `systemctl status vault-healer` |
| **Tempo de reindexação** | < 5 min para 1.000 notas | Cronometrar `indexer.py` |
| **Taxa de aprovação humana** | > 80% das sugestões de IA | Contagem de `status: revisar_*` resolvidos manualmente |

---

## 9. Notas Finais para o Agente OpenCode

> **Instrução de comportamento:** Este documento é a regra universal de arquitetura. Ao implementar qualquer script ou automação no ecossistema:
> 1. Siga estritamente o quarteto `.md 🔄 .py 🔄 .json 🔄 .gbnf`.
> 2. Nunca substitua validação humana por automação em ações destrutivas (fusão, exclusão, sobrescrita).
> 3. Prefira leveza sobre sofisticação: FAISS > Qdrant, SQLite > PostgreSQL, scripts puros > frameworks.
> 4. GBNF garante sintaxe; schemas JSON garantem semântica. Nunca confie apenas no LLM.
> 5. Todo script deve ser observável (logs), limitável (cgroups) e reversível (Git).

---

*Arquitetura validada e consolidada em 2026-09-05. Revisar a cada 3 meses ou após mudanças significativas na stack técnica.*

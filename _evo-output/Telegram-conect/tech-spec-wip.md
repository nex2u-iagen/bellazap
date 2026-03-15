---
title: 'Integração do Telegram para Gerenciamento de Revendedoras com Agente de IA Orquestrador e Memória por Cliente'
slug: 'telegram-integration-reseller-management-ai-orchestrator-client-memory'
created: '2026-03-15'
status: 'in-progress'
stepsCompleted: [1, 2]
tech_stack: ['Python', 'FastAPI', 'PostgreSQL', 'Redis', 'Celery', 'Langchain', 'python-telegram-bot']
files_to_modify: ['src/domains/telegram/', 'src/models/telegram.py', 'src/api/v1/endpoints/telegram.py', 'src/models/cliente.py', 'src/domains/clientes/', 'src/services/', 'src/core/config.py', 'src/domains/agentes/service.py', 'src/domains/notificacoes/service.py', 'src/workers/', 'docs/revendedoras/<revendedora_id>/clientes/<cliente_id>/conversations.md', 'src/tools/']
code_patterns: ['Modularidade de Domínio', 'Reuso de Serviços Existentes', 'Segurança Baseada em revendedora_id', 'Modelagem de Tools Langchain', 'Agente de IA como Orquestrador', 'Modo de Confirmação Transacional', 'Wizard Conversacional para Clientes', 'Gestão de Estoque Contextual', 'Relatórios Adaptativos', 'Notificações Proativas', 'Gestão de Contexto Conversacional', '"Memória Eterna" por Cliente', 'UI/UX Conversacional']
test_patterns: ['Testes de Unidade', 'Testes de Integração', 'Testes de Segurança', 'Testes de Performance', 'Testes de UX Conversacional']
---

# Tech-Spec: Integração do Telegram para Gerenciamento de Revendedoras com Agente de IA Orquestrador e Memória por Cliente

**Created:** 2026-03-15

## Overview

### Problem Statement

Revendedoras atualmente não possuem uma interface segura e baseada no Telegram para gerenciar suas operações BellaZap (produtos, estoque, vendas e relatórios), e a experiência de atendimento ao cliente carece de um histórico conversacional persistente e contextualmente rico.

### Solution

Desenvolver um bot seguro para Telegram, com um Agente de IA atuando como orquestrador central. Este Agente de IA permitirá às revendedoras gerenciar todo o seu fluxo de trabalho BellaZap (cadastro de produtos, atualizações de estoque, registro de vendas e geração/visualização de relatórios) através da vinculação do seu ID do Telegram à sua conta de revendedora existente. Adicionalmente, o sistema manterá uma "memória eterna" por cliente, persistindo resumos das interações em arquivos .md para um histórico rico e personalizado.

### Scope

**In Scope:**
-   Conexão segura utilizando o ID do usuário do Telegram, vinculado a uma conta de revendedora existente.
-   **Agente de IA como Orquestrador Central**: Interpretação de linguagem natural para invocar `Tools` do backend.
-   **Funcionalidades completas de gerenciamento via Telegram, orquestradas pelo Agente de IA**:
    -   Registro de vendas (com confirmação transacional para ações críticas).
    -   Gestão de estoque (com extração inteligente e confirmação condicional).
    -   Cadastro e Gestão de clientes (com fluxo "wizard" e filtros por `revendedora_id`).
    -   Geração e visualização de relatórios (resumos no chat, PDFs/planilhas via link para complexos).
-   **Memória de Conversas por Cliente**: Persistência de resumos de atendimentos em arquivos .md por cliente.
-   Notificações proativas e gerenciáveis via Telegram.
-   UI/UX conversacional otimizada para dispositivos móveis (botões, concisão, progresso).

**Out of Scope:**
-   Qualquer outra integração com plataformas de mensagens (foco exclusivo no Telegram).
-   Análises avançadas ou UI complexa diretamente dentro do Telegram (foco nas ações de gerenciamento essenciais e conversacionais).
-   Desenvolvimento de novas ferramentas ou LLMs para além da integração e orquestração.

## Context for Development

### Codebase Patterns

-   **Modularidade de Domínio**: Manter a estrutura atual de `src/domains/` para encapsular a lógica de negócio do Telegram, clientes, e extensão de serviços existentes.
-   **Reuso de Serviços Existentes**: `PaymentService`, `ProductService`, `NotificationService` serão reutilizados e expostos como `Tools` para o Agente de IA.
-   **Segurança Baseada em `revendedora_id`**: Todas as operações de dados devem incluir o `revendedora_id` como filtro para garantir segregação e privacidade.
-   **Modelagem de `Tools` Langchain**: As `Tools` para o Agente de IA devem ter descrições claras e schemas Pydantic robustos para validação de `inputs`.

### Files to Reference / Modify / Create

| File/Directory                  | Purpose                                                                                                 | Status    |
| :------------------------------ | :------------------------------------------------------------------------------------------------------ | :-------- |
| `src/domains/telegram/`         | Novo domínio para encapsular a lógica de interface com a API do Telegram (webhooks, envio de mensagens). | **CREATE**|
| `src/models/telegram.py`        | Modelos para dados específicos do Telegram (e.g., `TelegramUser`, `TelegramChatState`).                 | **CREATE**|
| `src/api/v1/endpoints/telegram.py`| Novo endpoint para webhooks do Telegram e comunicação do bot.                                          | **CREATE**|
| `src/models/cliente.py`         | Novo modelo `Cliente` com `revendedora_id` como `ForeignKey`.                                          | **CREATE**|
| `src/domains/clientes/`         | Novo domínio para gestão da lógica de clientes.                                                        | **CREATE**|
| `src/services/`                 | `ClientService` para CRUD de clientes.                                                                  | **CREATE**|
| `src/core/config.py`            | Adicionar chaves de API do Telegram (e.g., `TELEGRAM_BOT_TOKEN`), etc.                                 | MODIFY    |
| `src/domains/agentes/service.py`| Adaptar para incluir as novas `Tools` e lógica de orquestração do `BellaAgent` para o Telegram.        | MODIFY    |
| `src/domains/notificacoes/service.py`| Estender para enviar notificações para o Telegram.                                                    | MODIFY    |
| `src/workers/`                  | Adaptar ou criar novos workers para proatividade via Telegram.                                         | MODIFY    |
| `docs/revendedoras/<revendedora_id>/clientes/<cliente_id>/conversations.md` | Estrutura para a "memória eterna" das conversas por cliente.                               | **CREATE**|
| `src/tools/`                    | Diretório para novas `Tools` a serem expostas ao Agente de IA (e.g., `ProductSearchTool`, `ClientManagementTool`, `SummarizeAndPersistConversationTool`). | **CREATE**|

### Technical Decisions

1.  **Agente de IA como Orquestrador:** O `BellaAgent` será o ponto de entrada conversacional. Ele interpretará a intenção da revendedora usando LLMs e invocará `Tools` apropriadas.
2.  **Segurança e Vinculação de ID:** Autenticação inicial do `Telegram_user_id` com o `Revendedora_id` existente (via fluxo de OAuth simplificado ou token de uso único por e-mail/WhatsApp). Todas as ações subsequentes serão autenticadas e filtradas por `revendedora_id`.
3.  **Modo de Confirmação Transacional:** Para ações críticas (registro de venda, atualização de estoque), o Agente de IA apresentará um resumo dos dados extraídos e exigirá uma confirmação explícita ("Sim/Não") da revendedora antes da execução da `Tool`.
4.  **Wizard Conversacional para Clientes:** Para cadastro e edição de clientes, o Agente de IA guiará a revendedora com perguntas sequenciais curtas, validando entradas e aproveitando o contexto.
5.  **Gestão de Estoque Contextual:** O Agente de IA usará extração robusta de entidades para `ação`, `quantidade` e `produto`. Uma `ProductSearchTool` dedicada será usada para acesso eficiente ao catálogo.
6.  **Relatórios Adaptativos:** Relatórios simples no chat; relatórios complexos via links temporários para PDFs/planilhas gerados sob demanda.
7.  **Notificações Proativas:** Utilizar `Celery Workers` e `NotificationService` estendido para alertas configuráveis. Revendedoras gerenciarão suas preferências de notificação.
8.  **Gestão de Contexto Conversacional:** Persistência do histórico da conversa e do `conversation_state` (ligado a `revendedora_id` e `Telegram_user_id`), permitindo sessões longas e retomada. `Tools` devem ser reentrantes e cônscias do estado.
9.  **"Memória Eterna" por Cliente:** Ao final de cada atendimento via Agente de IA, um resumo de um parágrafo da interação será gerado (via `SummarizeAndPersistConversationTool`) e salvo em arquivos `.md` específicos por cliente. Uma `tool` "Consultar Histórico de Cliente" permitirá ao Agente de IA acessar essas memórias.
10. **UI/UX Conversacional:** Uso extensivo de botões inline/teclados personalizados para ações comuns. Mensagens concisas, uso de emojis, listas para dados, e indicação de progresso para fluxos "wizard".

## Implementation Plan

### Tasks

1.  **Configuração do Ambiente:**
    *   Adicionar `TELEGRAM_BOT_TOKEN` e outras configurações relevantes em `src/core/config.py`.
    *   Instalar dependências Python para interação com a API do Telegram (e.g., `python-telegram-bot`).
2.  **Desenvolvimento do Domínio Telegram:**
    *   Criar `src/domains/telegram/service.py` para abstrair a API do Telegram (envio/recebimento de mensagens, gerenciamento de bot).
    *   Criar `src/models/telegram.py` com modelos para `TelegramUser` (vinculado a `Revendedora`), `TelegramChatState` (para contexto conversacional).
    *   Implementar `src/api/v1/endpoints/telegram.py` para receber webhooks do Telegram e rotear para o Agente de IA.
3.  **Desenvolvimento do Domínio Cliente e Memória:**
    *   Criar `src/models/cliente.py` com `Cliente` (incluindo `revendedora_id`).
    *   Criar `src/domains/clientes/` e `ClientService` para CRUD de clientes.
    *   Implementar `SummarizeAndPersistConversationTool` para gerar e salvar resumos em `.md`.
    *   Implementar `ClientConversationMemoryService` para gerenciar a leitura e escrita dos arquivos `.md` por cliente.
4.  **Extensão do Agente de IA:**
    *   Atualizar `src/domains/agentes/service.py` para:
        *   Instanciar o `BellaAgent` com as novas `Tools`.
        *   Incluir lógica de pré-processamento para autenticar `Telegram_user_id` e injetar `revendedora_id`.
        *   Implementar o "modo de confirmação transacional".
        *   Gerenciar o `conversation_state` via `TelegramChatState`.
    *   Desenvolver `Tools` específicas para o Agente de IA:
        *   `RegisterSaleTool` (interface com `PaymentService`).
        *   `ManageStockTool` (interface com `ProductService`).
        *   `ClientManagementTool` (interface com `ClientService`, incluindo "wizard").
        *   `GenerateReportTool`.
        *   `ProductSearchTool`.
        *   `ConsultClientHistoryTool` (para a "memória eterna").
        *   `ManageAlertsTool` (interface com `NotificationService`).
5.  **Extensão de Notificações e Proatividade:**
    *   Atualizar `src/domains/notificacoes/service.py` para suportar o envio de mensagens para o Telegram.
    *   Adaptar `src/workers/` para acionar notificações proativas via Telegram com base em gatilhos.
6.  **UI/UX Conversacional:**
    *   Integrar uso de botões inline e teclados personalizados na interação via `src/domains/telegram/service.py`.

### Acceptance Criteria

1.  **Vinculação Segura:**
    *   **Dado** que uma revendedora nunca usou o bot do Telegram,
    *   **Quando** ela tenta usar uma funcionalidade que requer autenticação,
    *   **Então** o bot a guiará por um processo seguro para vincular seu `Telegram_user_id` a uma `Revendedora` existente.
2.  **Registro de Nova Venda:**
    *   **Dado** que uma revendedora inicia o fluxo de registro de venda,
    *   **Quando** ela fornece os detalhes da venda em linguagem natural,
    *   **Então** o Agente de IA extrai os parâmetros, apresenta um resumo e solicita confirmação explícita antes de registrar a venda via `PaymentService`.
3.  **Gestão de Estoque:**
    *   **Dado** que uma revendedora solicita uma atualização de estoque para um produto,
    *   **Quando** ela fornece a ação (adicionar/reduzir) e a quantidade,
    *   **Então** o Agente de IA extrai os detalhes, usa a `ManageStockTool` e confirma a atualização, solicitando confirmação explícita para grandes alterações.
4.  **Cadastro e Consulta de Clientes:**
    *   **Dado** que uma revendedora solicita o cadastro de um novo cliente,
    *   **Quando** o Agente de IA a guia passo a passo para coletar os dados,
    *   **Então** o cliente é salvo com o `revendedora_id` associado.
    *   **Dado** que uma revendedora consulta um cliente existente,
    *   **Quando** o Agente de IA busca pelo nome ou ID,
    *   **Então** as informações do cliente são apresentadas de forma concisa.
5.  **Geração de Relatórios:**
    *   **Dado** que uma revendedora solicita um relatório de vendas do mês,
    *   **Quando** o Agente de IA processa a solicitação,
    *   **Então** um resumo textual é apresentado no chat, e um link para um PDF/planilha detalhada é fornecido.
6.  **"Memória Eterna" por Cliente:**
    *   **Dado** que uma interação significativa com o Agente de IA para um cliente é concluída,
    *   **Quando** o atendimento é finalizado,
    *   **Então** um resumo de um parágrafo da conversa é gerado e anexado ao arquivo `.md` de memória do cliente.
    *   **Dado** que o Agente de IA interage com um cliente existente,
    *   **Quando** ele consulta o histórico do cliente via `ConsultClientHistoryTool`,
    *   **Então** o Agente de IA pode usar essas informações para um atendimento contextualizado.
7.  **Notificações Proativas:**
    *   **Dado** que um gatilho de "estoque baixo" é configurado e ativado,
    *   **Quando** o `Celery Worker` processa o evento,
    *   **Então** o `NotificationService` envia uma mensagem proativa para o Telegram da revendedora associada.

## Additional Context

### Dependencies

-   **Python-Telegram-Bot**: Biblioteca Python para interagir com a API do Telegram.
-   Atualização para `langchain` e `langchain-openai` para garantir suporte às novas `Tools` e funcionalidades do Agente de IA.
-   Potencialmente um sistema de armazenamento de arquivos para os `.md` da memória de conversas (e.g., armazenamento local simples ou integração com um blob storage como S3).

### Testing Strategy

-   **Testes de Unidade:** Para os novos domínios (`telegram`, `clientes`) e serviços (`TelegramService`, `ClientService`, `ClientConversationMemoryService`).
-   **Testes de Integração:** Para a orquestração do Agente de IA (integração entre Agente, `Tools` e serviços de backend), garantindo que as intenções sejam corretamente interpretadas e as ações executadas.
-   **Testes de Segurança:** Foco especial na vinculação de `Telegram_user_id` a `Revendedora_id` e na segregação de dados.
-   **Testes de Performance:** Avaliar a latência das interações do Agente de IA, especialmente com chamadas a LLMs e busca/persistência de memória de conversas.
-   **Testes de UX Conversacional:** Testes manuais para avaliar a clareza, concisão e fluxo das interações do bot no Telegram.

### Notes

-   A arquitetura deve ser desenhada para permitir a fácil adição de novas `Tools` ao Agente de IA no futuro.
-   Considerar a monitoração do uso de tokens do LLM e dos custos associados à medida que a funcionalidade escalar.
-   Explorar o uso de **Markdown no Telegram** para formatação de mensagens complexas (ex: relatórios).

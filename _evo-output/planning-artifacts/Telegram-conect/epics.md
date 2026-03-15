---
stepsCompleted: [1]
inputDocuments:
  - _evo-output/Telegram-conect/tech-spec-wip.md
  - _evo-output/planning-artifacts/Telegram-conect/architecture.md
  - docs/ui-component-inventory-frontend.md
workflowType: 'epics-and-stories'
project_name: 'BellaZap'
user_name: 'Eliezer'
date: '2026-03-15T15:37:00-03:00'
active_feature: 'Telegram-conect'
---

# BellaZap - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for BellaZap, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Gestão de representantes e planos (taxas fixas + variáveis) com aplicação em novas vendas.
FR2: Shadow Login (Impersonate) para suporte, com restrição de escrita em operações financeiras críticas.
FR3: Registro de vendas via IA (NLP) com fluxo de confirmação transacional (Sim/Não) obrigatório.
FR4: Estoque individual vinculado ao catálogo global, incluindo motor de sugestão de substitutos.
FR5: Split automático via PIX Asaas com retenção de comissão da plataforma na fonte.
FR6: Dashboard de inadimplência proativo com notificações automatizadas via Telegram/Web.

### NonFunctional Requirements

NFR1: Respostas da IA e funções backend devem respeitar o limite de 10s da Vercel (SLA interno de 3s para intenção).
NFR2: Isolamento total de dados entre representantes através do revendedora_id mandatório em nível de banco (Turso).
NFR3: Arquitetura 100% stateless compatível com o plano free da Vercel, sem diretórios locais.
NFR4: Interface conversacional otimizada (Wizard) para dispositivos móveis via Telegram com botões de ação rápida.

### Additional Requirements

- **Starter Template**: Estrutura serverless otimizada para borda.
- **Integração FinTech**: API Asaas para PIX dinâmico e Split de Pagamentos automático.
- **Estado Efêmero**: Persistência de estado de conversa entre acionamentos de Webhooks.

### FR Coverage Map

FR1: Epic 1 - Gestão de Planos e Representantes
FR2: Epic 4 - Suporte via Shadow Login (View-Only)
FR3: Epic 4 - Registro de Vendas via NLP com IA
FR4: Epic 3 - Estoque Individualizado vs Global
FR5: Epic 2 - Automação de Split e PIX Asaas
FR6: Epic 4 - Notificações de Inadimplência

## Epic List

### Epic 1: Gestão de Infraestrutura & Base Administrativa
Estabelecer a fundação "Serverless" na Vercel com Turso e o controle mestre de representantes e planos.
**FRs covered:** FR1, NFR1, NFR2, NFR3.

#### Story 1.1: Inicialização do Ambiente Serverless (Turso + Vercel)
As a desenvolvedor,
I want configurar a conexão com o banco de dados Turso no backend FastAPI,
So that possamos armazenar dados de forma persistente e escalável na borda da Vercel.

**Acceptance Criteria:**
- **Given** as credenciais do Turso (URL e Token),
- **When** o backend inicializa em ambiente de produção (Vercel),
- **Then** a conexão com o banco de dados é estabelecida com sucesso usando `libsql-client-python`.
- **And** um teste de "ping" é realizado e, em caso de falha, um log de erro estruturado é gerado (Fail-Fast).

#### Story 1.2: CRUD de Planos e Taxas com Validação Integrada
As a Super Admin,
I want criar e gerenciar planos com suas respectivas taxas de comissão,
So that a plataforma possa cobrar valores diferenciados por representante de forma segura.

**Acceptance Criteria:**
- **Given** o formulário de criação de plano,
- **When** eu tento salvar um plano com taxas negativas ou superiores a 100%,
- **Then** o sistema deve rejeitar o salvamento e retornar erro: "Taxas fora do intervalo permitido".
- **And** alterações em taxas devem gerar um registro de histórico (Audit Trail) vinculado ao usuário administrativo.

#### Story 1.3: Gestão de Representantes e Isolamento de Dados (Tenant Setup)
As a Super Admin,
I want cadastrar novas representantes vinculando-as a um plano e gerando um ID de isolamento,
So that cada usuária tenha seus dados protegidos e sua cobrança configurada.

**Acceptance Criteria:**
- **Given** os dados de uma nova representante (Nome, E-mail, CPF/CNPJ),
- **When** o registro é criado no Turso,
- **Then** o sistema deve gerar um UUID único para `revendedora_id` e garantir a unicidade de CPF/E-mail.
- **And** a representante deve ser associada obrigatoriamente a um `plano_id` válido.

### Epic 2: Automação Financeira & Split Asaas
Integração completa com Asaas para split de pagamento automático e liquidação via PIX.
**FRs covered:** FR5.

#### Story 2.1: Integração com API Asaas para PIX Dinâmico
As a representante, I want gerar um QR Code PIX para minha cliente no momento da venda, So that eu possa receber o pagamento de forma instantânea e segura.

**Acceptance Criteria:**
- **Given** uma ordem de venda criada no sistema,
- **When** o sistema solicita o pagamento à API do Asaas,
- **Then** deve gerar uma cobrança PIX e retornar o QR Code e a chave copia-e-cola.
- **And** em caso de erro na API do Asaas, o sistema deve realizar até 3 tentativas automáticas antes de notificar a falha.

#### Story 2.2: Lógica de Split de Comissão na Fonte
As a plataforma BellaZap, I want configurar o split automático entre minha comissão e o valor da representante, So that a rentabilidade seja garantida na liquidação.

**Acceptance Criteria:**
- **Given** uma venda em processamento para uma representante com plano ativo,
- **When** o payload do PIX é enviado ao Asaas,
- **Then** o parâmetro `split` deve ser preenchido com os percentuais/valores exatos do plano vinculado.
- **And** o sistema deve validar se a soma dos splits não excede 100% do valor bruto para evitar erros de cálculo financeiro.

#### Story 2.3: Webhook de Confirmação Idempotente
As a sistema, I want processar confirmações de pagamento via Webhook, So that a baixa financeira seja automática e confiável.

**Acceptance Criteria:**
- **Given** um Webhook autenticado recebido do Asaas,
- **When** o evento for `PAYMENT_CONFIRMED`,
- **Then** o status da venda deve ser atualizado para "Paga" no Turso.
- **And** o sistema deve ignorar mensagens duplicadas (idempotência) para evitar registros financeiros repetidos.

### Epic 3: Operação de Inventário & Catálogo Digital
Gestão de estoque individualizada por revendedora vinculada ao Catálogo Global.
**FRs covered:** FR4.

#### Story 3.1: CRUD de Catálogo Global (Super Admin)
As a Super Admin, I want gerenciar o catálogo centralizado de produtos, So that todas as representantes usem as mesmas fotos e descrições oficiais.

**Acceptance Criteria:**
- **Given** o painel Super Admin,
- **When** eu crio ou edito um produto no Catálogo Global,
- **Then** as alterações devem ser refletidas instantaneamente para todas as representantes que possuem esse item.
- **And** deve ser gerado um `global_product_id` único para rastreabilidade cross-tenant.

#### Story 3.2: Gestão de Estoque Individual e Alerta de Ruptura
As a representante, I want definir as quantidades que possuo de cada produto global, So that eu não venda itens que não tenho fisicamente.

**Acceptance Criteria:**
- **Given** um produto do catálogo global,
- **When** eu defino a quantidade em meu estoque local,
- **Then** o sistema deve salvar esse saldo vinculado ao meu `revendedora_id`.
- **And** se uma venda for tentada com estoque zero, o Bot deve sugerir automaticamente um produto substituto do catálogo global.

### Epic 4: Motor de Vendas IA & Interface Conversacional
Bot de Telegram com IA orquestradora para vendas, Shadow Login e gestão de cobrança.
**FRs covered:** FR2, FR3, FR6, NFR4.

#### Story 4.1: Registro de Vendas via IA (NLP) com Confirmação
As a representante, I want ditar ou digitar uma venda para a IA, So that o registro seja rápido e sem preenchimento de formulários longos.

**Acceptance Criteria:**
- **Given** uma mensagem de chat no Telegram (ex: "vendi 2 perfumes X para Maria"),
- **When** a IA processa a intenção e extrai os dados,
- **Then** o Bot deve apresentar um botão de "CONFIRMAR" com o resumo da venda antes de gerar o PIX.
- **And** o processamento da intenção não deve exceder o SLA interno de 3 segundos.

#### Story 4.2: Shadow Login (Impersonate View-Only)
As a Super Admin, I want visualizar o painel exatamente como a representante vê, So that eu possa prestar suporte eficiente.

**Acceptance Criteria:**
- **Given** o ID de uma representante no painel Admin,
- **When** eu aciono o modo "Assumir Perfil",
- **Then** o sistema gera um token temporário com permissões `READ_ONLY`.
- **And** qualquer tentativa de alteração financeira ou saque em modo Shadow deve ser bloqueada e logada como tentativa de violação.

#### Story 4.3: Notificações Pró-ativas de Inadimplência
As a sistema, I want monitorar parcelas vencidas e enviar alertas automáticos, So that a saúde financeira da representante seja preservada.

**Acceptance Criteria:**
- **Given** uma transação com pagamento atrasado,
- **When** o script de rotina detecta o atraso (via Webhook Asaas ou Cron),
- **Then** o Bot deve enviar uma mensagem de alerta para a representante e o Admin.
- **And** a mensagem deve conter um link direto para a renegociação ou novo QR Code PIX.

#### Story 4.4: Memória "Eterna" por Cliente (Markdown Persistence)
As a Agente de IA, I want persistir resumos de interações em arquivos Markdown, So that eu possa manter o contexto histórico e preferências de cada cliente indefinidamente.

**Acceptance Criteria:**
- **Given** uma conversa encerrada ou um marco transacional atingido,
- **When** o orquestrador processa o fechamento do contexto,
- **Then** deve gerar/atualizar um arquivo `.md` no diretório de memórias do cliente.
- **And** o arquivo deve conter: data, resumo da transação, preferências detectadas e "sentimento" da cliente.
- **And** o sistema deve realizar a leitura desse arquivo como contexto inicial na próxima interação.

#### Story 4.5: CRM Conversacional (Gestão de Clientes via Wizard)
As a representante, I want cadastrar e editar dados de clientes através de conversas simples, So that minha base de contatos esteja sempre atualizada sem esforço manual.

**Acceptance Criteria:**
- **Given** o comando de cadastro ou identificação de nova cliente pela IA,
- **When** o Bot inicia o fluxo de registro,
- **Then** deve utilizar botões inline e perguntas guiadas (Wizard) para coletar Nome, Telefone e Endereço.
- **And** a IA deve validar se os dados seguem o formato correto (Regex para telefone/CEP) antes de persistir no Turso.

#### Story 4.6: Relatórios Adaptativos (Chat + Links Externos)
As a representante, I want visualizar o desempenho das minhas vendas de forma resumida no chat, So that eu possa tomar decisões rápidas sem sair do Telegram.

**Acceptance Criteria:**
- **Given** a solicitação de um relatório (ex: "quanto vendi hoje?"),
- **When** o sistema processa os dados no Turso,
- **Then** deve retornar um resumo textual elegante no chat (Markdown formatado).
- **And** para visões complexas (ex: extrato mensal), deve gerar um link temporário seguro para visualização Web ou download de PDF.

# Backend Data Models

This document outlines the database schema and data models for the backend part of the application. The models are defined using SQLAlchemy ORM.

## Core Models (`src/models/core.py`)

### `Revendedora`
Represents a reseller in the system.

- **id**: UUID, Primary Key
- **nome**: String
- **email**: String, Unique
- **cpf_cnpj**: String, Unique
- **telefone**: String
- **whatsapp_instance**: String (Instance name in Evolution API)
- **whatsapp_status**: String (e.g., "disconnected")
- **data_cadastro**: DateTime
- **is_active**: Boolean
- **plano**: String (e.g., BASIC)
- **Relationships**: `wallets`, `transacoes`, `vendas`, `estoque`, `saques`

### `Venda`
Represents a sale made by a reseller.

- **id**: UUID, Primary Key
- **revendedora_id**: UUID, Foreign Key to `revendedoras`
- **valor_total**: DECIMAL
- **status**: String (e.g., "pending")
- **data_criacao**: DateTime
- **data_atualizacao**: DateTime
- **metadata_**: JSON
- **Relationships**: `revendedora`, `transacoes`

### `Produto`
Represents a global product in the catalog.

- **id**: UUID, Primary Key
- **codigo**: String, Unique (SKU)
- **nome**: String
- **descricao**: Text
- **categoria**: String
- **preco_sugerido**: DECIMAL
- **Relationships**: `estoques`

### `RevendedoraEstoque`
Represents the individual stock of a product for a specific reseller.

- **id**: UUID, Primary Key
- **revendedora_id**: UUID, Foreign Key to `revendedoras`
- **produto_id**: UUID, Foreign Key to `produtos`
- **quantidade**: Integer
- **preco_personalizado**: DECIMAL
- **Relationships**: `revendedora`, `produto`

### `AgentConfig`
Stores configurations for AI Agents.

- **id**: UUID, Primary Key
- **nome**: String (e.g., "Bella Suporte")
- **departamento**: String (e.g., "suporte")
- **prompt_contexto**: Text
- **api_key_openai**: String
- **model_name**: String
- **is_active**: Boolean
- **metadata_**: JSON

### `MessageLog`
Logs conversations for auditing and AI analysis.

- **id**: UUID, Primary Key
- **revendedora_id**: UUID, Foreign Key to `revendedoras`
- **role**: String (e.g., "user", "assistant")
- **content**: Text
- **model_used**: String
- **timestamp**: DateTime
- **intent**: String
- **Relationships**: `revendedora`

### `SystemConfiguration`
Stores global system configurations.

- **id**: UUID, Primary Key
- **key**: String, Unique
- **value**: Text
- **description**: String
- **updated_at**: DateTime
- **category**: String

## Payment Models (`src/models/payment.py`)

### `PaymentProvider`
Represents a payment provider (e.g., Asaas).

- **id**: UUID, Primary Key
- **name**: String, Unique
- **is_active**: Boolean
- **priority**: Integer
- **config**: JSON
- **created_at**: DateTime
- **Relationships**: `wallets`, `transactions`, `webhook_failures`

### `RevendedoraWallet`
Represents a reseller's digital wallet with a specific provider.

- **id**: UUID, Primary Key
- **revendedora_id**: UUID, Foreign Key to `revendedoras`
- **provider_id**: UUID, Foreign Key to `payment_providers`
- **wallet_id**: Text
- **is_active**: Boolean
- **created_at**: DateTime
- **Relationships**: `provider`, `revendedora`

### `Transaction`
Represents a financial transaction.

- **id**: UUID, Primary Key
- **revendedora_id**: UUID, Foreign Key to `revendedoras`
- **venda_id**: UUID, Foreign Key to `vendas`
- **provider_id**: UUID, Foreign Key to `payment_providers`
- **provider_payment_id**: Text
- **valor_bruto**: DECIMAL
- **taxa_plataforma**: DECIMAL
- **taxa_provider**: DECIMAL
- **valor_liquido_revendedora**: DECIMAL
- **split_config**: JSON
- **status**: String
- **webhook_recebido**: Boolean
- **webhook_retries**: Integer
- **created_at**: DateTime
- **confirmed_at**: DateTime
- **failed_at**: DateTime
- **Relationships**: `provider`, `revendedora`, `venda`

### `WebhookFailure`
A dead-letter queue for failed webhooks.

- **id**: UUID, Primary Key
- **provider_id**: UUID, Foreign Key to `payment_providers`
- **payload**: JSON
- **error**: Text
- **attempts**: Integer
- **last_attempt**: DateTime
- **status**: String
- **created_at**: DateTime
- **Relationships**: `provider`

### `Withdraw`
Represents a withdrawal request from a reseller.

- **id**: UUID, Primary Key
- **revendedora_id**: UUID, Foreign Key to `revendedoras`
- **valor**: DECIMAL
- **status**: String
- **pix_key**: String
- **created_at**: DateTime
- **processed_at**: DateTime
- **metadata_**: JSON
- **Relationships**: `revendedora`

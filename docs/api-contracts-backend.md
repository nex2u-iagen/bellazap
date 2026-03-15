# Backend API Contracts

This document details the API endpoints provided by the backend application, organized by their respective modules.

## `src/api/v1/endpoints/payments.py`

### `POST /v1/payments/`
**Description:** Creates a new payment with automatic provider fallback and split rules.
**Status Code:** `201 Created`
**Request Body:** `PaymentCreate` (customer_data, amount, split_rules, revendedora_id, venda_id)
**Response Body:** `PaymentResponse` (id, provider_name, provider_payment_id, status, amount, created_at)

## `src/api/v1/endpoints/admin.py`

### `GET /v1/admin/stats`
**Description:** Returns real-time global statistics for the admin dashboard.
**Response Body:** `AdminStats` (total_revendedoras, vendas_mensais, mrr, saques_pendentes, llm_status)

### `GET /v1/admin/revendedoras`
**Description:** Lists all resellers.
**Response Body:** `List[RevendedoraResponse]` (id, nome, telefone, plano, is_active)

### `POST /v1/admin/revendedoras`
**Description:** Manually creates a new reseller.
**Request Body:** `RevendedoraCreate` (nome, email, cpf_cnpj, telefone, plano)
**Response Body:** `RevendedoraResponse`

### `GET /v1/admin/configs`
**Description:** Lists all system configurations.
**Response Body:** `List[ConfigResponse]` (key, value, category)

### `POST /v1/admin/configs`
**Description:** Updates an existing system configuration or creates a new one if it doesn't exist.
**Request Body:** `ConfigUpdate` (key, value, category)
**Response Body:** `ConfigResponse`

### `POST /v1/admin/infra/evo/test`
**Description:** Tests connectivity with the Evolution API using saved configurations.
**Response Body:** `Dict` (status, message)

### `POST /v1/admin/infra/db/maintenance`
**Description:** Executes database maintenance tasks (e.g., simulates cache cleanup).
**Response Body:** `Dict` (status, message)

### `POST /v1/admin/produtos/import`
**Description:** Imports products from a CSV file.
**Request Body:** `UploadFile` (CSV file)
**Response Body:** `Dict` (message)

### `GET /v1/admin/financial/predictive`
**Description:** Generates predictive insights based on real database data.
**Response Body:** `Dict` (insights, top_performers)

### `GET /v1/admin/help/{topic}`
**Description:** Returns Markdown-formatted administration guides.
**Parameters:** `topic` (string)
**Response Body:** `Dict` (content)

### `GET /v1/admin/agents`
**Description:** Lists all AI agent configurations.
**Response Body:** `List[AgentConfigResponse]` (id, nome, departamento, model_name, is_active, prompt_contexto)

### `POST /v1/admin/agents`
**Description:** Creates a new AI agent configuration.
**Request Body:** `AgentConfigCreate` (nome, departamento, prompt_contexto, model_name, is_active)
**Response Body:** `AgentConfigResponse`

### `PUT /v1/admin/agents/{id}`
**Description:** Updates an existing AI agent configuration.
**Parameters:** `id` (UUID)
**Request Body:** `AgentConfigCreate`
**Response Body:** `AgentConfigResponse`

### `DELETE /v1/admin/agents/{id}`
**Description:** Deletes an AI agent.
**Parameters:** `id` (UUID)
**Response Body:** `Dict` (message)

### `GET /v1/admin/agents/logs`
**Description:** Lists AI agent message logs.
**Parameters:** `limit` (integer, default 20)
**Response Body:** `List[MessageLogResponse]` (id, role, content, model_used, timestamp, intent)

<h2>`src/api/v1/endpoints/agents.py`</h2>

<h3>`POST /v1/agents/chat`</h3>
<b>Description:</b> Interacts with the "Bella Agent" AI.
<b>Request Body:</b> `ChatRequest` (revendedora_id, message, history)
<b>Response Body:</b> `Dict` (response)

<h2>`src/api/v1/endpoints/whatsapp.py`</h2>

<h3>`POST /v1/whatsapp/webhook`</h3>
<b>Description:</b> Receives events from the Evolution API (messages, status, connections).
<b>Request Body:</b> `Request` (JSON payload)
<b>Response Body:</b> `Dict` (status)

<h3>`POST /v1/whatsapp/instance/create`</h3>
<b>Description:</b> Creates a new WhatsApp instance.
<b>Parameters:</b> `instance_name` (string)
<b>Response Body:</b> `Dict` (with details from whatsapp_service)

<h3>`GET /v1/whatsapp/instance/qrcode/{instance_name}`</h3>
<b>Description:</b> Fetches the QR Code for WhatsApp connection.
<b>Parameters:</b> `instance_name` (string)
<b>Response Body:</b> `Dict` (with QR code data or error)

<h3>`POST /v1/whatsapp/send`</h3>
<b>Description:</b> Sends a WhatsApp message.
<b>Parameters:</b> `instance_name` (string), `number` (string), `message` (string)
<b>Response Body:</b> `Dict` (with details from whatsapp_service)

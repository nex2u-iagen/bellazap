# Guia Evolution API (WhatsApp)

A Evolution API é o motor que conecta a BellaZap ao WhatsApp das revendedoras.

## Configuração de Instância
1. **URL Base:** A URL onde sua Evolution API está rodando (Ex: `https://api.bellazap.com.br`).
2. **Global API Key:** A chave mestra definida no seu `env` da Evolution.

## Webhooks
A BellaZap precisa receber eventos da Evolution. Certifique-se de que a Evolution está apontando para:
`https://seu-backend.com/api/v1/telegram/webhook` (ou o endpoint configurado).

## Status da Conexão
Use o botão "Testar Conexão" no painel de ajustes para validar se as credenciais estão corretas.

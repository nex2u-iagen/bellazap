# Configuração da Evolution API

A Evolution API é o coração da comunicação do BellaZap via WhatsApp.

### Requisitos:
1. Uma instância da Evolution API rodando (Docker ou Servidor Próprio).
2. Uma **Global API Key** definida na instalação da Evo.

### Passos:
1. No painel BellaZap, vá em **Ajustes > Evolution API**.
2. Insira a **URL Base** (ex: `https://sua-api-evo.com`).
3. Insira a **Global API Key**.
4. Clique em **Testar Conexão**.
5. Quando uma nova revendedora se cadastra, o sistema tentará criar automaticamente uma instância com o nome `instancia-[ID-CURTO]`.

### Dicas de Troubleshooting:
- Certifique-se de que o Webhook da Evolution está apontando para o seu backend BellaZap (`/api/v1/whatsapp/webhook`).
- O plano da revendedora deve permitir o uso de IA para que as mensagens sejam processadas.

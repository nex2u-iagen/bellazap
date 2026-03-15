# BellaZap �✨

> **A Plataforma SaaS definitiva para Revendedoras de Cosméticos.**
> Automatize suas vendas, cobranças e gestão financeira diretamente pelo WhatsApp com a inteligência da Bella.

---

## 🚀 Visão Geral do Sistema

O BellaZap é uma solução de última geração projetada para transformar o WhatsApp em uma máquina de vendas. Com uma arquitetura **Multi-tenant (SaaS)** e foco em **Resiliência**, a plataforma oferece:

- **Inteligência Híbrida (Bella IA):** Processamento local com **Qwen 2.5 (Ollama)** e fallback automático para **GPT-4 (OpenAI)**.
- **Pagamentos Dual-Provider:** Integração primária com **Asaas** e fallback transparente para **Abacate Pay**.
- **Gestão de Estoque SaaS:** Catálogo global de produtos com preços e quantidades personalizadas por revendedora.
- **Split Automático:** Divisão de taxas entre plataforma e revendedora direto no checkout.
- **Painel Administrativo Premium:** Gestão estratégica de agentes, instâncias WhatsApp e métricas financeiras.

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia |
| :--- | :--- |
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy (Async) |
| **IA / LLM** | LangChain, Ollama (Qwen 2.5), OpenAI |
| **Frontend** | React, Chakra UI, Vite |
| **Banco de Dados** | PostgreSQL (Supabase/Local) |
| **Mensageria** | Redis + Celery |
| **Integrações** | Evolution API (WhatsApp), Asaas, Abacate Pay |

---

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado:
1. **Python 3.11+**
2. **PostgreSQL** (ou conta Supabase)
3. **Redis** (para as filas do Celery)
4. **Ollama** (para o LLM Local - opcional, mas recomendado)
5. **Node.js & npm** (para o Frontend)

---

## ⚙️ Instalação Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/bellazap.git
   cd bellazap
   ```

2. **Configure o Ambiente Virtual:**
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instale as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as Variáveis de Ambiente:**
   Crie um arquivo `.env` na raiz do projeto com base no seu `src/core/config.py`:
   ```env
   # Database & Redis
   DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/bellazap
   CELERY_BROKER_URL=redis://localhost:6379/0

   # IA (LLM)
   LLM_STRATEGY=local # ou cloud
   LOCAL_LLM_MODEL=qwen2.5:1.5b
   OPENAI_API_KEY=sk-your-key-here

   # Pagamentos
   ASAAS_API_KEY=your-asaas-key
   ABACATE_API_KEY=your-abacate-key

   # WhatsApp
   WHATSAPP_API_URL=http://localhost:8080
   WHATSAPP_GLOBAL_API_KEY=your-evolution-key
   ```

---

## 🚦 Como Rodar (Ambiente de Desenvolvimento)

Com o `honcho` e o `docker-compose`, agora você pode iniciar todo o ambiente de desenvolvimento com um único comando.

**Pré-requisitos:**
- Certifique-se de que o **Docker Desktop** está em execução.
- Certifique-se de que o **Ollama** está instalado e o modelo (`qwen2.5:1.5b`) foi baixado.
- Instale as dependências do frontend com `npm install --prefix frontend`.

### Inicialização Simplificada

Abra um terminal e execute o script de inicialização apropriado para o seu sistema operacional:

**No Windows:**
```bash
start.bat
```

**No Linux/Mac (futuro):**
_(Você pode criar um `start.sh` similar ao `start.bat`)_
```bash
# Exemplo de start.sh
# echo "--- Iniciando servicos de infraestrutura..."
# docker-compose up -d
# echo "--- Ativando ambiente virtual..."
# source .venv/bin/activate
# echo "--- Iniciando aplicacoes com Honcho..."
# honcho -f Procfile.dev start
```

Este comando irá:
1.  **Iniciar o Postgres e o Redis** em background usando `docker-compose`.
2.  **Ativar o ambiente virtual** Python.
3.  **Iniciar a API, o Worker do Celery, o servidor do Frontend e o LLM** em um único terminal com `honcho`, exibindo os logs de todos os serviços de forma centralizada.

Acesse a plataforma em `http://localhost:5173`.


---

## 🧪 Validação dos Módulos

Para garantir que tudo está funcionando corretamente após a instalação:

- **Testes Unitários:** `pytest tests/`
- **Docs API:** `http://localhost:8000/docs`
- **Fluxo Inicial:** Envie "QUERO COMEÇAR" para o seu número configurado no WhatsApp e aguarde o onboarding da Bella.

---

## 🛡️ Segurança e Resiliência

O sistema possui **Circuit Breakers** para todas as chamadas externas. Se o Asaas cair, o sistema muda para o Abacate Pay automaticamente. Se o seu PC local ficar offline, a Bella migra para a nuvem (OpenAI) sem que a revendedora perceba.

---
Desenvolvido com ❤️ pela equipe nex2u - IA para negócios.

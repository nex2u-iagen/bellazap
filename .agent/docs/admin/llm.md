# Configuração de Modelos IA (Ollama, OpenAI, Gemini, Groq)

O BellaZap suporta uma estratégia híbrida:

### 1. Local (Ollama) - Grátis e Privado
- Instale o [Ollama](https://ollama.com).
- Rode `ollama run qwen2.5:3b` para baixar o modelo sugerido.
- No painel, configure o endpoint (padrão: `http://localhost:11434`).

### 2. Nuvem (Fallback)
- **OpenAI**: Requer uma chave `sk-...`. Alta precisão para vendas.
- **Google (Gemini)**: Ótimo custo-benefício. Requer chave do Google AI Studio.
- **Groq**: Velocidade ultra-rápida. Use modelos como `llama-3.1-70b-versatile`.

### Como Funciona o Fallback:
Se o servidor local (Ollama) demorar mais de 10 segundos para responder ou estiver offline, a Bella automaticamente usará o Provedor de Nuvem configurado em **Ajustes > Fallback & LLM**.

from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "BellaZap"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "segredo_padrao_para_dev"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/bellazap"
    TURSO_DATABASE_URL: str = "libsql://bellazap-eliezer.turso.io"
    TURSO_AUTH_TOKEN: str = "SUA_AUTH_TOKEN_AQUI"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_HOST: str = "localhost" # Para configurar o Celery
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CELERY_BROKER_URL: str = "redis://localhost:6379/0" # URL do broker Celery
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0" # Backend para resultados Celery

    # Asaas
    ASAAS_API_KEY: str = "SUA_API_KEY_ASAAS_AQUI"
    ASAAS_WEBHOOK_TOKEN: str = "TOKEN_DE_SEGURANCA_WEBHOOK"
    ASAAS_ENV: str = "sandbox" # ou "production"

    # Abacate Pay
    ABACATE_API_KEY: str = "SUA_API_KEY_ABACATE_AQUI"
    ABACATE_ENV: str = "sandbox" # ou "production"

    # WhatsApp (Evolution API ou similar)
    WHATSAPP_API_URL: str = "http://localhost:8080"
    WHATSAPP_GLOBAL_API_KEY: str = "42ha9631-411a-4286-932d-20d43c7b64a2"

    # LLM & Agentes
    OPENAI_API_KEY: str = "SUA_API_KEY_OPENAI"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_STRATEGY: str = "local" # 'local' ou 'cloud'
    LOCAL_LLM_MODEL: str = "qwen2.5:3b"
    CLOUD_LLM_MODEL: str = "gpt-4-turbo-preview"

    # Telegram
    TELEGRAM_BOT_TOKEN: str = "SEU_TOKEN_AQUI"
    TELEGRAM_WEBHOOK_SECRET: str = "segredo_webhook_telegram" # Para validar webhooks

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" # Ignora variaveis extras no .env
    )

settings = Settings()

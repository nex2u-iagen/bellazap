from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.v1.endpoints import payments # Importar o router de pagamentos

from contextlib import asynccontextmanager
from src.db.session import check_database_connection

from src.db.init_db import init_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Verificar conexão com Turso
    db_ok = await check_database_connection()
    if db_ok:
        # Inicializar tabelas de forma assíncrona
        await init_tables()
    else:
        print("⚠️ ALERTA: Não foi possível conectar ao Turso. Verifique as credenciais.")
    yield
    # Shutdown: (opcional) fechar conexões
    pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Plataforma SaaS para revendedoras de cosméticos com IA via Telegram.",
    lifespan=lifespan
)

# Configuração de CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
async def root():
    return {
        "mensagem": "Bem-vindo ao BellaZap API",
        "docs": "/docs",
        "status": "online"
    }

# Incluir os routers
from src.api.v1.endpoints import payments, admin, telegram

app.include_router(payments.router, prefix=f"{settings.API_V1_STR}/payments", tags=["Pagamentos"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Super Admin"])
app.include_router(telegram.router, prefix=f"{settings.API_V1_STR}/telegram", tags=["Telegram"])

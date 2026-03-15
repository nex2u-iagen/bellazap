from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.v1.endpoints import payments # Importar o router de pagamentos

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Plataforma SaaS para revendedoras de cosméticos com automação via WhatsApp."
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
from src.api.v1.endpoints import payments, whatsapp, agents, admin

app.include_router(payments.router, prefix=f"{settings.API_V1_STR}/payments", tags=["Pagamentos"])
app.include_router(whatsapp.router, prefix=f"{settings.API_V1_STR}/whatsapp", tags=["WhatsApp"])
app.include_router(agents.router, prefix=f"{settings.API_V1_STR}/agents", tags=["Agentes"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Super Admin"])

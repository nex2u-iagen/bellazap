import libsql_client
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Criar cliente Turso (LibSQL)
# Suporta conexões HTTP (Edge) e WebSocket
_client_instance = None

class LazyClient:
    def __getattr__(self, name):
        global _client_instance
        if _client_instance is None:
            import asyncio
            # Ensure an event loop exists before creating the client
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                # If there's truly no loop yet, it's safer to wait, but uvicorn should have one
                pass
            
            _client_instance = libsql_client.create_client(
                url=settings.TURSO_DATABASE_URL,
                auth_token=settings.TURSO_AUTH_TOKEN
            )
        return getattr(_client_instance, name)
        
client = LazyClient()

async def check_database_connection():
    """
    Realiza um teste de ping no Turso para garantir que o ambiente serverless
    consegue alcançar o banco de dados.
    """
    try:
        await client.execute("SELECT 1")
        logger.info("✅ Conexão com Turso estabelecida com sucesso.")
        return True
    except Exception as e:
        logger.error(f"❌ Falha ao conectar no Turso: {str(e)}")
        # Em ambiente serverless, podemos querer que o sistema 'fail-fast'
        return False

# Dependência para injetar o cliente nos endpoints (se necessário)
async def get_db():
    """
    Retorna o cliente de banco de dados para ser usado nas rotas.
    O cliente do libsql já gerencia o pool de forma eficiente para serverless.
    """
    return client

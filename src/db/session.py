from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import settings

# Criar engine assíncrono
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False, # Defina como True para ver os SQLs gerados no console
    future=True,
)

# Criar fábrica de sessões
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Dependência para injetar sessão nos endpoints
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

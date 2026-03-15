import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db.base import Base
from src.db.session import get_db # Importa a dependência original para sobrescrever

# Configuração de um banco de dados SQLite em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function", autouse=True)
async def setup_db():
    """Cria as tabelas no banco de dados de teste e as dropa no final para cada teste."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fornece uma sessão de banco de dados assíncrona para os testes."""
    async with TestingSessionLocal() as session:
        yield session

# Função para sobrescrever a dependência get_db do FastAPI para testes.
# Esta função será usada pelo FastAPI quando ele chamar get_db().
async def get_test_db_override():
    """Função para sobrescrever a dependência get_db do FastAPI para testes."""
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = get_test_db_override

@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP assíncrono para testar a aplicação FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # A fixture client *não* precisa chamar get_test_db_override(), pois o FastAPI já usa.
        # Mas para testes que precisam de uma sessão do DB para configurar dados,
        # a fixture db_session é injetada.
        yield c

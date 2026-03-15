import uuid
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.cliente import Cliente
from typing import List, Optional

class ClientService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create_client(self, revendedora_id: uuid.UUID, nome: str, **kwargs) -> Cliente:
        cliente = Cliente(
            revendedora_id=revendedora_id,
            nome=nome,
            **kwargs
        )
        self.db.add(cliente)
        await self.db.commit()
        await self.db.refresh(cliente)
        return cliente

    async def get_client_by_id(self, client_id: uuid.UUID, revendedora_id: uuid.UUID) -> Optional[Cliente]:
        stmt = select(Cliente).where(
            Cliente.id == client_id,
            Cliente.revendedora_id == revendedora_id
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def search_clients(self, revendedora_id: uuid.UUID, query: str) -> List[Cliente]:
        stmt = select(Cliente).where(
            Cliente.revendedora_id == revendedora_id,
            Cliente.nome.ilike(f"%{query}%")
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

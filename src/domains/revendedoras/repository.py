import uuid
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.core import Revendedora, Venda

class RevendedoraRepository:
    """Repositório para gerenciar dados de revendedoras."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_by_id(self, revendedora_id: uuid.UUID) -> Optional[Revendedora]:
        return await self.db.get(Revendedora, revendedora_id)

    async def get_active_revendedoras(self) -> List[Revendedora]:
        result = await self.db.execute(select(Revendedora).where(Revendedora.is_active == True))
        return list(result.scalars().all())

class VendaRepository:
    """Repositório para gerenciar vendas."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create(self, venda: Venda) -> Venda:
        self.db.add(venda)
        await self.db.commit()
        await self.db.refresh(venda)
        return venda

    async def get_contingency_sales(self) -> List[Venda]:
        """Busca vendas em modo contingência."""
        result = await self.db.execute(select(Venda).where(Venda.status == 'contingency'))
        return list(result.scalars().all())

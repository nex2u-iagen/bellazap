import uuid
from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.core import AgentConfig, Produto, RevendedoraEstoque

class AgentRepository:
    """Gestão de configurações de agentes IA."""
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_active(self) -> List[AgentConfig]:
        result = await self.db.execute(select(AgentConfig).where(AgentConfig.is_active == True))
        return list(result.scalars().all())

    async def create_or_update(self, config_data: dict) -> AgentConfig:
        agent_id = config_data.get('id')
        if agent_id:
            agent = await self.db.get(AgentConfig, agent_id)
            for key, value in config_data.items():
                setattr(agent, key, value)
        else:
            agent = AgentConfig(**config_data)
            self.db.add(agent)
        
        await self.db.commit()
        await self.db.refresh(agent)
        return agent

class CatalogRepository:
    """Gestão de produtos (Global) e Estoque (Individual/SaaS)."""
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_global_products(self) -> List[Produto]:
        result = await self.db.execute(select(Produto))
        return list(result.scalars().all())

    async def get_revendedora_inventory(self, revendedora_id: uuid.UUID) -> List[RevendedoraEstoque]:
        from sqlalchemy.orm import selectinload
        stmt = (
            select(RevendedoraEstoque)
            .options(selectinload(RevendedoraEstoque.produto))
            .where(RevendedoraEstoque.revendedora_id == revendedora_id)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update_inventory(self, revendedora_id: uuid.UUID, produto_id: uuid.UUID, quantidade: int):
        stmt = select(RevendedoraEstoque).where(
            RevendedoraEstoque.revendedora_id == revendedora_id,
            RevendedoraEstoque.produto_id == produto_id
        )
        result = await self.db.execute(stmt)
        item = result.scalars().first()
        
        if item:
            item.quantidade = quantidade
        else:
            item = RevendedoraEstoque(
                revendedora_id=revendedora_id,
                produto_id=produto_id,
                quantidade=quantidade
            )
            self.db.add(item)
        
        await self.db.commit()

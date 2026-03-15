import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.base import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    revendedora_id = Column(UUID(as_uuid=True), ForeignKey("revendedoras.id"), nullable=False)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    cpf_cnpj = Column(String, nullable=True)
    endereco = Column(Text, nullable=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    metadata_ = Column(JSON, nullable=True, name="metadata")

    revendedora = relationship("Revendedora")
    # Relacionamento futuro para histórico de conversas/vendas específicas

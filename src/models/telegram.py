import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, BigInteger, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.base import Base

class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    revendedora_id = Column(UUID(as_uuid=True), ForeignKey("revendedoras.id"), nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    data_vinculacao = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    revendedora = relationship("Revendedora")

class TelegramChatState(Base):
    __tablename__ = "telegram_chat_states"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    state = Column(String, default="IDLE") # IDLE, WIZARD_CLIENTE, CONFIRMING_SALE, etc.
    context_data = Column(JSON, nullable=True) # Para armazenar dados temporários do fluxo
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

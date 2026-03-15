import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, DateTime, DECIMAL, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.base import Base
from sqlalchemy import UniqueConstraint # Importar UniqueConstraint
from src.models.core import Revendedora, Venda # Importar os novos modelos

# Tabela de provedores
class PaymentProvider(Base):
    __tablename__ = "payment_providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False) # 'asaas', 'abacate'
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=1) # 1 = primário, 2 = fallback
    config = Column(JSON, nullable=True) # Configurações específicas JSONB
    created_at = Column(DateTime, default=datetime.utcnow)

    wallets = relationship("RevendedoraWallet", back_populates="provider")
    transactions = relationship("Transaction", back_populates="provider")
    webhook_failures = relationship("WebhookFailure", back_populates="provider")

# Carteiras digitais por provedor (para revendedoras)
class RevendedoraWallet(Base):
    __tablename__ = "revendedora_wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    revendedora_id = Column(UUID(as_uuid=True), ForeignKey("revendedoras.id"), nullable=False) # Assumindo tabela 'revendedoras'
    provider_id = Column(UUID(as_uuid=True), ForeignKey("payment_providers.id"), nullable=False)
    wallet_id = Column(Text, nullable=False) # ID da carteira no provedor
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    provider = relationship("PaymentProvider", back_populates="wallets")
    revendedora = relationship("Revendedora", back_populates="wallets")

    __table_args__ = (
        # Garante que uma revendedora só tenha uma carteira por provedor
        UniqueConstraint('revendedora_id', 'provider_id', name='uq_revendedora_provider_wallet'),
    )

# Transações (unificado)
class Transaction(Base):
    __tablename__ = "transacoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    revendedora_id = Column(UUID(as_uuid=True), ForeignKey("revendedoras.id"), nullable=False) # Assumindo tabela 'revendedoras'
    venda_id = Column(UUID(as_uuid=True), ForeignKey("vendas.id"), nullable=True) # Assumindo tabela 'vendas'
    
    # Provider usado
    provider_id = Column(UUID(as_uuid=True), ForeignKey("payment_providers.id"), nullable=False)
    provider_payment_id = Column(Text, nullable=True) # ID do pagamento no provedor
    
    # Valores
    valor_bruto = Column(DECIMAL, nullable=False)
    taxa_plataforma = Column(DECIMAL, nullable=False)
    taxa_provider = Column(DECIMAL, nullable=False)
    valor_liquido_revendedora = Column(DECIMAL, nullable=False)
    
    # Split
    split_config = Column(JSON, nullable=True) # Configuração de split enviada
    
    # Status
    status = Column(String, default='pending') # pending, confirmed, failed, refunded
    webhook_recebido = Column(Boolean, default=False)
    webhook_retries = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    failed_at = Column(DateTime, nullable=True)

    provider = relationship("PaymentProvider", back_populates="transactions")
    revendedora = relationship("Revendedora", back_populates="transacoes")
    venda = relationship("Venda", back_populates="transacoes")

# Dead Letter Queue para webhooks falhos
class WebhookFailure(Base):
    __tablename__ = "webhook_failures"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("payment_providers.id"), nullable=False)
    payload = Column(JSON, nullable=False)
    error = Column(Text, nullable=True)
    attempts = Column(Integer, default=1)
    last_attempt = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='pending') # pending, resolved, dead
    created_at = Column(DateTime, default=datetime.utcnow)

    provider = relationship("PaymentProvider", back_populates="webhook_failures")

class Withdraw(Base):
    """Solicitações de saque das revendedoras."""
    __tablename__ = "saques"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    revendedora_id = Column(UUID(as_uuid=True), ForeignKey("revendedoras.id"), nullable=False)
    valor = Column(DECIMAL, nullable=False)
    status = Column(String, default="pending") # pending, processed, failed
    pix_key = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    metadata_ = Column(JSON, nullable=True)

    revendedora = relationship("Revendedora", back_populates="saques")

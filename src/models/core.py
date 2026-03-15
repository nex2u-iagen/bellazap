import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, DECIMAL, ForeignKey, Text, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.base import Base
from src.domains.pagamentos.split_calculator import PlanType

class Revendedora(Base):
    __tablename__ = "revendedoras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    cpf_cnpj = Column(String, unique=True, nullable=False)
    telefone = Column(String, nullable=True)
    whatsapp_instance = Column(String, nullable=True) # Nome da instância na Evolution API
    whatsapp_status = Column(String, default="disconnected")
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    plano = Column(String, default=PlanType.BASIC.value)

    # Relacionamentos
    wallets = relationship("RevendedoraWallet", back_populates="revendedora")
    transacoes = relationship("Transaction", back_populates="revendedora")
    vendas = relationship("Venda", back_populates="revendedora")
    estoque = relationship("RevendedoraEstoque", back_populates="revendedora")
    saques = relationship("Withdraw", back_populates="revendedora")

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    revendedora_id = Column(UUID(as_uuid=True), ForeignKey("revendedoras.id"), nullable=False)
    valor_total = Column(DECIMAL, nullable=False)
    status = Column(String, default="pending") 
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata_ = Column(JSON, nullable=True, name="metadata")

    revendedora = relationship("Revendedora", back_populates="vendas")
    transacoes = relationship("Transaction", back_populates="venda")

class Produto(Base):
    """Catálogo global de produtos compartilhado entre todos."""
    __tablename__ = "produtos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = Column(String, unique=True, nullable=False) # SKU
    nome = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    categoria = Column(String, nullable=True)
    preco_sugerido = Column(DECIMAL, nullable=True)

    estoques = relationship("RevendedoraEstoque", back_populates="produto")

class RevendedoraEstoque(Base):
    """Estoque individual de cada revendedora para os produtos globais."""
    __tablename__ = "revendedoras_estoque"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    revendedora_id = Column(UUID(as_uuid=True), ForeignKey("revendedoras.id"), nullable=False)
    produto_id = Column(UUID(as_uuid=True), ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, default=0)
    preco_personalizado = Column(DECIMAL, nullable=True) # Revendedora pode mudar o preço dela

    revendedora = relationship("Revendedora", back_populates="estoque")
    produto = relationship("Produto", back_populates="estoques")

class AgentConfig(Base):
    """Configurações administrativas e estratégicas dos Agentes IA."""
    __tablename__ = "agentes_config"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False) # Ex: "Bella Suporte", "Bella Vendas"
    departamento = Column(String, nullable=False) # Ex: "suporte", "vendas"
    prompt_contexto = Column(Text, nullable=False) # Contexto/Prompt do sistema
    api_key_openai = Column(String, nullable=True) # Sobrescreve a global se necessário
    model_name = Column(String, default="gpt-4-turbo-preview")
    is_active = Column(Boolean, default=True)
    metadata_ = Column(JSON, nullable=True, name="metadata")
class MessageLog(Base):
    """Log de conversas para auditoria e análise de padrões da IA."""
    __tablename__ = "message_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    revendedora_id = Column(UUID(as_uuid=True), ForeignKey("revendedoras.id"), nullable=False)
    role = Column(String) # user, assistant
    content = Column(Text)
    model_used = Column(String) # qwen2.5:3b, gpt-4
    timestamp = Column(DateTime, default=datetime.utcnow)
    intent = Column(String, nullable=True) # venda, cadastro_produto, dúvida
    
    revendedora = relationship("Revendedora")

class SystemConfiguration(Base):
    """Configurações globais do sistema (Evolution, Fallback, etc)."""
    __tablename__ = "system_configurations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String, unique=True, nullable=False) # Ex: 'evo_url', 'fallback_llm'
    value = Column(Text, nullable=False)
    description = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category = Column(String, default="general") # evolution, llm, security, database

from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, condecimal

class SplitRule(BaseModel):
    """Schema para uma regra de split de pagamento."""
    wallet_id: str = Field(..., description="ID da carteira do recebedor no provedor de pagamento.")
    value: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Valor fixo a ser transferido para o recebedor.")
    # Ou porcentagem, dependendo do provedor:
    # percentage: float = Field(None, description="Percentual do valor total a ser transferido.")

class PaymentCreate(BaseModel):
    """Schema para a criação de um novo pagamento."""
    revendedora_id: UUID = Field(..., description="ID da revendedora associada a este pagamento.")
    venda_id: Optional[UUID] = Field(None, description="ID da venda associada (opcional).")
    amount: condecimal(max_digits=10, decimal_places=2) = Field(..., gt=0, description="Valor total bruto do pagamento.")
    customer_data: Dict[str, Any] = Field(..., description="Dados do cliente para o provedor de pagamento (ex: name, email, cpfCnpj).")
    split_rules: List[SplitRule] = Field([], description="Regras de split para o pagamento.")

class PaymentResponse(BaseModel):
    """Schema para a resposta de um pagamento criado."""
    id: UUID = Field(..., description="ID interno da transação no sistema BellaZap.")
    provider_name: str = Field(..., description="Nome do provedor de pagamento usado.")
    provider_payment_id: str = Field(..., description="ID da transação no provedor de pagamento.")
    status: str = Field(..., description="Status atual do pagamento (ex: 'pending', 'confirmed').")
    amount: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Valor total do pagamento.")
    created_at: datetime = Field(..., description="Timestamp de criação do pagamento.")

    class Config:
        from_attributes = True # ou orm_mode = True para Pydantic < v2

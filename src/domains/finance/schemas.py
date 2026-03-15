from pydantic import BaseModel, Field
from typing import Optional, List

class PaymentRequest(BaseModel):
    revendedora_id: str
    cliente_id: str
    valor: float = Field(..., gt=0)
    descricao: Optional[str] = "Venda BellaZap"

class PaymentResponse(BaseModel):
    pix_qr_code: str
    pix_chave: str
    asaas_id: str
    status: str

class WebhookAsaas(BaseModel):
    event: str
    payment: dict

from fastapi import APIRouter, Depends, HTTPException, Request, Header, status
from src.domains.finance.schemas import PaymentRequest, PaymentResponse
from src.domains.finance.service import FinanceService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=PaymentResponse)
async def create_payment(payment_data: PaymentRequest):
    """
    Cria um novo pagamento PIX com split automático.
    """
    try:
        data = await FinanceService.generate_pix_venda(
            revendedora_id=payment_data.revendedora_id,
            valor=payment_data.valor,
            cliente_id=payment_data.cliente_id
        )
        return PaymentResponse(**data)
    except Exception as e:
        logger.error(f"Erro ao criar pagamento: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def asaas_webhook(
    request: Request,
    asaas_access_token: str = Header(None)
):
    """
    Recebe notificações de pagamento do Asaas com segurança e idempotência.
    """
    payload = await request.json()
    # No Asaas, o token costuma vir em asa-access-token (header customizada)
    success = await FinanceService.process_webhook(payload, asaas_access_token)
    
    if not success:
        # Se falhar a validação do token, retornamos 401
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return {"status": "processed"}

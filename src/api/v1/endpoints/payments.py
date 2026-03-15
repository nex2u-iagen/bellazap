from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.schemas.payment import PaymentCreate, PaymentResponse
from src.domains.pagamentos.payment_service import PaymentService
from src.models.core import Revendedora
from src.models.payment import PaymentProvider # Importar para obter o nome do provedor na resposta
from src.domains.pagamentos.split_calculator import PlanType, SplitCalculator # Importar SplitCalculator e PlanType

router = APIRouter()

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_new_payment(
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Cria um novo pagamento com fallback automático de provedor e regras de split.
    """
    # 1. Buscar a revendedora para determinar o plano
    revendedora = await db.get(Revendedora, payment_data.revendedora_id)
    if not revendedora:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Revendedora com ID {payment_data.revendedora_id} não encontrada."
        )
    
    # 2. Instanciar o PaymentService
    payment_service = PaymentService(db_session=db)

    try:
        # Passar o plano da revendedora para o PaymentService
        created_transaction = await payment_service.create_payment_with_split(
            customer_data=payment_data.customer_data,
            amount=float(payment_data.amount),
            split_rules=payment_data.split_rules,
            revendedora_id=payment_data.revendedora_id,
            venda_id=payment_data.venda_id,
            revendedora_plan=PlanType(revendedora.plano) # Passa o plano da revendedora
        )
        
        # O created_transaction é o modelo Transaction do SQLAlchemy
        # Precisamos convertê-lo para PaymentResponse (schema Pydantic)
        provider_name = "desconhecido"
        if created_transaction.provider_id:
            provider_db_obj = await db.get(PaymentProvider, created_transaction.provider_id)
            if provider_db_obj:
                provider_name = provider_db_obj.name

        return PaymentResponse(
            id=created_transaction.id,
            provider_name=provider_name,
            provider_payment_id=created_transaction.provider_payment_id,
            status=created_transaction.status,
            amount=created_transaction.valor_bruto,
            created_at=created_transaction.created_at
        )

    except Exception as e:
        # Tratar exceções do serviço de pagamento
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao criar pagamento: {e}"
        )

from celery import Celery
import logging
import asyncio
import datetime
from src.core.config import settings
from src.db.session import AsyncSessionLocal
from src.domains.pagamentos.payment_service import PaymentService
from src.domains.pagamentos.repository import PaymentRepository
from src.domains.notificacoes.service import NotificationService

logger = logging.getLogger(__name__)

app = Celery(
    'reconciliation_worker',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@app.task
def reconcile_payments_task():
    """Tarefa Celery para reconciliação de pagamentos (Trabalho noturno/periódico)."""
    asyncio.run(_reconcile_payments_async())

async def _reconcile_payments_async():
    """Lógica assíncrona de reconciliação."""
    logger.info("Iniciando tarefa de reconciliação de pagamentos.")
    async with AsyncSessionLocal() as db_session:
        payment_repo = PaymentRepository(db_session)
        payment_service = PaymentService(db_session=db_session)
        notification_service = NotificationService()
        
        # 1. Busca transações pendentes há mais de 2h
        transacoes_pendentes = await payment_repo.get_pending_transactions(hours=2)
        
        for transacao in transacoes_pendentes:
            try:
                # Consulta status no provider
                provider_db_obj = await payment_repo.get_provider_by_id(transacao.provider_id)
                if not provider_db_obj:
                    logger.error(f"Provedor {transacao.provider_id} não encontrado.")
                    continue

                provider_instance = (payment_service.primary if provider_db_obj.name == "asaas" 
                                    else payment_service.fallback)
                
                status_response = await provider_instance.get_payment_status(str(transacao.provider_payment_id))
                internal_status = status_response.get('status', '').upper()
                
                if internal_status in ['CONFIRMED', 'RECEIVED']:
                    await payment_repo.confirm_transaction(transacao.id)
                    await notification_service.notify_revendedora(transacao.revendedora_id, "pagamento_confirmado")
                    logger.info(f"Pagamento {transacao.id} confirmado via reconciliação.")
                    
                elif internal_status in ['FAILED', 'CANCELLED']:
                    await payment_repo.fail_transaction(transacao.id)
                    
            except Exception as e:
                logger.error(f"Erro na reconciliação da transação {transacao.id}: {e}")
        
    logger.info("Reconciliação de pagamentos concluída.")

@app.task
def retry_failed_webhooks_task():
    """Tarefa Celery para reprocessar webhooks falhos na DLQ."""
    asyncio.run(_retry_failed_webhooks_async())

async def _retry_failed_webhooks_async():
    """Lógica assíncrona de reprocessamento de webhooks."""
    logger.info("Iniciando reprocessamento de webhooks falhos.")
    async with AsyncSessionLocal() as db_session:
        payment_repo = PaymentRepository(db_session)
        payment_service = PaymentService(db_session=db_session)
        notification_service = NotificationService()
        
        failures = await payment_repo.get_pending_webhook_failures(limit=100)
        
        for failure in failures:
            if failure.attempts >= 5:
                # Excedeu tentativas - marcar como morto e alertar admin
                logger.critical(f"Webhook {failure.id} permanentemente falho.")
                await payment_repo.mark_webhook_as_dead(failure.id)
                await notification_service.alert_admin(
                    title="Webhook falho permanentemente",
                    message=f"ID: {failure.id} - Provider: {failure.provider_id}",
                    priority="high"
                )
                continue
            
            try:
                provider_db_obj = await payment_repo.get_provider_by_id(failure.provider_id)
                provider_name = provider_db_obj.name if provider_db_obj else None
                
                await payment_service.process_webhook(
                    payload=failure.payload,
                    provider_name_hint=provider_name
                )
                await payment_repo.resolve_webhook_failure(failure.id)
                
            except Exception as e:
                await payment_repo.increment_webhook_attempt(failure.id, str(e))
                logger.warning(f"Falha ao reprocessar webhook {failure.id}: {e}")
                
    logger.info("Reprocessamento de webhooks concluído.")

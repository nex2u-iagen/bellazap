import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
import uuid
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from src.models.payment import Transaction, WebhookFailure, PaymentProvider as PaymentProviderModel
from src.workers.reconciliation_worker import reconcile_payments_task, retry_failed_webhooks_task

# Mock para datetime.utcnow() para controlar o tempo nos testes
@pytest.fixture
def mock_utcnow():
    with patch('src.workers.reconciliation_worker.datetime') as mock_dt:
        mock_dt.datetime.utcnow.return_value = datetime(2023, 1, 1, 12, 0, 0)
        yield mock_dt

@pytest.mark.asyncio
@patch('src.workers.reconciliation_worker.AsyncSessionLocal')
@patch('src.workers.reconciliation_worker.PaymentRepository', autospec=True)
@patch('src.workers.reconciliation_worker.PaymentService', autospec=True)
@patch('src.workers.reconciliation_worker.NotificationService', autospec=True)
@patch('src.workers.reconciliation_worker.asyncio.run')
async def test_reconcile_payments_task(
    mock_asyncio_run,
    mock_notification_service_class,
    mock_payment_service_class,
    mock_payment_repo_class,
    mock_async_session_local,
    db_session: AsyncSession,
    mock_utcnow
):
    # Simular a execução da tarefa chamando a função interna diretamente para facilitar o teste
    from src.workers.reconciliation_worker import _reconcile_payments_async
    
    mock_session = AsyncMock(spec=AsyncSession)
    mock_async_session_local.return_value.__aenter__.return_value = mock_session
    
    mock_repo = mock_payment_repo_class.return_value
    mock_service = mock_payment_service_class.return_value
    mock_notification = mock_notification_service_class.return_value

    asaas_provider = PaymentProviderModel(id=uuid.uuid4(), name="asaas")
    mock_repo.get_provider_by_id.return_value = asaas_provider

    pending_transaction = Transaction(
        id=uuid.uuid4(),
        revendedora_id=uuid.uuid4(),
        provider_id=asaas_provider.id,
        provider_payment_id="pay_pending_123",
        status="pending"
    )
    mock_repo.get_pending_transactions.return_value = [pending_transaction]

    mock_service.primary = AsyncMock()
    mock_service.primary.get_payment_status.return_value = {"status": "CONFIRMED"}

    await _reconcile_payments_async()

    mock_repo.get_pending_transactions.assert_called_once_with(hours=2)
    mock_repo.confirm_transaction.assert_called_once_with(pending_transaction.id)
    mock_notification.notify_revendedora.assert_called_once_with(
        pending_transaction.revendedora_id, "pagamento_confirmado"
    )

@pytest.mark.asyncio
@patch('src.workers.reconciliation_worker.AsyncSessionLocal')
@patch('src.workers.reconciliation_worker.PaymentRepository', autospec=True)
@patch('src.workers.reconciliation_worker.PaymentService', autospec=True)
@patch('src.workers.reconciliation_worker.NotificationService', autospec=True)
async def test_retry_failed_webhooks_task(
    mock_notification_service_class,
    mock_payment_service_class,
    mock_payment_repo_class,
    mock_async_session_local,
    db_session: AsyncSession,
    mock_utcnow
):
    from src.workers.reconciliation_worker import _retry_failed_webhooks_async
    
    mock_session = AsyncMock(spec=AsyncSession)
    mock_async_session_local.return_value.__aenter__.return_value = mock_session
    
    mock_repo = mock_payment_repo_class.return_value
    mock_service = mock_payment_service_class.return_value
    mock_service.process_webhook = AsyncMock(return_value={"status": "processed"})

    asaas_provider = PaymentProviderModel(id=uuid.uuid4(), name="asaas")
    mock_repo.get_provider_by_id.return_value = asaas_provider

    failed_webhook = WebhookFailure(
        id=uuid.uuid4(),
        provider_id=asaas_provider.id,
        payload={"event": "payment.failed"},
        attempts=1
    )
    mock_repo.get_pending_webhook_failures.return_value = [failed_webhook]

    await _retry_failed_webhooks_async()

    mock_repo.get_pending_webhook_failures.assert_called_once_with(limit=100)
    mock_service.process_webhook.assert_called_once_with(
        payload={"event": "payment.failed"},
        provider_name_hint="asaas"
    )
    mock_repo.resolve_webhook_failure.assert_called_once_with(failed_webhook.id)

@pytest.mark.asyncio
@patch('src.workers.reconciliation_worker.AsyncSessionLocal')
@patch('src.workers.reconciliation_worker.PaymentRepository', autospec=True)
@patch('src.workers.reconciliation_worker.PaymentService', autospec=True)
@patch('src.workers.reconciliation_worker.NotificationService', autospec=True)
async def test_retry_failed_webhooks_max_attempts(
    mock_notification_service_class,
    mock_payment_service_class,
    mock_payment_repo_class,
    mock_async_session_local,
    db_session: AsyncSession,
    mock_utcnow
):
    from src.workers.reconciliation_worker import _retry_failed_webhooks_async
    
    mock_session = AsyncMock(spec=AsyncSession)
    mock_async_session_local.return_value.__aenter__.return_value = mock_session
    
    mock_repo = mock_payment_repo_class.return_value
    mock_notification = mock_notification_service_class.return_value

    failed_webhook_max = WebhookFailure(
        id=uuid.uuid4(),
        provider_id=uuid.uuid4(),
        payload={"event": "payment.failed"},
        attempts=5
    )
    mock_repo.get_pending_webhook_failures.return_value = [failed_webhook_max]

    await _retry_failed_webhooks_async()

    mock_repo.mark_webhook_as_dead.assert_called_once_with(failed_webhook_max.id)
    mock_notification.alert_admin.assert_called_once()

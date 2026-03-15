import uuid
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.payment import Transaction, WebhookFailure, PaymentProvider

class PaymentRepository:
    """Repositório para gerenciar transações e falhas de webhooks."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_pending_transactions(self, hours: int = 2) -> List[Transaction]:
        """Busca transações pendentes há mais de X horas."""
        limit_date = datetime.utcnow() - timedelta(hours=hours)
        result = await self.db.execute(
            select(Transaction).where(
                Transaction.status == 'pending',
                Transaction.created_at < limit_date
            )
        )
        return list(result.scalars().all())

    async def confirm_transaction(self, transaction_id: uuid.UUID):
        """Confirma uma transação."""
        transaction = await self.db.get(Transaction, transaction_id)
        if transaction:
            transaction.status = 'confirmed'
            transaction.confirmed_at = datetime.utcnow()
            await self.db.commit()

    async def fail_transaction(self, transaction_id: uuid.UUID):
        """Marca transação como falha."""
        transaction = await self.db.get(Transaction, transaction_id)
        if transaction:
            transaction.status = 'failed'
            transaction.failed_at = datetime.utcnow()
            await self.db.commit()

    async def get_pending_webhook_failures(self, limit: int = 100) -> List[WebhookFailure]:
        """Busca webhooks falhos pendentes."""
        result = await self.db.execute(
            select(WebhookFailure)
            .where(WebhookFailure.status == 'pending')
            .order_by(WebhookFailure.last_attempt.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def mark_webhook_as_dead(self, failure_id: uuid.UUID):
        failure = await self.db.get(WebhookFailure, failure_id)
        if failure:
            failure.status = 'dead'
            await self.db.commit()

    async def resolve_webhook_failure(self, failure_id: uuid.UUID):
        failure = await self.db.get(WebhookFailure, failure_id)
        if failure:
            failure.status = 'resolved'
            await self.db.commit()

    async def increment_webhook_attempt(self, failure_id: uuid.UUID, error: str):
        failure = await self.db.get(WebhookFailure, failure_id)
        if failure:
            failure.attempts += 1
            failure.last_attempt = datetime.utcnow()
            failure.error = error
            await self.db.commit()

    async def get_provider_by_id(self, provider_id: uuid.UUID) -> Optional[PaymentProvider]:
        return await self.db.get(PaymentProvider, provider_id)

import logging
import uuid
from decimal import Decimal
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.payment import Transaction, Withdraw, RevendedoraWallet

logger = logging.getLogger(__name__)

class WalletService:
    """Gerencia o saldo líquido e solicitações de saque das revendedoras."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_balance(self, revendedora_id: uuid.UUID) -> Decimal:
        """Calcula o saldo disponível (Vendas Pagas - Saques Processados)."""
        # 1. Total de entradas (Vendas confirmadas)
        stmt_entries = select(func.sum(Transaction.valor_liquido_revendedora)).where(
            Transaction.revendedora_id == revendedora_id,
            Transaction.status == 'confirmed'
        )
        result_entries = await self.db.execute(stmt_entries)
        entries = result_entries.scalar() or Decimal('0.00')

        # 2. Total de saídas (Saques processados ou pendentes)
        stmt_withdraws = select(func.sum(Withdraw.valor)).where(
            Withdraw.revendedora_id == revendedora_id,
            Withdraw.status.in_(['pending', 'processed'])
        )
        result_withdraws = await self.db.execute(stmt_withdraws)
        withdraws = result_withdraws.scalar() or Decimal('0.00')

        return entries - withdraws

    async def request_withdraw(self, revendedora_id: uuid.UUID, amount: Decimal, pix_key: str) -> Withdraw:
        """Cria uma solicitação de saque após validar saldo."""
        if amount < Decimal('10.00'):
            raise Exception("O valor mínimo para saque é R$ 10,00.")

        balance = await self.get_balance(revendedora_id)
        if amount > balance:
            raise Exception(f"Saldo insuficiente. Seu saldo disponível é R$ {balance:.2f}")

        new_withdraw = Withdraw(
            revendedora_id=revendedora_id,
            valor=amount,
            pix_key=pix_key,
            status='pending'
        )
        
        self.db.add(new_withdraw)
        await self.db.commit()
        await self.db.refresh(new_withdraw)
        
        logger.info(f"Solicitação de saque de R$ {amount} registrada para revendedora {revendedora_id}")
        return new_withdraw

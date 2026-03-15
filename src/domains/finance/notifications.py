from src.db.session import client
from src.domains.telegram.service import TelegramService
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    async def notify_overdue_payments():
        """
        Varre vendas pendentes e envia lembrete para a representante (Story 4.3).
        """
        # Buscar vendas pendentes há mais de 24h (Simulado no YOLO com simples query)
        res = await client.execute("""
            SELECT v.id, v.valor_total, r.telegram_id, r.nome as rev_nome, c.nome as cli_nome
            FROM vendas v
            JOIN revendedoras r ON v.revendedora_id = r.id
            JOIN clientes c ON v.cliente_id = c.id
            WHERE v.status = 'pendente'
        """)
        
        tg = TelegramService()
        count = 0
        
        for row in res.rows:
            venda_id, valor, telegram_id, rev_nome, cli_nome = row
            if telegram_id:
                message = (
                    f"⚠️ *Alerta de Inadimplência*\n\n"
                    f"Olá {rev_nome}, a venda para *{cli_nome}* no valor de R$ {valor:.2f} ainda consta como pendente.\n"
                    f"Deseja que eu envie um lembrete para a cliente agora? ✨"
                )
                try:
                    await tg.send_message(int(telegram_id), message)
                    count += 1
                except:
                    logger.warning(f"Não foi possível notificar o telegram {telegram_id}")
        
        return count

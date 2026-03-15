import logging
import uuid

logger = logging.getLogger(__name__)

class NotificationService:
    """
    Serviço central de notificações (WhatsApp, Email, App).
    """

    async def notify_revendedora(self, revendedora_id: uuid.UUID, message_type: str):
        """
        Envia uma notificação para a revendedora (WhatsApp, Telegram, etc).
        """
        logger.info(f"🔔 Notificando revendedora {revendedora_id} sobre: {message_type}")
        
        # 1. Tentar enviar via Telegram se houver vínculo
        try:
            # Em um cenário real, usaríamos uma tarefa Celery ou injetaríamos db_session
            # Para o MVP, registramos a intenção
            pass 
        except Exception as e:
            logger.error(f"Erro ao tentar notificar via Telegram: {e}")

    async def alert_admin(self, title: str, message: str, priority: str = "normal"):
        """
        Envia alertas para o painel administrativo ou canais de suporte.
        """
        logger.warning(f"⚠️ ALERTA ADMIN [{priority.upper()}]: {title} - {message}")
        # TODO: Integrar com Slack ou Firebase Cloud Messaging.
        pass

import logging
import uuid

logger = logging.getLogger(__name__)

class NotificationService:
    """
    Serviço central de notificações (WhatsApp, Email, App).
    """

    async def notify_revendedora(self, revendedora_id: uuid.UUID, message_type: str):
        """
        Envia uma notificação para a revendedora.
        Tipos: 'pagamento_confirmado', 'venda_cancelada', 'saque_processado', etc.
        """
        logger.info(f"🔔 Notificando revendedora {revendedora_id} sobre: {message_type}")
        # TODO: Integrar com API do WhatsApp (BellaZap core) ou serviço de push.
        pass

    async def alert_admin(self, title: str, message: str, priority: str = "normal"):
        """
        Envia alertas para o painel administrativo ou canais de suporte.
        """
        logger.warning(f"⚠️ ALERTA ADMIN [{priority.upper()}]: {title} - {message}")
        # TODO: Integrar com Slack ou Firebase Cloud Messaging.
        pass

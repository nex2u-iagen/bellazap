import logging
import httpx
from typing import Dict, Any, Optional, List
from src.core.config import settings

logger = logging.getLogger(__name__)

class WhatsAppService:
    """
    Serviço centralizado para gestão da Evolution API.
    Permite controle total de instâncias, conexões e mensagens a partir do BellaZap.
    """

    def __init__(self):
        self.base_url = settings.WHATSAPP_API_URL
        self.api_key = settings.WHATSAPP_GLOBAL_API_KEY
        self.headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }

    async def list_instances(self) -> List[Dict[str, Any]]:
        """Lista todas as instâncias existentes na Evolution API."""
        url = f"{self.base_url}/instance/fetchInstances"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def create_instance(self, instance_name: str) -> Dict[str, Any]:
        """Cria e configura uma nova instância."""
        url = f"{self.base_url}/instance/create"
        payload = {
            "instanceName": instance_name,
            "token": None,
            "qrcode": True,
            "webhook_wa_business": False,
            "webhook_enabled": True,
            "webhook_url": f"{settings.API_V1_STR}/whatsapp/webhook" # Direciona para nosso backend
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Instância WhatsApp '{instance_name}' criada e configurada.")
            return response.json()

    async def delete_instance(self, instance_name: str):
        """Remove permanentemente uma instância."""
        url = f"{self.base_url}/instance/delete/{instance_name}"
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Instância '{instance_name}' removida com sucesso.")

    async def get_connection_status(self, instance_name: str) -> str:
        """Verifica se a instância está conectada ao WhatsApp."""
        url = f"{self.base_url}/instance/connectionStatus/{instance_name}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            data = response.json()
            return data.get("instance", {}).get("state", "disconnected")

    async def send_message(self, instance_name: str, number: str, text: str):
        """Envia mensagem para representante ou cliente final."""
        url = f"{self.base_url}/message/sendText/{instance_name}"
        payload = {
            "number": number,
            "options": {"delay": 1000, "presence": "composing"},
            "textMessage": {"text": text}
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.headers)
            return response.json()

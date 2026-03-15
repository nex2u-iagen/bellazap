from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.domains.whatsapp.service import WhatsAppService
from src.domains.whatsapp.interaction_service import InteractionService

router = APIRouter()
whatsapp_service = WhatsAppService()

@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Recebe eventos da Evolution API (mensagens, status, conexões).
    """
    data = await request.json()
    event = data.get("event")
    instance = data.get("instance")
    
    # Focamos no evento de recebimento de mensagem (MESSAGES_UPSERT)
    if event == "messages.upsert":
        msg_data = data.get("data", {})
        message = msg_data.get("message", {})
        
        # Ignorar mensagens enviadas por nós mesmos
        if msg_data.get("key", {}).get("fromMe"):
            return {"status": "ignored_self_message"}

        number = msg_data.get("key", {}).get("remoteJid", "").split("@")[0]
        text = message.get("conversation") or message.get("extendedTextMessage", {}).get("text")
        
        if number and text:
            service = InteractionService(db)
            await service.process_incoming_message(number, text, instance)
            
    return {"status": "processed"}

@router.post("/instance/create")
async def create_instance(instance_name: str):
    """Cria uma nova instância de WhatsApp."""
    try:
        return await whatsapp_service.create_instance(instance_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/instance/qrcode/{instance_name}")
async def get_qrcode(instance_name: str):
    """Busca o QR Code para conexão."""
    try:
        # Nota: assumindo que o método get_qrcode existe no WhatsAppService
        # Caso contrário, precisamos implementá-lo.
        if hasattr(whatsapp_service, 'get_qrcode'):
            return await whatsapp_service.get_qrcode(instance_name)
        return {"error": "Método get_qrcode não implementado no serviço"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send")
async def send_message(instance_name: str, number: str, message: str):
    """Envia uma mensagem via WhatsApp."""
    try:
        return await whatsapp_service.send_message(instance_name, number, message, text=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

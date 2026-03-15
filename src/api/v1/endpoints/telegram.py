from fastapi import APIRouter, Depends, Request, HTTPException, status, Header
from src.core.config import settings
from src.db.session import client as db_client
from src.domains.telegram.service import TelegramService
from src.domains.agentes.service import BellaAgent
from telegram import Update
import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(None)
):
    """Handler para o webhook do Telegram (Serverless Ready)."""
    # YOLO: Tentar pegar segredo do banco
    secret = settings.TELEGRAM_WEBHOOK_SECRET
    try:
        res_secret = await db_client.execute("SELECT value FROM configs WHERE key = 'telegram_webhook_secret'")
        if res_secret.rows:
            secret = res_secret.rows[0][0]
    except:
        pass

    if secret and x_telegram_bot_api_secret_token != secret:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        data = await request.json()
        update = Update.de_json(data, None)
        telegram_id = str(update.effective_user.id)
        
        # 1. Tentar encontrar vínculo na tabela revendedoras
        res = await db_client.execute("SELECT id, nome FROM revendedoras WHERE telegram_id = ?", [telegram_id])
        
        tg_service = TelegramService()
        
        if res.rows:
            # Usuário vinculado
            revendedora_id = res.rows[0][0]
            agent = BellaAgent(revendedora_id=revendedora_id)
            
            user_text = update.message.text if update.message and update.message.text else ""
            if user_text.lower() in ["menu", "/start", "perfil"]:
                await tg_service.send_main_menu(int(telegram_id), f"Olá {res.rows[0][1]}, como posso ajudar hoje?")
            else:
                response = await agent.chat(user_text)
                await tg_service.send_message(int(telegram_id), response)
        else:
            # Fluxo de Vínculo via Email (Story 4.5 Simplificada)
            user_text = update.message.text if update.message and update.message.text else ""
            if user_text.startswith("/vincular"):
                email = user_text.replace("/vincular", "").strip()
                res_vinc = await db_client.execute("SELECT id, nome FROM revendedoras WHERE email = ?", [email])
                if res_vinc.rows:
                    rev_id = res_vinc.rows[0][0]
                    await db_client.execute("UPDATE revendedoras SET telegram_id = ? WHERE id = ?", [telegram_id, rev_id])
                    await tg_service.send_main_menu(int(telegram_id), f"✅ Sucesso! {res_vinc.rows[0][1]}, seu Telegram foi vinculado.")
                else:
                    await tg_service.send_message(int(telegram_id), "❌ Email não encontrado no cadastro BellaZap.")
            else:
                await tg_service.send_message(int(telegram_id), "Bem-vinda à BellaZap! 🤖\n\nPor favor, digite `/vincular seu@email.com` para começar.")

        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        return {"status": "error"}

@router.get("/status")
async def telegram_status():
    token = settings.TELEGRAM_BOT_TOKEN
    try:
        res = await db_client.execute("SELECT value FROM configs WHERE key = 'telegram_bot_token'")
        if res.rows:
            token = res.rows[0][0]
    except:
        pass
    
    return {"bot_configured": token != "SEU_TOKEN_AQUI" and token != ""}

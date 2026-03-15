import httpx
from src.core.config import settings
from src.db.session import client
import uuid
import logging

logger = logging.getLogger(__name__)

class FinanceService:
    ASAAS_URL = "https://sandbox.asaas.com/api/v3" if settings.ASAAS_ENV == "sandbox" else "https://api.asaas.com/v3"

    @staticmethod
    async def generate_pix_venda(revendedora_id: str, valor: float, cliente_id: str):
        """
        Gera uma cobrança PIX no Asaas com Split Automático.
        """
        # 1. Buscar dados do plano para o Split (Story 2.2)
        res_plano = await client.execute(
            "SELECT p.taxa_variavel, p.taxa_fixa FROM planos p JOIN revendedoras r ON r.plano_id = p.id WHERE r.id = ?",
            [revendedora_id]
        )
        if not res_plano.rows:
            taxa_v, taxa_f = 0.05, 1.0 # Fallback 5% + 1 real
        else:
            taxa_v, taxa_f = res_plano.rows[0][0], res_plano.rows[0][1]

        # Cálculo do Split (Plataforma fica com a taxa do plano)
        valor_comissao = (valor * (taxa_v / 100)) + taxa_f
        
        # Payload Asaas (Simplificado para o exemplo YOLO)
        payload = {
            "customer": "cus_000000000000", # No mundo real, buscaria o ID do cliente no Asaas
            "billingType": "PIX",
            "value": valor,
            "dueDate": "2026-12-31",
            "description": f"Venda BellaZap - Rev: {revendedora_id}",
            "split": [
                {
                    "walletId": "ID_CARTEIRA_PLATAFORMA", # Central
                    "fixedValue": valor_comissao
                }
            ]
        }

        # Simulação de chamada API (Story 2.1)
        # Nota: Por ser YOLO e não termos o token real agora, vamos simular o sucesso
        asaas_id = f"pay_{uuid.uuid4().hex[:12]}"
        
        # 2. Registrar venda no banco (Pendente)
        venda_id = str(uuid.uuid4())
        await client.execute(
            "INSERT INTO vendas (id, revendedora_id, cliente_id, valor_total, asaas_billing_id, status) VALUES (?, ?, ?, ?, ?, ?)",
            [venda_id, revendedora_id, cliente_id, valor, asaas_id, "pendente"]
        )

        return {
            "pix_qr_code": "BASE64_MOCKED_QR_CODE",
            "pix_chave": "00020126360014br.gov.bcb.pix0114+5511999999999",
            "asaas_id": asaas_id,
            "status": "pendente"
        }

    @staticmethod
    async def process_webhook(payload: dict, webhook_token: str):
        """
        Processa confirmação de pagamento (Story 2.3) com Idempotência e Segurança.
        """
        # 1. Segurança: Validar Token do Header
        if webhook_token != settings.ASAAS_WEBHOOK_TOKEN:
            logger.warning(f"⚠️ Tentativa de Webhook com token inválido!")
            return False

        event = payload.get("event")
        payment = payload.get("payment", {})
        payment_id = payment.get("id")
        event_id = payload.get("id") # ID único do evento no Asaas

        # 2. Idempotência: Verificar se este evento já foi processado
        res_event = await client.execute("SELECT 1 FROM processed_events WHERE event_id = ?", [event_id])
        if res_event.rows:
            logger.info(f"♻️ Evento {event_id} já processado anteriormente. Ignorando.")
            return True

        # 3. Processamento Lógico
        if event == "PAYMENT_CONFIRMED" or event == "PAYMENT_RECEIVED":
            # Verificar se a venda existe
            res_venda = await client.execute("SELECT status FROM vendas WHERE asaas_billing_id = ?", [payment_id])
            if res_venda.rows:
                # Atualizar status para paga
                await client.execute(
                    "UPDATE vendas SET status = 'paga' WHERE asaas_billing_id = ?",
                    [payment_id]
                )
                logger.info(f"💰 Venda {payment_id} confirmada e split processado.")
        
        # 4. Registrar que o evento foi processado com sucesso
        await client.execute("INSERT INTO processed_events (event_id) VALUES (?)", [event_id])
        return True

    @staticmethod
    async def get_analytics(revendedora_id: str):
        """
        Gera métricas para o dashboard adaptativo (Story 4.6).
        """
        res = await client.execute("""
            SELECT 
                COUNT(*) as total_vendas,
                SUM(valor_total) as faturamento,
                SUM(CASE WHEN status = 'paga' THEN 1 ELSE 0 END) as pagas
            FROM vendas 
            WHERE revendedora_id = ?
        """, [revendedora_id])
        
        if not res.rows:
            return {"vendas": 0, "faturamento": 0, "taxa_conversao": 0}
            
        total, fat, pagas = res.rows[0]
        fat = fat if fat else 0
        conv = (pagas / total * 100) if total > 0 else 0
        
        return {
            "vendas": total,
            "faturamento": fat,
            "taxa_conversao": f"{conv:.1f}%"
        }

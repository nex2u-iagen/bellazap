import logging
import uuid
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.core import Revendedora
from src.domains.agentes.service import BellaAgent
from src.domains.whatsapp.service import WhatsAppService
from src.domains.pagamentos.split_calculator import PlanType

logger = logging.getLogger(__name__)

class InteractionService:
    """Gerencia a orquestração entre WhatsApp, IA e Regras de Negócio."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.whatsapp = WhatsAppService()

    async def process_incoming_message(self, number: str, text: str, instance_name: str):
        """Processa mensagens recebidas do WhatsApp."""
        # 1. Identificar revendedora
        result = await self.db.execute(select(Revendedora).where(Revendedora.telefone == number))
        revendedora = result.scalars().first()

        if not revendedora:
            if text.upper().strip() == "QUERO COMEÇAR":
                return await self._start_onboarding(number, instance_name)
            else:
                return await self.whatsapp.send_message(
                    instance_name, number, 
                    "Olá! Bem-vinda à BellaZap. ✨\n\nIdentificamos que você ainda não tem uma conta. "
                    "Para começar a vender agora mesmo, envie *QUERO COMEÇAR*."
                )

        # 2. Se a revendedora está bloqueada
        if not revendedora.is_active:
            return await self.whatsapp.send_message(
                instance_name, number,
                "Sua conta está suspensa temporariamente. Entre em contato com o suporte admin."
            )

        # 3. Encaminhar para a Bella (IA)
        agent = BellaAgent(revendedora_id=revendedora.id, db_session=self.db)
        response = await agent.chat(text)
        
        # 4. Responder via WhatsApp
        await self.whatsapp.send_message(instance_name, number, response)

    async def _start_onboarding(self, number: str, instance_name: str):
        """Inicia o cadastro simplificado via WhatsApp."""
        logger.info(f"Iniciando onboarding para o número {number}")
        
        # Criação inicial com plano Básico
        nova_revendedora = Revendedora(
            nome="Nova Revendedora", # Poderemos extrair com a IA depois
            email=f"provisorio_{uuid.uuid4().hex[:6]}@bellazap.com",
            cpf_cnpj=f"TEMP_{uuid.uuid4().hex[:8]}",
            telefone=number,
            plano=PlanType.BASIC.value,
            whatsapp_instance=instance_name,
            whatsapp_status="connected"
        )
        
        self.db.add(nova_revendedora)
        await self.db.commit()
        await self.db.refresh(nova_revendedora)
        
        await self.whatsapp.send_message(
            instance_name, number,
            "Parabéns! 🎉 Sua conta BellaZap foi criada com sucesso no plano *Básico*.\n\n"
            "Eu sou a Bella, sua assistente. Você já pode registrar suas vendas enviando mensagens como:\n"
            "_'Vendi um produto de 50 reais para a Maria'_.\n\n"
            "Acesse seu painel web para completar seu cadastro e configurar seus pagamentos!"
        )

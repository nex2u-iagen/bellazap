import logging
from datetime import datetime
from typing import List, Dict
from src.domains.revendedoras.repository import VendaRepository
from src.models.core import Venda

logger = logging.getLogger(__name__)

class ContingencyMode:
    """
    Modo de emergência quando ambos provedores de pagamento estão fora do ar.
    """
    
    def __init__(self, db_session):
        self.db = db_session
        self.venda_repo = VendaRepository(db_session)
    
    async def enter_contingency(self):
        """Ativa o modo de contingência no sistema."""
        logger.critical("🚨 MODO CONTINGÊNCIA ATIVADO - Todos os provedores de pagamento estão offline.")
        # TODO: Implementar Feature Flag global (ex: Redis ou Tabela de Config)
        # await set_feature_flag('payments.disabled', True)
        
        # Notificação para a equipe técnica
        await self._alert_team("ALERTA: Entrando em modo de contingência de pagamentos.")
    
    async def process_contingency_sale(self, venda_data: Dict) -> Dict:
        """
        Registra uma venda em modo de contingência para processamento posterior.
        """
        venda = Venda(
            revendedora_id=venda_data['revendedora_id'],
            valor_total=venda_data['valor_total'],
            status='contingency',
            metadata_={
                'contingency': True,
                'entered_at': datetime.utcnow().isoformat(),
                'original_payload': venda_data
            }
        )
        
        await self.venda_repo.create(venda)
        
        return {
            'status': 'success',
            'mensagem': (
                "✅ Venda registrada com sucesso! Devido a uma instabilidade temporária "
                "nos sistemas de pagamento, o link de cobrança será enviado em breve."
            ),
            'venda_id': str(venda.id)
        }
    
    async def _alert_team(self, message: str):
        """Placeholder para alertas via Slack, Telegram ou PagerDuty."""
        logger.warning(f"Notificação enviada para equipe: {message}")

    async def exit_contingency(self):
        """Processa vendas pendentes e desativa o modo de contingência."""
        # 1. Busca todas vendas em contingência
        pendentes = await self.venda_repo.get_contingency_sales()
        
        logger.info(f"Saindo do modo de contingência. Processando {len(pendentes)} vendas pendentes.")
        
        for venda in pendentes:
            try:
                # TODO: Tentar criar o pagamento novamente via PaymentService
                # Se sucesso, atualiza status para 'pending'
                logger.info(f"Tentando reprocessar venda {venda.id}")
                pass
            except Exception as e:
                logger.error(f"Falha ao reprocessar venda em contingência {venda.id}: {e}")
        
        # 2. Desativa Feature Flag
        # await set_feature_flag('payments.disabled', False)

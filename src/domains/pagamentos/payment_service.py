import logging
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta
import uuid # Importar o módulo uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from src.domains.pagamentos.interfaces import PaymentProvider
from src.domains.pagamentos.providers.asaas import AsaasProvider
from src.domains.pagamentos.providers.abacate import AbacatePayProvider
from src.core.config import settings
from src.models.payment import PaymentProvider as PaymentProviderModel, Transaction, WebhookFailure
from circuitbreaker import circuit # Importar o decorador circuit
from src.domains.pagamentos.split_calculator import PlanType # Importar PlanType

logger = logging.getLogger(__name__)

# Configurações do circuit breaker para o PaymentService
# Este circuit breaker será para o serviço como um todo se ele não conseguir encontrar um provedor saudável
@circuit(failure_threshold=3, recovery_timeout=60, expected_exception=Exception)
class PaymentService:
    """
    Serviço principal de pagamentos com fallback automático
    Gerencia Asaas (primário) e Abacate Pay (fallback)
    """
    
    def __init__(self, db_session: AsyncSession = None):
        self._db_session = db_session # Opcional, para operações de DB
        self.primary: AsaasProvider = AsaasProvider(
            api_key=settings.ASAAS_API_KEY,
            environment=settings.ASAAS_ENV
        )
        self.fallback: AbacatePayProvider = AbacatePayProvider(
            api_key=settings.ABACATE_API_KEY,
            environment=settings.ABACATE_ENV
        )
        
        self.primary_healthy = True
        self.fallback_healthy = True
        self.current_provider_name = "asaas"  # 'asaas' ou 'abacate'
        self.last_health_check = datetime.min
        self.health_check_interval = timedelta(seconds=30)
        
        # Métricas (podem ser substituídas por um sistema de métricas real como Prometheus)
        self.fallback_usage_count = 0
        self.provider_switches = 0
        
    async def _perform_health_checks(self):
        """Executa health checks para ambos os provedores."""
        logger.info("Executando health checks para provedores de pagamento.")
        self.primary_healthy = await self.primary.health_check()
        self.fallback_healthy = await self.fallback.health_check()
        self.last_health_check = datetime.utcnow()
        
        if not self.primary_healthy:
            logger.warning("Provedor primário (Asaas) está unhealthy.")
        if not self.fallback_healthy:
            logger.warning("Provedor fallback (Abacate Pay) está unhealthy.")

    async def get_healthy_provider_instance(self) -> PaymentProvider:
        """
        Retorna a instância do provedor saudável com prioridade para o primário.
        Realiza health checks periodicamente.
        """
        if datetime.utcnow() - self.last_health_check > self.health_check_interval:
            await self._perform_health_checks()

        if self.primary_healthy:
            if self.current_provider_name != "asaas":
                self.current_provider_name = "asaas"
                self.provider_switches += 1
                await self._alert_provider_switch("abacate → asaas")
            return self.primary
        
        if self.fallback_healthy:
            if self.current_provider_name != "abacate":
                self.current_provider_name = "abacate"
                self.provider_switches += 1
                await self._alert_provider_switch("asaas → abacate")
            self.fallback_usage_count += 1
            return self.fallback
        
        await self._alert_critical("AMBOS OS PROVEDORES DE PAGAMENTO ESTÃO FORA DO AR!")
        raise Exception("Nenhum provedor de pagamento disponível.")
    
    async def create_payment_with_split(
        self,
        customer_data: Dict, # Dados para criar/identificar cliente
        amount: float,
        split_rules: List[Dict],
        revendedora_id: uuid.UUID, # Adicionado para registrar a transação
        revendedora_plan: PlanType, # Novo parâmetro para o plano da revendedora
        venda_id: uuid.UUID = None # Opcional, para vincular a uma venda
    ) -> Transaction: # Retorna o objeto da transação criada
        """
        Cria pagamento com split, tentando fallback se necessário.
        """
        provider_instance = await self.get_healthy_provider_instance()
        provider_name = "asaas" if isinstance(provider_instance, AsaasProvider) else "abacate"
        
        try:
            # 0. Verificar limites do plano
            if revendedora_plan == PlanType.BASIC:
                await self._check_plan_limits(revendedora_id)

            # 1. Adaptar dados para o formato do provedor
            # Adaptação para o Asaas (ex: precisa de customerId) ou Abacate
            # Isso pode ser feito dentro do PaymentService ou em um método auxiliar
            
            # Para simplificar o exemplo, vamos usar os dados do cliente diretamente
            # e assumir que o provedor de pagamento vai criar ou usar um existente.
            
            # TODO: Implementar lógica de criação/busca de customer no provedor
            # customer_in_provider = await provider_instance.create_customer(customer_data)
            # customer_id_in_provider = customer_in_provider.get("id")
            
            # Exemplo de payment_data para Asaas:
            # https://www.asaas.com/docs/api/#!/Pagamentos/postPayments
            payment_data = {
                "customer": customer_data.get("id"), # ID do cliente no Asaas, se existir
                "billingType": "PIX", # Exemplo
                "value": amount,
                "dueDate": (datetime.utcnow() + timedelta(days=1)).isoformat()[:10],
                "description": "Pagamento de Venda BellaZap",
                "externalReference": str(venda_id) if venda_id else None,
                # Outros campos necessários...
            }
            
            if provider_name == "abacate":
                 # O Abacate Pay no exemplo do prompt aceita split na criação do pagamento.
                 # Então, as split_rules seriam passadas diretamente no payment_data para ele.
                 payment_data["split"] = split_rules
            
            # 2. Cria pagamento
            payment_response = await provider_instance.create_payment(payment_data)
            
            # 3. Configura split (se o provedor exigir após a criação)
            if provider_name == "asaas" and split_rules:
                await provider_instance.create_split(payment_response['id'], split_rules)
            
            # 4. Calcular margens para a transação no banco de dados
            # TODO: Obter o plano da revendedora para usar o SplitCalculator
            from src.domains.pagamentos.split_calculator import SplitCalculator
            split_calc = SplitCalculator(revendedora_plan) 
            margins = split_calc.get_platform_margin(amount, provider_name)

            # 5. Registrar transação no banco de dados
            if not self._db_session:
                 raise Exception("Sessão de banco de dados não fornecida ao PaymentService.")
            
            provider_db_obj = await self._db_session.execute(
                select(PaymentProviderModel).filter_by(name=provider_name)
            )
            provider_db_obj = provider_db_obj.scalar_one_or_none()

            from decimal import Decimal # Importar Decimal para verificar o tipo
            # Serializar split_rules para uma lista de dicionários Python (compatível com JSON)
            # e converter objetos Decimal para float
            final_split_rules_json_compatible = []
            for rule in split_rules: # Iterar sobre os modelos Pydantic SplitRule
                rule_dict = rule.model_dump()
                new_rule_dict = {}
                for key, value in rule_dict.items():
                    if isinstance(value, Decimal):
                        new_rule_dict[key] = float(value) # Converter Decimal para float
                    else:
                        new_rule_dict[key] = value
                final_split_rules_json_compatible.append(new_rule_dict)

            transaction = Transaction(
                revendedora_id=revendedora_id,
                venda_id=venda_id,
                provider_id=provider_db_obj.id if provider_db_obj else None,
                provider_payment_id=payment_response.get('id'),
                valor_bruto=amount,
                taxa_plataforma=margins['platform_net'],
                taxa_provider=margins['provider_fee_value'],
                valor_liquido_revendedora=margins['revendedora_net'],
                split_config=final_split_rules_json_compatible, # <-- Corrigido aqui
                status='pending', # O status inicial é pendente até o webhook confirmar
            )
            self._db_session.add(transaction)
            await self._db_session.commit()
            await self._db_session.refresh(transaction)
            
            return transaction
            
        except Exception as e:
            logger.error(f"Erro ao criar pagamento com {provider_name}: {e}")
            raise # Re-raise para que o chamador possa lidar com o erro (ex: entrar em contingência)
    
    async def process_webhook(self, payload: Dict, provider_name_hint: str = None) -> Dict:
        """
        Processa webhook, tentando identificar o provedor ou usando a dica.
        """
        provider_instance: Optional[PaymentProvider] = None
        identified_provider_name: Optional[str] = None

        if provider_name_hint == "asaas":
            provider_instance = self.primary
            identified_provider_name = "asaas"
        elif provider_name_hint == "abacate":
            provider_instance = self.fallback
            identified_provider_name = "abacate"
        else:
            # Tenta identificar pelo payload
            if 'event' in payload and 'payment' in payload and 'id' in payload.get('payment', {}): # Exemplo para Asaas
                provider_instance = self.primary
                identified_provider_name = "asaas"
            elif 'event' in payload and 'charge' in payload and 'id' in payload.get('charge', {}): # Exemplo para Abacate
                provider_instance = self.fallback
                identified_provider_name = "abacate"
            
        if not provider_instance:
            logger.error(f"Não foi possível identificar o provedor do webhook com payload: {payload}")
            if self._db_session:
                await self._log_webhook_failure(None, payload, "Provedor não identificado")
            raise Exception("Provedor de webhook desconhecido.")

        try:
            processed_data = await provider_instance.process_webhook(payload)
            # TODO: Atualizar status da transação no DB com base em `processed_data`
            logger.info(f"Webhook de {identified_provider_name} processado: {processed_data}")
            return processed_data
        except Exception as e:
            logger.error(f"Falha ao processar webhook de {identified_provider_name}: {e}")
            if self._db_session:
                provider_db_obj = await self._db_session.execute(
                    select(PaymentProviderModel).filter_by(name=identified_provider_name)
                )
                provider_db_obj = provider_db_obj.scalar_one_or_none()
                await self._log_webhook_failure(
                    provider_db_obj.id if provider_db_obj else None, 
                    payload, 
                    str(e)
                )
            raise

    async def _log_provider_failure(self, provider_name: str):
        """Registra falha do provedor."""
        logger.error(f"🔴 Provedor de pagamento '{provider_name}' falhou ou está unhealthy.")
        # TODO: Enviar métrica para Prometheus, emitir alerta...
    
    async def _alert_provider_switch(self, message: str):
        """Alerta time sobre troca de provedor."""
        logger.warning(f"🔄 ALERTA: Troca de provedor de pagamento: {message}")
        # TODO: Integrar com Slack/PagerDuty
    
    async def _alert_critical(self, message: str):
        """Alerta crítico - ambos provedores fora."""
        logger.critical(f"🚨 ALERTA CRÍTICO: {message}")
        # TODO: Integrar com SMS/PagerDuty urgente
    
    async def _check_plan_limits(self, revendedora_id: uuid.UUID):
        """Verifica se a revendedora atingiu o limite de vendas do plano Básico (50/mês)."""
        first_day = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        stmt = select(func.count(Transaction.id)).where(
            Transaction.revendedora_id == revendedora_id,
            Transaction.created_at >= first_day
        )
        result = await self._db_session.execute(stmt)
        count = result.scalar()
        
        if count >= 50:
            logger.warning(f"Revendedora {revendedora_id} atingiu o limite do plano Básico.")
            raise Exception("Você atingiu o limite de 50 vendas do plano Básico este mês. Faça um upgrade para continuar vendendo! 🚀")

    async def _log_webhook_failure(self, provider_id: uuid.UUID, payload: Dict, error: str):
        """Registra um webhook falho na Dead Letter Queue."""
        if not self._db_session:
            logger.error(f"Não foi possível registrar falha de webhook no DB: {error}")
            return
        
        webhook_fail = WebhookFailure(
            provider_id=provider_id,
            payload=payload,
            error=error,
            status='pending'
        )
        self._db_session.add(webhook_fail)
        await self._db_session.commit()
        await self._db_session.refresh(webhook_fail)
        logger.warning(f"Webhook falho registrado na DLQ. ID: {webhook_fail.id}")

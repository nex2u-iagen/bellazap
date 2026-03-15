from enum import Enum
from typing import Dict, List, Any

class PlanType(str, Enum):
    BASIC = "basico"
    PRO = "pro"
    PREMIUM = "premium"

class SplitCalculator:
    """
    Calcula regras de split baseado no plano da revendedora
    Adapta para cada provider (Asaas vs Abacate)
    """
    
    # Taxas por plano (já descontando Asaas/Abacate)
    PLAN_RATES = {
        PlanType.BASIC: {
            'platform_rate': 10.0,  # 10% sua taxa
            'asaas_fee_percent': 1.99,      # repassado
            'abacate_fee_percent': 1.5,     # repassado (Abacate é mais barato)
        },
        PlanType.PRO: {
            'platform_rate': 8.0,
            'asaas_fee_percent': 1.99,
            'abacate_fee_percent': 1.5,
        },
        PlanType.PREMIUM: {
            'platform_rate': 6.0,
            'asaas_fee_percent': 1.99,
            'abacate_fee_percent': 1.5,
        }
    }
    
    def __init__(self, revendedora_plano: PlanType):
        if revendedora_plano not in self.PLAN_RATES:
            raise ValueError(f"Plano '{revendedora_plano}' inválido.")
        self.rates = self.PLAN_RATES[revendedora_plano]
    
    def calculate_split_asaas(
        self, 
        amount: float, 
        revendedora_wallet_id: str,
        platform_wallet_id: str
    ) -> List[Dict[str, Any]]:
        """
        Retorna regras de split no formato Asaas.
        O Asaas usa 'fixedValue' para o valor a ser enviado para cada subconta.
        O valor da taxa Asaas é geralmente cobrado do pagador principal,
        e no split, as subcontas recebem seus valores líquidos.
        Aqui, o exemplo repassa a taxa do Asaas para a plataforma como custo.
        """
        # Plataforma ganha sua %
        platform_revenue = amount * (self.rates['platform_rate'] / 100)
        
        # Taxa do provedor Asaas (custo para a plataforma, exemplo)
        asaas_fee_value = amount * (self.rates['asaas_fee_percent'] / 100)
        
        # O que sobra para a revendedora
        revendedora_revenue = amount - platform_revenue - asaas_fee_value
        
        # Asaas espera uma lista de objetos 'split'
        # Cada item é para uma conta que NÃO é a conta principal.
        # Se a conta principal for a da plataforma, então só enviamos o da revendedora.
        # Se a conta principal for da revendedora, enviamos para a plataforma.
        # Supondo que a conta principal de origem seja a da plataforma.
        
        return [
            {
                'walletId': revendedora_wallet_id, # ID da carteira da revendedora no Asaas
                'value': round(revendedora_revenue, 2),
                'description': 'Saldo revendedora'
            },
            # A taxa da plataforma e a taxa do Asaas ficam na conta da plataforma (principal)
            # ou você pode fazer um split para uma sub-conta específica da taxa Asaas
            # se Asaas tiver essa funcionalidade. No exemplo, as fees ficam com a plataforma.
            # O Asaas não costuma ter um 'walletId' para "taxa do Asaas", essa é uma dedução.
            # Se for para mandar para uma conta de "taxas" da plataforma:
            # {
            #     'walletId': platform_fee_wallet_id,
            #     'value': round(platform_revenue + asaas_fee_value, 2),
            #     'description': 'Taxas e repasses da plataforma'
            # }
            # O exemplo do prompt sugeria 3 splits, vou seguir o prompt, mas o Asaas pode variar.
            # Se a conta de origem da cobrança for a da plataforma:
            {
                'walletId': platform_wallet_id,
                'value': round(platform_revenue + asaas_fee_value, 2), # Plataforma recebe sua % + o valor da taxa do Asaas que é repassado para ela pagar.
                'description': 'Taxa Plataforma + Repasse Asaas'
            }
        ]

    def calculate_split_abacate(
        self,
        amount: float,
        revendedora_id: str,
        platform_id: str
    ) -> List[Dict[str, Any]]:
        """
        Retorna regras de split no formato Abacate Pay (hipotético).
        O Abacate permite split percentual diretamente.
        """
        platform_percent = self.rates['platform_rate']
        abacate_fee_percent = self.rates['abacate_fee_percent']
        
        # A porcentagem para a revendedora é o restante.
        revendedora_percent = 100.0 - platform_percent - abacate_fee_percent
        
        return [
            {
                'recipient_id': revendedora_id,
                'percentage': round(revendedora_percent, 2),
                'description': 'Saldo revendedora'
            },
            {
                'recipient_id': platform_id,
                'percentage': round(platform_percent + abacate_fee_percent, 2), # Plataforma recebe sua % + a % da taxa do Abacate para cobrir o custo.
                'description': 'Taxa Plataforma + Repasse Abacate'
            }
        ]

    def get_platform_margin(self, amount: float, provider_name: str) -> Dict[str, float]:
        """
        Calcula margem líquida da plataforma por transação
        """
        platform_rate = self.rates['platform_rate']
        
        if provider_name == "asaas":
            provider_fee_percent = self.rates['asaas_fee_percent']
        elif provider_name == "abacate":
            provider_fee_percent = self.rates['abacate_fee_percent']
        else:
            raise ValueError(f"Provedor '{provider_name}' desconhecido para cálculo de margem.")
        
        platform_gross = amount * (platform_rate / 100)
        provider_fee_value = amount * (provider_fee_percent / 100)
        
        # A margem líquida da plataforma é a taxa dela, pois o custo do provider é repassado/considerado.
        platform_net = platform_gross
        
        revendedora_net = amount - platform_gross - provider_fee_value
        
        return {
            'amount': amount,
            'platform_gross': platform_gross,
            'provider_fee_value': provider_fee_value,
            'platform_net': platform_net,
            'revendedora_net': revendedora_net,
            'effective_margin_percent': platform_rate
        }

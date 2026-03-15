from typing import Dict, Any, List
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from circuitbreaker import circuit

from src.domains.pagamentos.interfaces import PaymentProvider
from src.core.config import settings

class AsaasProvider(PaymentProvider):
    """Implementação primária - Asaas"""
    
    def __init__(self, api_key: str, environment: str = "sandbox"):
        self.api_key = api_key
        self.base_url = "https://sandbox.asaas.com/api/v3" if environment == "sandbox" else "https://api.asaas.com/v3"
        # Usar httpx.AsyncClient para melhor integração com FastAPI
        self.client = httpx.AsyncClient() 
        self.headers = {
            "access_token": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def create_customer(self, customer_data: Dict) -> Dict:
        # Implementação para criar cliente no Asaas
        # Ex: https://www.asaas.com/docs/api/#!/Clientes/postCustomers
        async with self.client.post(
            f"{self.base_url}/customers",
            json=customer_data,
            headers=self.headers
        ) as resp:
            resp.raise_for_status() # Lança exceção para status 4xx/5xx
            return resp.json()

    # Aplica circuit breaker e retry para métodos críticos
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=httpx.HTTPStatusError)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    async def create_payment(self, payment_data: Dict) -> Dict:
        """Cria cobrança no Asaas com retry automático"""
        async with self.client.post(
            f"{self.base_url}/payments",
            json=payment_data,
            headers=self.headers
        ) as resp:
            resp.raise_for_status()
            return resp.json()

    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=httpx.HTTPStatusError)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    async def get_payment_status(self, payment_id: str) -> Dict:
        """Consulta status do pagamento no Asaas"""
        async with self.client.get(
            f"{self.base_url}/payments/{payment_id}",
            headers=self.headers
        ) as resp:
            resp.raise_for_status()
            return resp.json()

    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=httpx.HTTPStatusError)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    async def create_split(self, payment_id: str, split_rules: List[Dict]) -> Dict:
        """Configura split no Asaas"""
        # O endpoint de split do Asaas é separado do de criação de pagamento
        # O payload pode variar ligeiramente, adaptando ao exemplo fornecido.
        async with self.client.post(
            f"{self.base_url}/payments/{payment_id}/split",
            json={"split": split_rules}, # Adaptação do payload para o exemplo
            headers=self.headers
        ) as resp:
            resp.raise_for_status()
            return resp.json()
    
    async def process_webhook(self, payload: Dict) -> Dict:
        """
        Processa webhook do Asaas. 
        Normalmente, aqui você validaria a assinatura do webhook e processaria os eventos.
        Retorna um dicionário com o status processado.
        """
        # Exemplo simplificado. Em um cenário real, você verificaria a autenticidade do webhook.
        event_type = payload.get("event")
        payment_status = payload.get("payment", {}).get("status")
        # Lógica de processamento de webhook...
        return {"status": "processed", "event_type": event_type, "payment_status": payment_status}

    async def health_check(self) -> bool:
        """Verifica se API do Asaas está respondendo"""
        try:
            # Não há um endpoint de health dedicado no Asaas publicamente,
            # então tentamos um endpoint leve como listar clientes.
            # Ou apenas um GET na base_url se ele permitir sem autenticação para um health check básico.
            async with self.client.get(
                f"{self.base_url}/customers?limit=1", # Tentativa de endpoint leve
                headers=self.headers,
                timeout=5
            ) as resp:
                return resp.status_code == 200
        except httpx.HTTPStatusError:
            return False
        except httpx.RequestError: # Erro de conexão, timeout, etc.
            return False


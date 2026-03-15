from typing import Dict, Any, List
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from circuitbreaker import circuit

from src.domains.pagamentos.interfaces import PaymentProvider
from src.core.config import settings

class AbacatePayProvider(PaymentProvider):
    """Implementação fallback - Abacate Pay"""
    
    def __init__(self, api_key: str, environment: str = "sandbox"):
        self.api_key = api_key
        # Usar uma URL hipotética mais consistente para sandbox/produção
        self.base_url = "https://sandbox.api.abacatepay.com/v1" if environment == "sandbox" else "https://api.abacatepay.com/v1"
        self.client = httpx.AsyncClient()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_customer(self, customer_data: Dict) -> Dict:
        # Implementação para criar cliente no Abacate Pay (hipotético)
        async with self.client.post(
            f"{self.base_url}/customers",
            json=customer_data,
            headers=self.headers
        ) as resp:
            resp.raise_for_status()
            return resp.json()

    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=httpx.HTTPStatusError)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    async def create_payment(self, payment_data: Dict) -> Dict:
        """Cria cobrança no Abacate Pay"""
        # Adapta formato do Asaas para Abacate (exemplo do prompt)
        adapted_data = {
            "amount": payment_data.get("value"),
            "payer": {
                "name": payment_data.get("customerName"), # Adaptar para campos do Asaas
                "tax_id": payment_data.get("cpfCnpj") # Adaptar para campos do Asaas
            },
            "methods": ["pix"],
            "split": payment_data.get("split", []) # Abacate já aceita split na criação
        }
        
        async with self.client.post(
            f"{self.base_url}/charges",
            json=adapted_data,
            headers=self.headers
        ) as resp:
            resp.raise_for_status()
            return resp.json()
    
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=httpx.HTTPStatusError)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
    async def get_payment_status(self, payment_id: str) -> Dict:
        """Consulta status do pagamento no Abacate Pay (hipotético)"""
        async with self.client.get(
            f"{self.base_url}/charges/{payment_id}",
            headers=self.headers
        ) as resp:
            resp.raise_for_status()
            return resp.json()
    
    async def create_split(self, payment_id: str, split_rules: List[Dict]) -> Dict:
        """
        No Abacate Pay, o split é normalmente enviado junto com a criação do pagamento.
        Esta função pode ser um no-op ou levantar um erro se for chamada separadamente.
        Depende da documentação real da Abacate Pay.
        Por enquanto, retorna um placeholder indicando que não é necessário.
        """
        return {"message": "Split handled during payment creation for Abacate Pay."}

    async def process_webhook(self, payload: Dict) -> Dict:
        """
        Processa webhook do Abacate Pay.
        Similar ao Asaas, aqui você validaria a assinatura e processaria os eventos.
        """
        event_type = payload.get("event")
        charge_status = payload.get("charge", {}).get("status")
        return {"status": "processed", "event_type": event_type, "charge_status": charge_status}
    
    async def health_check(self) -> bool:
        """Verifica se Abacate Pay está saudável"""
        try:
            # Endpoint de health check hipotético
            async with self.client.get(
                f"{self.base_url}/health",
                headers=self.headers, # Pode não precisar de auth para health
                timeout=5
            ) as resp:
                return resp.status_code == 200
        except httpx.HTTPStatusError:
            return False
        except httpx.RequestError:
            return False

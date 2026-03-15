from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio
from circuitbreaker import circuit
from tenacity import retry, stop_after_attempt, wait_exponential

class PaymentProvider(ABC):
    """Interface comum para todos os provedores de pagamento"""
    
    @abstractmethod
    async def create_customer(self, customer_data: Dict) -> Dict:
        """Cria cliente no provedor"""
        pass
    
    @abstractmethod
    async def create_payment(self, payment_data: Dict) -> Dict:
        """Cria cobrança/PIX"""
        pass
    
    @abstractmethod
    async def get_payment_status(self, payment_id: str) -> Dict:
        """Consulta status do pagamento"""
        pass
    
    @abstractmethod
    async def create_split(self, payment_id: str, split_rules: List[Dict]) -> Dict:
        """Configura split de pagamento"""
        pass
    
    @abstractmethod
    async def process_webhook(self, payload: Dict) -> Dict:
        """Processa webhook do provedor"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Verifica se provedor está saudável"""
        pass

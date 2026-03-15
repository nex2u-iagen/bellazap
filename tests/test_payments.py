import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.core import Revendedora, Venda
from src.models.payment import PaymentProvider as DBPaymentProvider, Transaction
from src.domains.pagamentos.split_calculator import PlanType
import uuid
from unittest.mock import AsyncMock, patch

# Fixture para criar uma revendedora para testes
@pytest.fixture
async def test_revendedora(db_session: AsyncSession) -> Revendedora:
    revendedora = Revendedora(
        id=uuid.uuid4(),
        nome="Revendedora Teste",
        email="teste@revendedora.com",
        cpf_cnpj="12345678900",
        plano=PlanType.BASIC.value
    )
    db_session.add(revendedora)
    await db_session.commit()
    await db_session.refresh(revendedora)
    return revendedora

# Fixture para configurar provedores de pagamento no DB
@pytest.fixture
async def setup_payment_providers(db_session: AsyncSession):
    asaas_provider = DBPaymentProvider(name="asaas", priority=1, is_active=True)
    abacate_provider = DBPaymentProvider(name="abacate", priority=2, is_active=True)
    db_session.add_all([asaas_provider, abacate_provider])
    await db_session.commit()
    await db_session.refresh(asaas_provider)
    await db_session.refresh(abacate_provider)
    return asaas_provider, abacate_provider

@pytest.mark.asyncio
@patch('src.domains.pagamentos.providers.abacate.AbacatePayProvider.health_check', new_callable=AsyncMock)
@patch('src.domains.pagamentos.providers.asaas.AsaasProvider.health_check', new_callable=AsyncMock)
@patch('src.domains.pagamentos.providers.asaas.AsaasProvider.create_split', new_callable=AsyncMock)
@patch('src.domains.pagamentos.providers.asaas.AsaasProvider.create_payment', new_callable=AsyncMock)
async def test_create_payment_success_asaas(
    mock_create_payment_asaas, mock_create_split_asaas, mock_health_check_asaas, mock_health_check_abacate,
    client: AsyncClient,
    test_revendedora: Revendedora,
    setup_payment_providers,
    db_session: AsyncSession
):
    asaas_provider, _ = setup_payment_providers

    mock_health_check_asaas.return_value = True
    mock_health_check_abacate.return_value = True # Ambos saudáveis, Asaas será primário

    mock_create_payment_asaas.return_value = {
        "id": "pay_asaas_123",
        "invoiceUrl": "http://asaas.com/invoice/123",
        "status": "PENDING"
    }
    mock_create_split_asaas.return_value = {"success": True}

    payment_payload = {
        "revendedora_id": str(test_revendedora.id),
        "amount": 100.00,
        "customer_data": {"name": "Cliente Teste", "email": "cliente@teste.com", "cpfCnpj": "11122233344"},
        "split_rules": [
            {"wallet_id": "rev_wallet_1", "value": 80.00},
            {"wallet_id": "plat_wallet_1", "value": 20.00}
        ]
    }

    response = await client.post("/api/v1/payments/", json=payment_payload)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["provider_name"] == "asaas"
    assert response_data["provider_payment_id"] == "pay_asaas_123"
    assert response_data["status"] == "pending" # Status inicial
    assert float(response_data["amount"]) == 100.00
    mock_create_payment_asaas.assert_called_once()
    mock_create_split_asaas.assert_called_once()

    # Verificar se a transação foi salva no DB
    transaction = await db_session.get(
        Transaction,
        uuid.UUID(response_data["id"]) # CONVERTENDO PARA UUID
    )
    assert transaction is not None
    assert str(transaction.provider_payment_id) == "pay_asaas_123" # Conversão para string
    assert transaction.provider_id == asaas_provider.id
    assert float(transaction.valor_bruto) == 100.00 # Comparar como float


@pytest.mark.asyncio
@patch('src.domains.pagamentos.providers.abacate.AbacatePayProvider.health_check', new_callable=AsyncMock)
@patch('src.domains.pagamentos.providers.asaas.AsaasProvider.health_check', new_callable=AsyncMock)
@patch('src.domains.pagamentos.providers.abacate.AbacatePayProvider.create_payment', new_callable=AsyncMock)
@patch('src.domains.pagamentos.providers.asaas.AsaasProvider.create_payment', new_callable=AsyncMock)
async def test_create_payment_fallback_to_abacate(
    mock_create_payment_asaas, mock_create_payment_abacate, mock_health_check_asaas, mock_health_check_abacate,
    client: AsyncClient,
    test_revendedora: Revendedora,
    setup_payment_providers,
    db_session: AsyncSession
):
    _, abacate_provider = setup_payment_providers # Corrigir a desestruturação

    mock_health_check_asaas.return_value = False # Asaas unhealthy
    mock_health_check_abacate.return_value = True # Abacate healthy

    mock_create_payment_abacate.return_value = {
        "id": "charge_abacate_456",
        "link": "http://abacatepay.com/charge/456",
        "status": "WAITING_PAYMENT"
    }
    # Abacate Pay não tem create_split separado no exemplo, é no create_payment

    payment_payload = {
        "revendedora_id": str(test_revendedora.id),
        "amount": 50.00,
        "customer_data": {"name": "Cliente Fallback", "email": "fallback@teste.com", "cpfCnpj": "99988877766"},
        "split_rules": [
            {"wallet_id": "rev_wallet_f", "value": 40.00},
            {"wallet_id": "plat_wallet_f", "value": 10.00}
        ]
    }

    response = await client.post("/api/v1/payments/", json=payment_payload)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["provider_name"] == "abacate"
    assert response_data["provider_payment_id"] == "charge_abacate_456"
    assert response_data["status"] == "pending"
    assert float(response_data["amount"]) == 50.00
    mock_create_payment_asaas.assert_not_called() # Asaas não deve ser chamado
    mock_create_payment_abacate.assert_called_once()
    
    # Verificar se a transação foi salva no DB
    transaction = await db_session.get(
        Transaction,
        uuid.UUID(response_data["id"]) # CONVERTENDO PARA UUID
    )
    assert transaction is not None
    assert str(transaction.provider_payment_id) == "charge_abacate_456" # Conversão para string
    assert transaction.provider_id == abacate_provider.id
    assert float(transaction.valor_bruto) == 50.00 # Comparar como float


@pytest.mark.asyncio
@patch('src.domains.pagamentos.providers.abacate.AbacatePayProvider.health_check', new_callable=AsyncMock)
@patch('src.domains.pagamentos.providers.asaas.AsaasProvider.health_check', new_callable=AsyncMock)
async def test_create_payment_all_providers_unhealthy(
    mock_health_check_asaas, mock_health_check_abacate,
    client: AsyncClient,
    test_revendedora: Revendedora,
    setup_payment_providers,
    db_session: AsyncSession
):
    mock_health_check_asaas.return_value = False
    mock_health_check_abacate.return_value = False

    payment_payload = {
        "revendedora_id": str(test_revendedora.id),
        "amount": 200.00,
        "customer_data": {"name": "Cliente Offline", "email": "offline@teste.com", "cpfCnpj": "11122233344"},
        "split_rules": []
    }

    response = await client.post("/api/v1/payments/", json=payment_payload)

    assert response.status_code == 500
    assert "Nenhum provedor de pagamento disponível." in response.json()["detail"]
    mock_health_check_asaas.assert_called_once()
    mock_health_check_abacate.assert_called_once()

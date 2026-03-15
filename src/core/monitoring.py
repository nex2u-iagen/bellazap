from prometheus_client import Counter, Gauge, Histogram, generate_latest

# --- Métricas de Infraestrutura e Integrações ---

# Contador de pagamentos por provedor e status (asaas/abacate, success/failed)
payments_total = Counter(
    'bellazap_payments_total', 
    'Total de tentativas de pagamento', 
    ['provider', 'status']
)

# Contador de falhas específicas por motivo
payments_failed = Counter(
    'bellazap_payments_failed_total', 
    'Pagamentos falhos detalhados', 
    ['provider', 'reason']
)

# Status de saúde do provedor (1 = Healthy, 0 = Unhealthy)
provider_health = Gauge(
    'bellazap_provider_health', 
    'Status de saúde dos provedores de pagamento', 
    ['provider']
)

# Uso do Fallback (ex: de asaas para abacate)
fallback_usage = Counter(
    'bellazap_fallback_usage_total', 
    'Uso do sistema de fallback automático', 
    ['from_provider', 'to_provider']
)

# Latência das chamadas de API de pagamento
payment_latency = Histogram(
    'bellazap_payment_api_latency_seconds', 
    'Latência das requisições aos provedores de pagamento', 
    ['provider']
)

# --- Métricas de Negócio e Operação ---

# Monthly Recurring Revenue (MRR) - Segmentado por plano (Básico, Pro, Premium)
mrr = Gauge(
    'bellazap_mrr_reais', 
    'Receita recorrente mensal estimada por plano', 
    ['plan']
)

# Número de revendedoras ativas
active_revendedoras = Gauge(
    'bellazap_active_revendedoras_total', 
    'Quantidade total de revendedoras ativas'
)

# Transações que estão no limbo (pending)
pending_transactions = Gauge(
    'bellazap_transactions_pending_total', 
    'Quantidade de transações pendentes de confirmação'
)

# Webhooks na Dead Letter Queue que aguardam reprocessamento ou intervenção
webhook_dead_letter = Gauge(
    'bellazap_webhook_dlq_total', 
    'Quantidade de webhooks falhos na Dead Letter Queue'
)

def get_metrics():
    """Retorna as métricas formatadas para o Prometheus (usado em endpoints HTTP)."""
    return generate_latest()

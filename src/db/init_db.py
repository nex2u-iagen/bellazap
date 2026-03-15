from src.db.session import client
import logging

logger = logging.getLogger(__name__)

async def init_tables():
    """
    Cria as tabelas fundamentais no Turso (LibSQL).
    """
    try:
        # Tabela de Planos
        await client.execute("""
            CREATE TABLE IF NOT EXISTS planos (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                taxa_fixa REAL DEFAULT 0,
                taxa_variavel REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Tabela de Auditoria (Audit Trail)
        await client.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id TEXT PRIMARY KEY,
                entidade TEXT NOT NULL,
                entidade_id TEXT,
                acao TEXT NOT NULL,
                dados_anteriores TEXT,
                dados_novos TEXT,
                usuario_admin TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Tabela de Representantes (Revendedoras)
        await client.execute("""
            CREATE TABLE IF NOT EXISTS revendedoras (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                cpf_cnpj TEXT UNIQUE NOT NULL,
                plano_id TEXT,
                telegram_id TEXT UNIQUE,
                asaas_access_token TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plano_id) REFERENCES planos(id)
            );
        """)

        # Tabela de Clientes
        await client.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id TEXT PRIMARY KEY,
                revendedora_id TEXT NOT NULL,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                endereco TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (revendedora_id) REFERENCES revendedoras(id)
            );
        """)

        # Tabela de Catálogo Global
        await client.execute("""
            CREATE TABLE IF NOT EXISTS catalogo_global (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco_sugerido REAL,
                imagem_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Tabela de Estoque Local
        await client.execute("""
            CREATE TABLE IF NOT EXISTS estoque_local (
                id TEXT PRIMARY KEY,
                revendedora_id TEXT NOT NULL,
                produto_global_id TEXT NOT NULL,
                quantidade INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (revendedora_id) REFERENCES revendedoras(id),
                FOREIGN KEY (produto_global_id) REFERENCES catalogo_global(id)
            );
        """)

        # Tabela de Vendas
        await client.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id TEXT PRIMARY KEY,
                revendedora_id TEXT NOT NULL,
                cliente_id TEXT NOT NULL,
                valor_total REAL NOT NULL,
                status TEXT DEFAULT 'pendente',
                asaas_billing_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (revendedora_id) REFERENCES revendedoras(id),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            );
        """)

        # Tabela de Eventos Processados (Idempotência Webhook)
        await client.execute("""
            CREATE TABLE IF NOT EXISTS processed_events (
                event_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        logger.info("✅ Tabelas inicializadas com sucesso no Turso.")
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar tabelas: {str(e)}")
        raise e

from src.db.session import client
from src.domains.admin.schemas import PlanoCreate, RevendedoraCreate
import uuid
import logging

logger = logging.getLogger(__name__)

class AdminService:
    @staticmethod
    async def create_plano(plano: PlanoCreate):
        plano_id = str(uuid.uuid4())
        try:
            await client.execute(
                "INSERT INTO planos (id, nome, taxa_fixa, taxa_variavel) VALUES (?, ?, ?, ?)",
                [plano_id, plano.nome, plano.taxa_fixa, plano.taxa_variavel]
            )
            # Registrar na auditoria
            await client.execute(
                "INSERT INTO audit_log (id, entidade, entidade_id, acao, dados_novos) VALUES (?, ?, ?, ?, ?)",
                [str(uuid.uuid4()), "plano", plano_id, "CREATE", str(plano.dict())]
            )
            logger.info(f"🛡️ Audit Trail: Plano {plano.nome} criado com ID {plano_id}")
            return {"id": plano_id, **plano.dict()}
        except Exception as e:
            logger.error(f"Erro ao criar plano: {e}")
            raise e

    @staticmethod
    async def list_planos():
        result = await client.execute("SELECT * FROM planos")
        return [dict(row) for row in result.rows]

    @staticmethod
    async def create_revendedora(rev: RevendedoraCreate):
        rev_id = f"rev_{uuid.uuid4().hex[:8]}"
        try:
            await client.execute(
                "INSERT INTO revendedoras (id, nome, email, cpf_cnpj, plano_id, telegram_id, asaas_access_token) VALUES (?, ?, ?, ?, ?, ?, ?)",
                [rev_id, rev.nome, rev.email, rev.cpf_cnpj, rev.plano_id, rev.telegram_id, rev.asaas_access_token]
            )
            logger.info(f"✅ Revendedora {rev.nome} cadastrada com ID {rev_id}")
            return {"id": rev_id, **rev.dict()}
        except Exception as e:
            logger.error(f"Erro ao cadastrar revendedora: {e}")
            raise e

    @staticmethod
    async def get_revendedora_by_telegram(telegram_id: str):
        result = await client.execute(
            "SELECT * FROM revendedoras WHERE telegram_id = ?",
            [telegram_id]
        )
        if result.rows:
            return dict(result.rows[0])
        return None

    @staticmethod
    async def list_revendedoras():
        result = await client.execute("SELECT r.id, r.nome, r.telegram_id as telefone, p.nome as plano, COALESCE(r.is_active, 1) as is_active FROM revendedoras r LEFT JOIN planos p ON r.plano_id = p.id")
        return [dict(row) for row in result.rows]

    @staticmethod
    async def toggle_active(rev_id: str):
        result = await client.execute("SELECT COALESCE(is_active, 1) as is_active FROM revendedoras WHERE id = ?", [rev_id])
        if not result.rows:
            raise Exception("Revendedora não encontrada")
        current = result.rows[0][0]
        new_val = 0 if current else 1
        await client.execute("UPDATE revendedoras SET is_active = ? WHERE id = ?", [new_val, rev_id])
        return {"id": rev_id, "is_active": new_val}

    @staticmethod
    async def delete_revendedora(rev_id: str):
        await client.execute("DELETE FROM revendedoras WHERE id = ?", [rev_id])
        return {"detail": "Deleted"}

    @staticmethod
    async def get_revendedora_summary(rev_id: str):
        rev = await client.execute("SELECT * FROM revendedoras WHERE id = ?", [rev_id])
        if not rev.rows:
            raise Exception("Not found")
        data = dict(rev.rows[0])
        
        vendas = await client.execute("SELECT valor_total as valor, status FROM vendas WHERE revendedora_id = ? ORDER BY id DESC LIMIT 5", [rev_id])
        
        return {
            "revendedora": { "telegram_status": "Online" if data.get("telegram_id") else "Pendente" },
            "ai_usage": 150, # YOLO mock
            "recent_sales": [dict(v) for v in vendas.rows]
        }

    @staticmethod
    async def get_global_stats():
        revs = await client.execute("SELECT COUNT(*) FROM revendedoras")
        vendas = await client.execute("SELECT SUM(valor_total) FROM vendas")
        
        vendas_val = vendas.rows[0][0] if vendas.rows and vendas.rows[0][0] is not None else 0
        
        return {
            "total_revendedoras": revs.rows[0][0] if revs.rows else 0,
            "vendas_mensais": vendas_val,
            "mrr": vendas_val * 0.1, # YOLO simulação de 10%
            "llm_status": "OK"
        }

    @staticmethod
    async def get_configs():
        try:
            result = await client.execute("SELECT key, value, category FROM configs")
            return [dict(row) for row in result.rows]
        except:
            return []

    @staticmethod
    async def save_config(key: str, value: str, category: str):
        try:
            # Upsert fallback
            await client.execute(
                "INSERT INTO configs (key, value, category) VALUES (?, ?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                [key, value, category]
            )
            return {"status": "success"}
        except Exception as e:
            # If table doesn't exist, create and retry
            logger.error(f"Erro configs: {e}")
            await client.execute("""
            CREATE TABLE IF NOT EXISTS configs (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                category TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            await client.execute(
                "INSERT INTO configs (key, value, category) VALUES (?, ?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                [key, value, category]
            )
            return {"status": "success"}

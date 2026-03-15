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
                "INSERT INTO revendedoras (id, nome, email, cpf_cnpj, plano_id, telegram_id) VALUES (?, ?, ?, ?, ?, ?)",
                [rev_id, rev.nome, rev.email, rev.cpf_cnpj, rev.plano_id, rev.telegram_id]
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

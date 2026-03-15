from src.db.session import client
import logging
import uuid

logger = logging.getLogger(__name__)

class ShadowService:
    @staticmethod
    async def get_readonly_context(admin_id: str, revendedora_id: str):
        """
        Cria um contexto de visualização segura (Story 4.2).
        Retorna o perfil da revendedora marcado como read-only.
        """
        # Audit logs (Story 4.2 AC 2)
        await client.execute(
            "INSERT INTO audit_log (id, entidade, entidade_id, acao, usuario_admin) VALUES (?, ?, ?, ?, ?)",
            [str(uuid.uuid4()), "shadow_access", revendedora_id, "IMPERSONATE_START", admin_id]
        )
        
        # Buscar dados da revendedora
        res = await client.execute("SELECT * FROM revendedoras WHERE id = ?", [revendedora_id])
        if not res.rows:
            return None
            
        data = dict(res.rows[0])
        data["shadow_mode"] = True
        data["readonly"] = True
        return data

    @staticmethod
    def validate_mutation(is_shadow: bool):
        """
        Impede mutações financeiras em modo shadow (Story 4.2 AC 1).
        """
        if is_shadow:
            raise Exception("🛑 Ação bloqueada: Modo Shadow é apenas para visualização.")
        return True

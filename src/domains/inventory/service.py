from src.db.session import client
import uuid
import logging

logger = logging.getLogger(__name__)

class InventoryService:
    @staticmethod
    async def add_global_product(nome: str, descricao: str, preco: float, url: str):
        p_id = str(uuid.uuid4())
        await client.execute(
            "INSERT INTO catalogo_global (id, nome, descricao, preco_sugerido, imagem_url) VALUES (?, ?, ?, ?, ?)",
            [p_id, nome, descricao, preco, url]
        )
        return p_id

    @staticmethod
    async def update_local_stock(revendedora_id: str, produto_id: str, qtd: int):
        # Verificar se existe
        res = await client.execute(
            "SELECT id FROM estoque_local WHERE revendedora_id = ? AND produto_global_id = ?",
            [revendedora_id, produto_id]
        )
        if res.rows:
            await client.execute(
                "UPDATE estoque_local SET quantidade = ? WHERE revendedora_id = ? AND produto_global_id = ?",
                [qtd, revendedora_id, produto_id]
            )
        else:
            stock_id = str(uuid.uuid4())
            await client.execute(
                "INSERT INTO estoque_local (id, revendedora_id, produto_global_id, quantidade) VALUES (?, ?, ?, ?)",
                [stock_id, revendedora_id, produto_id, qtd]
            )
        return True

    @staticmethod
    async def check_availability(revendedora_id: str, produto_id: str, qtd_needed: int):
        """
        Verifica estoque e sugere substituto se necessário (Story 3.2 AC 2).
        """
        res = await client.execute(
            "SELECT quantidade FROM estoque_local WHERE revendedora_id = ? AND produto_global_id = ?",
            [revendedora_id, produto_id]
        )
        if not res.rows or res.rows[0][0] < qtd_needed:
            # Sugerir substituto (Pega outro item aleatório do catálogo global para o YOLO)
            sub = await client.execute("SELECT nome FROM catalogo_global WHERE id != ? LIMIT 1", [produto_id])
            sugestao = sub.rows[0][0] if sub.rows else "Nenhum substituto encontrado"
            return {"available": False, "sugestao": sugestao}
        
        return {"available": True}

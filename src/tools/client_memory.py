import os
import aiofiles
from langchain.tools import tool
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Base path for client memories
BASE_MEMORIES_PATH = "docs/revendedoras"

@tool
async def persistir_memoria_cliente(revendedora_id: str, cliente_id: str, resumo: str) -> str:
    """
    Persiste um resumo de uma conversa com um cliente em um arquivo .md.
    Isso cria a 'memória eterna' do cliente para o SaaS.
    """
    path = os.path.join(BASE_MEMORIES_PATH, revendedora_id, "clientes", cliente_id)
    os.makedirs(path, exist_ok=True)
    
    filename = os.path.join(path, "conversations.md")
    
    try:
        async with aiofiles.open(filename, mode="a", encoding="utf-8") as f:
            await f.write(f"### Interação em {os.uname().nodename if hasattr(os, 'uname') else 'server'}\n")
            await f.write(f"{resumo}\n\n---\n")
        return f"Memória atualizada para o cliente {cliente_id}."
    except Exception as e:
        logger.error(f"Erro ao persistir memória: {e}")
        return f"Falha ao salvar memória: {e}"

@tool
async def consultar_historico_cliente(revendedora_id: str, cliente_id: str) -> str:
    """
    Lê o histórico de interações (memória eterna) de um cliente específico.
    """
    filename = os.path.join(BASE_MEMORIES_PATH, revendedora_id, "clientes", cliente_id, "conversations.md")
    
    if not os.path.exists(filename):
        return "Nenhum histórico encontrado para este cliente."
        
    try:
        async with aiofiles.open(filename, mode="r", encoding="utf-8") as f:
            content = await f.read()
            return content
    except Exception as e:
        logger.error(f"Erro ao ler histórico: {e}")
        return f"Erro ao acessar histórico: {e}"

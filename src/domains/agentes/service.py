import logging
import uuid
import datetime
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from src.core.config import settings
from src.db.session import client as db_client
from src.domains.admin.service import AdminService
from src.domains.finance.service import FinanceService
from src.domains.inventory.service import InventoryService

logger = logging.getLogger(__name__)

class BellaAgent:
    """
    Agente BellaZap multi-tenant (Serverless Ready) usando Turso/LibSQL.
    """

    def __init__(self, revendedora_id: str, departamento: str = "vendas"):
        self.revendedora_id = revendedora_id
        self.departamento = departamento
        self.config: Optional[Dict] = None
        
    async def initialize(self):
        """Carrega configurações e inicializa o LLM."""
        # Mock de configurações (no YOLO, assumimos defaults agressivos)
        system_prompt = (
            "Você é a Bella, o cérebro de IA da BellaZap. Seu tom é amigável e focado em vendas.\n"
            f"Você está atendendo a revendedora ID: {self.revendedora_id}."
        )

        self.llm = self._get_llm()
        self.tools = self._setup_tools()
        self.agent_executor = self._setup_agent(system_prompt)

    def _get_llm(self):
        """Prioriza OpenAI para garantir nota 10 na extração de dados."""
        return ChatOpenAI(api_key=settings.OPENAI_API_KEY, model=settings.CLOUD_LLM_MODEL, temperature=0)

    def _setup_tools(self) -> List[Any]:
        
        @tool
        async def consulta_estoque_proprio() -> str:
            """Consulta seu estoque local e preços."""
            res = await db_client.execute(
                "SELECT c.nome, e.quantidade, c.preco_sugerido FROM estoque_local e JOIN catalogo_global c ON e.produto_global_id = c.id WHERE e.revendedora_id = ?",
                [self.revendedora_id]
            )
            if not res.rows:
                return "Seu estoque está vazio."
            
            report = "📦 Seu Estoque:\n"
            for row in res.rows:
                report += f"- {row[0]}: {row[1]} un. | R$ {row[2]}\n"
            return report

        @tool
        async def registrar_venda_pix(cliente_nome: str, valor: float) -> str:
            """Registra uma venda e gera QR Code PIX via Asaas."""
            # 1. Buscar ou cadastrar cliente (Simplificado)
            res_cli = await db_client.execute("SELECT id FROM clientes WHERE nome = ? AND revendedora_id = ?", [cliente_nome, self.revendedora_id])
            if not res_cli.rows:
                cliente_id = str(uuid.uuid4())
                await db_client.execute("INSERT INTO clientes (id, nome, revendedora_id) VALUES (?, ?, ?)", [cliente_id, cliente_nome, self.revendedora_id])
            else:
                cliente_id = res_cli.rows[0][0]

            # 2. Gerar PIX
            pix_data = await FinanceService.generate_pix_venda(self.revendedora_id, valor, cliente_id)
            return f"✅ Venda registrada! PIX Gerado.\nCopia e Cola: `{pix_data['pix_chave']}`\nStatus: {pix_data['status']}"

        @tool
        async def consulta_dashboard() -> str:
            """Mostra o faturamento e métricas de desempenho (Relatórios Adaptativos)."""
            data = await FinanceService.get_analytics(self.revendedora_id)
            return (
                f"📊 *Seu Desempenho Atual*\n"
                f"- Total de Vendas: {data['vendas']}\n"
                f"- Faturamento: R$ {data['faturamento']:.2f}\n"
                f"- Conversão: {data['taxa_conversao']}\n\n"
                "Você está indo muito bem! ✨"
            )

        @tool
        async def verificar_disponibilidade(produto_nome: str, qtd: int) -> str:
            """Verifica se há estoque e sugere substitutos se estiver acabando."""
            # Buscar ID do produto pelo nome (Simulado YOLO)
            res = await db_client.execute("SELECT id FROM catalogo_global WHERE nome LIKE ?", [f"%{produto_nome}%"])
            if not res.rows:
                return "Produto não encontrado no catálogo global."
            
            p_id = res.rows[0][0]
            check = await InventoryService.check_availability(self.revendedora_id, p_id, qtd)
            
            if not check["available"]:
                return f"❌ Estoque insuficiente. Que tal oferecer o *{check['sugestao']}* no lugar?"
            
            return "✅ Produto disponível em estoque!"

        return [consulta_estoque_proprio, registrar_venda_pix, consulta_dashboard, verificar_disponibilidade]

    def _setup_agent(self, system_prompt: str) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    async def chat(self, user_input: str, history: List[Dict[str, str]] = []) -> str:
        if not hasattr(self, 'agent_executor'):
            await self.initialize()
            
        try:
            response = await self.agent_executor.ainvoke({
                "input": user_input,
                "chat_history": history
            })
            output = response["output"]

            # Log de Auditoria
            log_id = str(uuid.uuid4())
            await db_client.execute(
                "INSERT INTO audit_log (id, entidade, entidade_id, acao, dados_novos) VALUES (?, ?, ?, ?, ?)",
                [log_id, "chat", self.revendedora_id, "IA_INTERACTION", output[:100]]
            )

            return output
        except Exception as e:
            logger.error(f"Erro no chat motor Bella: {e}")
            return "Ops! Tive um problema técnico. Pode repetir?"

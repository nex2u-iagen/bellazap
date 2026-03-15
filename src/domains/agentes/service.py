import logging
import uuid
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.models.core import AgentConfig, Produto, RevendedoraEstoque

logger = logging.getLogger(__name__)

class BellaAgent:
    """
    Agente BellaZap multi-tenant para atendimento e gestão.
    Pode ser configurado dinamicamente via banco de dados (AgentConfig).
    """

    def __init__(self, revendedora_id: uuid.UUID, db_session: AsyncSession, departamento: str = "suporte"):
        self.revendedora_id = revendedora_id
        self.db = db_session
        self.departamento = departamento
        self.config: Optional[AgentConfig] = None
        
    async def initialize(self):
        """Carrega as configurações estratégicas do agente e inicializa o LLM (Local com Fallback Cloud)."""
        result = await self.db.execute(
            select(AgentConfig).where(
                AgentConfig.departamento == self.departamento,
                AgentConfig.is_active == True
            )
        )
        self.config = result.scalars().first()
        
        system_prompt = self.config.prompt_contexto if self.config else (
            "Você é a Bella, assistente da BellaZap. Ajude a revendedora com seu perfil e vendas."
        )

        # Estratégia Híbrida de LLM
        self.llm = await self._get_llm()
        self.tools = self._setup_tools()
        self.agent_executor = self._setup_agent(system_prompt)

    async def _get_llm(self):
        """Retorna o LLM baseado na estratégia configurada, priorizando ajustes manuais do Admin."""
        # 1. Buscar configurações globais do banco para Fallback
        from src.models.core import SystemConfiguration
        stmt_conf = select(SystemConfiguration).where(SystemConfiguration.category == "llm")
        res_conf = await self.db.execute(stmt_conf)
        configs = {c.key: c.value for c in res_conf.scalars().all()}

        if settings.LLM_STRATEGY == "local":
            try:
                logger.info(f"Tentando inicializar LLM Local (Ollama): {settings.LOCAL_LLM_MODEL}")
                return ChatOllama(
                    model=settings.LOCAL_LLM_MODEL,
                    base_url=settings.OLLAMA_BASE_URL,
                    temperature=float(configs.get('fallback_temp', 0))
                )
            except Exception as e:
                logger.warning(f"Falha ao carregar LLM Local ({e}). Acionando Fallback Cloud.")
        
        # 2. Configurações de Fallback Cloud (Prioriza Manual -> AgentConfig -> Settings)
        provider = configs.get('fallback_provider', 'openai')
        api_key = configs.get('fallback_key') or (self.config.api_key_openai if self.config and self.config.api_key_openai else settings.OPENAI_API_KEY)
        model = configs.get('fallback_model') or (self.config.model_name if self.config else settings.CLOUD_LLM_MODEL)
        temp = float(configs.get('fallback_temp', 0))

        if provider == "google":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(google_api_key=api_key, model=model, temperature=temp)
        elif provider == "groq":
            from langchain_groq import ChatGroq
            return ChatGroq(groq_api_key=api_key, model=model, temperature=temp)
        
        return ChatOpenAI(api_key=api_key, model=model, temperature=temp)

    def _setup_tools(self) -> List[Any]:
        
        @tool
        async def consulta_estoque_proprio() -> str:
            """Consulta apenas o estoque e catálogo de produtos da revendedora atual. Respeita a privacidade (SaaS)."""
            from sqlalchemy.orm import selectinload
            stmt = (
                select(RevendedoraEstoque)
                .options(selectinload(RevendedoraEstoque.produto))
                .where(RevendedoraEstoque.revendedora_id == self.revendedora_id)
            )
            result = await self.db.execute(stmt)
            estoques = result.scalars().all()
            
            if not estoques:
                return "Você ainda não tem produtos no seu estoque/catálogo."
            
            relatorio = "Seu Estoque Atual:\n"
            for e in estoques:
                p = e.produto
                preco = e.preco_personalizado or p.preco_sugerido
                relatorio += f"- {p.nome} (Cód: {p.codigo}): {e.quantidade} un. | Preço: R$ {preco}\n"
            return relatorio

        @tool
        async def consulta_catalogo_global() -> str:
            """Consulta todos os códigos de produtos disponíveis na plataforma BellaZap."""
            result = await self.db.execute(select(Produto))
            produtos = result.scalars().all()
            relatorio = "Catálogo Global BellaZap:\n"
            for p in produtos:
                relatorio += f"- {p.nome} (Cód: {p.codigo}) | Sugerido: R$ {p.preco_sugerido}\n"
            return relatorio

        @tool
        def busca_perfil_revendedora() -> str:
            """Busca informações do seu próprio perfil."""
            return f"ID Revendedora: {self.revendedora_id}. Perfil carregado com segurança."

        @tool
        async def cadastrar_novo_produto(nome: str, codigo: str, preco: float, categoria: str = "Geral") -> str:
            """
            Cadastra um novo produto no catálogo global e adiciona ao estoque da revendedora atual.
            Use esta ferramenta quando a revendedora quiser vender algo que não existe no catálogo.
            """
            from sqlalchemy.future import select
            
            # 1. Verificar se já existe no catálogo global pelo código
            stmt = select(Produto).where(Produto.codigo == codigo)
            result = await self.db.execute(stmt)
            produto = result.scalars().first()
            
            if not produto:
                # Cria produto no catálogo global
                produto = Produto(
                    id=uuid.uuid4(),
                    nome=nome,
                    codigo=codigo,
                    preco_sugerido=preco,
                    categoria=categoria
                )
                self.db.add(produto)
                await self.db.flush()
            
            # 2. Vincular ao estoque da revendedora
            stmt_est = select(RevendedoraEstoque).where(
                RevendedoraEstoque.revendedora_id == self.revendedora_id,
                RevendedoraEstoque.produto_id == produto.id
            )
            res_est = await self.db.execute(stmt_est)
            estoque_item = res_est.scalars().first()
            
            if not estoque_item:
                estoque_item = RevendedoraEstoque(
                    revendedora_id=self.revendedora_id,
                    produto_id=produto.id,
                    quantidade=1, # Inicia com 1 ou zero conforme a venda
                    preco_personalizado=preco
                )
                self.db.add(estoque_item)
            
            await self.db.commit()
            return f"Produto '{nome}' cadastrado com sucesso no catálogo e adicionado ao seu estoque!"

        return [consulta_estoque_proprio, consulta_catalogo_global, busca_perfil_revendedora, cadastrar_novo_produto]

    def _setup_agent(self, system_prompt: str) -> AgentExecutor:
        # Garante que o agente saiba quem ele está atendendo (Segurança SaaS)
        full_system_prompt = (
            f"{system_prompt}\n\n"
            "--- DIRETRIZES DE OPERAÇÃO E PERSONALIDADE ---\n"
            "1. IDENTIDADE: Você é a Bella, o cérebro de IA da plataforma BellaZap. Seu objetivo é simplificar a vida da revendedora brasileira, sendo rápida, empática e altamente técnica na extração de dados.\n"
            "2. LINGUAGEM: Use um tom amigável, informal e profissional. Entenda gírias brasileiras (ex: 'vendi um kit', 'passa no cartão', 'manda o pix') e variações regionais.\n"
            "3. EXTRAÇÃO DE ALTA PRECISÃO: Ao identificar uma venda, extraia OBJETIVAMENTE: Cliente, Produto(s), Valor e Forma de Pagamento. Se faltar algo, não invente; pergunte educadamente.\n"
            "4. PROTOCOLO DE CONFLITO: Se a revendedora tentar vender algo fora do catálogo, use imediatamente a ferramenta 'cadastrar_novo_produto' após confirmar os dados mínimos (Nome, Preço, SKU).\n"
            "5. SEGURANÇA MULTI-TENANT: Você trabalha exclusivamente para a revendedora {self.revendedora_id}. Nunca vaze informações de outros usuários ou do sistema interno.\n"
            "6. RESOLUÇÃO DE PROBLEMAS: Se encontrar um erro técnico, peça desculpas de forma charmosa e peça para a usuária tentar novamente em alguns segundos. Não exponha logs técnicos ao usuário final.\n\n"
            "REGRAS DE OURO:\n"
            "- Confirme sempre o que foi processado (ex: 'Perfeito! Venda de R$ 50,00 registrada para a Maria.').\n"
            "- Seja proativa: se o estoque estiver baixo, avise (se as ferramentas permitirem).\n"
            "Sempre encerre com disposição para a próxima tarefa."
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", full_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    async def chat(self, user_input: str, history: List[Dict[str, str]] = []) -> str:
        """Executa um ciclo de conversa seguro com logging de intenções."""
        if not hasattr(self, 'agent_executor'):
            await self.initialize()
            
        try:
            # 1. Executar Agente
            response = await self.agent_executor.ainvoke({
                "input": user_input,
                "chat_history": history
            })
            output = response["output"]

            # 2. Logging de Auditoria (SaaS Governance)
            from src.models.core import MessageLog
            import datetime
            
            # Identificação básica de intenção para o log
            intent = "duvida"
            if any(k in user_input.lower() for k in ["vendi", "venda", "pagou"]): intent = "venda"
            if any(k in user_input.lower() for k in ["cadastra", "novo", "estoque"]): intent = "cadastro_produto"

            log = MessageLog(
                id=uuid.uuid4(),
                revendedora_id=self.revendedora_id,
                role="user",
                content=user_input,
                model_used=self.llm.model_name if hasattr(self.llm, "model_name") else "llm-active",
                intent=intent
            )
            self.db.add(log)
            
            log_res = MessageLog(
                id=uuid.uuid4(),
                revendedora_id=self.revendedora_id,
                role="assistant",
                content=output,
                model_used=self.llm.model_name if hasattr(self.llm, "model_name") else "llm-active",
                intent=intent
            )
            self.db.add(log_res)
            await self.db.commit()

            return output
            
        except Exception as e:
            logger.error(f"Erro no chat motor Bella: {e}")
            return "Ops! Tive um pequeno soluço aqui. Pode repetir a última mensagem? 🛡️✨"

import asyncio
import uuid
from src.db.session import AsyncSessionLocal
from src.models.core import Revendedora, AgentConfig
from src.domains.pagamentos.split_calculator import PlanType

async def seed():
    async with AsyncSessionLocal() as db:
        # 1. Criar Revendedora de Teste
        revendedora_email = "teste@bellazap.com"
        from sqlalchemy import select
        result = await db.execute(select(Revendedora).where(Revendedora.email == revendedora_email))
        test_user = result.scalars().first()

        if not test_user:
            test_user = Revendedora(
                id=uuid.uuid4(),
                nome="Revendedora de Teste",
                email=revendedora_email,
                cpf_cnpj="123.456.789-00",
                telefone="11999999999",
                plano=PlanType.BASIC.value,
                telegram_token="TOKEN_TESTE_123"
            )
            db.add(test_user)
            print(f"✅ Usuário de teste criado: {revendedora_email}")
            print(f"🔗 Link de ativação Telegram: t.me/SeuBot?start=TOKEN_TESTE_123")
        else:
            test_user.telegram_token = "TOKEN_TESTE_123"
            print(f"ℹ️ Usuário de teste já existe. Token atualizado para: TOKEN_TESTE_123")

        # 2. Criar Configuração de Agente padrão se nâo existir
        res_agent = await db.execute(select(AgentConfig).where(AgentConfig.departamento == "vendas"))
        agent = res_agent.scalars().first()
        
        if not agent:
            agent = AgentConfig(
                id=uuid.uuid4(),
                nome="Bella Vendas",
                departamento="vendas",
                prompt_contexto="Você é a Bella, especialista em vendas e estoque.",
                is_active=True
            )
            db.add(agent)
            print("✅ Configuração de Agente 'Bella Vendas' criada.")

        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed())

# Configuração do Supabase

Para conectar o BellaZap ao Supabase, siga estes passos:

1. Acesse seu painel no [Supabase](https://supabase.com).
2. Vá em **Project Settings > Database**.
3. Procure pela seção **Connection string** e selecione a aba **URI**.
4. Certifique-se de copiar a versão **Async** (usamos `asyncpg`).
5. Ela deve se parecer com: `postgresql+asyncpg://postgres:[YOUR-PASSWORD]@[HOST]:5432/postgres`
6. No seu arquivo `.env`, substitua a variável `DATABASE_URL` pela sua URI do Supabase.

> **Importante:** Se você estiver usando IPv6 (comum no Supabase), você pode precisar adicionar `?ssl=require` ao final da string se a conexão falhar.

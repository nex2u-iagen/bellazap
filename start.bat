@echo off
ECHO "--- Iniciando servicos de infraestrutura (Postgres e Redis) ---"
docker-compose up -d

ECHO "--- Ativando ambiente virtual ---"
CALL .\.venv\Scripts\activate

ECHO "--- Iniciando aplicacoes com Honcho ---"
honcho -f Procfile.dev start

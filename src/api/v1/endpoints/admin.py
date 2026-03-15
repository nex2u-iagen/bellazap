from fastapi import APIRouter, Depends, HTTPException
from src.domains.admin.schemas import PlanoCreate, PlanoResponse, RevendedoraCreate, RevendedoraResponse
from src.domains.admin.service import AdminService
from typing import List

router = APIRouter()

# --- Planos ---

@router.post("/planos", response_model=PlanoResponse)
async def create_plano(plano: PlanoCreate):
    """
    Cria um novo plano de comissão para a plataforma.
    """
    return await AdminService.create_plano(plano)

@router.get("/planos", response_model=List[PlanoResponse])
async def list_planos():
    """
    Lista todos os planos disponíveis.
    """
    return await AdminService.list_planos()

# --- Revendedoras ---

@router.post("/revendedoras", response_model=RevendedoraResponse)
async def create_revendedora(rev: RevendedoraCreate):
    """
    Cadastra uma nova representante vinculada a um plano.
    """
    try:
        return await AdminService.create_revendedora(rev)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/revendedoras/telegram/{telegram_id}", response_model=RevendedoraResponse)
async def get_revendedora_by_telegram(telegram_id: str):
    """
    Busca uma revendedora pelo ID do Telegram.
    """
    rev = await AdminService.get_revendedora_by_telegram(telegram_id)
    if not rev:
        raise HTTPException(status_code=404, detail="Revendedora não encontrada")
    return rev

@router.get("/revendedoras")
async def list_revendedoras():
    return await AdminService.list_revendedoras()

@router.patch("/revendedoras/{id}/toggle-active")
async def toggle_active(id: str):
    try:
        return await AdminService.toggle_active(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/revendedoras/{id}")
async def delete_rev(id: str):
    return await AdminService.delete_revendedora(id)

@router.get("/revendedoras/{id}/summary")
async def get_summary(id: str):
    try:
        return await AdminService.get_revendedora_summary(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/stats")
async def get_global_stats():
    return await AdminService.get_global_stats()

@router.get("/configs")
async def get_configs():
    return await AdminService.get_configs()

from pydantic import BaseModel
class ConfigSet(BaseModel):
    key: str
    value: str
    category: str

@router.post("/configs")
async def save_config(cfg: ConfigSet):
    return await AdminService.save_config(cfg.key, cfg.value, cfg.category)


@router.get("/rep/stats")
async def get_rep_dashboard_stats():
    # Para o MVP YOLO: Retornar as estatísticas mockadas ou reais da primeira revendedora
    from src.db.session import client
    res = await client.execute("SELECT id, nome, plano_id FROM revendedoras LIMIT 1")
    if not res.rows:
        return {"saldo": 0, "vendas": 0, "plano": "Sem Plano", "lancamento": "Aguarde"}
    
    rev_id = res.rows[0][0]
    plano = res.rows[0][2]
    
    from src.domains.finance.service import FinanceService
    analytics = await FinanceService.get_analytics(rev_id)
    
    return {
        "saldo": analytics["faturamento"],
        "vendas": analytics["vendas"],
        "plano": plano,
        "lancamento": "Natura Una Gold"
    }

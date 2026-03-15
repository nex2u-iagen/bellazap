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

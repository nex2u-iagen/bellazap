from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
import uuid

# --- Planos ---

class PlanoBase(BaseModel):
    nome: str = Field(..., min_length=3)
    taxa_fixa: float = Field(default=0.0, ge=0.0)
    taxa_variavel: float = Field(default=0.0, ge=0.0, le=100.0)

    @validator("taxa_variavel")
    def validate_taxa(cls, v):
        if v < 0 or v > 100:
            raise ValueError("Taxa variável deve estar entre 0 e 100%")
        return v

class PlanoCreate(PlanoBase):
    pass

class PlanoResponse(PlanoBase):
    id: str
    created_at: Optional[str] = None

# --- Representantes (Revendedoras) ---

class RevendedoraBase(BaseModel):
    nome: str
    email: EmailStr
    cpf_cnpj: str
    plano_id: str

class RevendedoraCreate(RevendedoraBase):
    telegram_id: Optional[str] = None
    asaas_access_token: Optional[str] = None

class RevendedoraResponse(RevendedoraBase):
    id: str
    created_at: Optional[str] = None
    telegram_id: Optional[str] = None
    asaas_access_token: Optional[str] = None

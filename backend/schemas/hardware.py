"""
Hardware-related schemas
"""
from pydantic import BaseModel
from typing import Optional


class HardwareResponse(BaseModel):
    id_hw: int
    nome_hw: str
    descrizione_hw: Optional[str] = None
    tipo: str
    DI: int = 0
    DO: int = 0
    AI: int = 0
    AO: int = 0
    F_DI: int = 0
    F_DO: int = 0
    Ox: float = 0.0
    Oy: float = 0.0
    L: float = 0.0
    H: float = 0.0
    blocco_grafico: Optional[str] = None
    
    class Config:
        from_attributes = True


class HardwareNodeCreate(BaseModel):
    id_nodo: int
    id_hw: int
    slot: Optional[int] = None
    quantita: int = 1


class HardwareNodeResponse(BaseModel):
    id_nodo_hw: int
    id_nodo: int
    id_hw: int
    slot: Optional[int] = None
    quantita: int = 1
    nome_hw: Optional[str] = None
    tipo: Optional[str] = None
    DI: Optional[int] = None
    DO: Optional[int] = None
    
    class Config:
        from_attributes = True
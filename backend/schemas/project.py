"""
Project-related schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProjectBase(BaseModel):
    nome_progetto: str
    descrizione: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id_prg: int
    data_creazione: Optional[datetime] = None
    utente: Optional[str] = None
    
    class Config:
        from_attributes = True


class NodeBase(BaseModel):
    nome_nodo: str
    tipo_nodo: str = "PLC"
    descrizione: Optional[str] = None


class NodeCreate(NodeBase):
    id_prg: int
    id_quadro: Optional[int] = None


class NodeResponse(NodeBase):
    id_nodo: int
    id_prg: int
    id_quadro: Optional[int] = None
    
    class Config:
        from_attributes = True
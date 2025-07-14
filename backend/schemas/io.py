"""
I/O related schemas
"""
from pydantic import BaseModel
from typing import Optional


class IOBase(BaseModel):
    codice: str
    descrizione: Optional[str] = None
    tipo: str
    note: Optional[str] = None


class IOResponse(IOBase):
    id_io: int
    id_modulo: Optional[int] = None
    indirizzo: Optional[str] = None
    id_prg: int
    
    class Config:
        from_attributes = True


class IOAssignRequest(BaseModel):
    id_io: int
    id_modulo: int
    indirizzo: Optional[str] = None
    note: Optional[str] = None


class IORemoveRequest(BaseModel):
    id_io: int
    id_modulo: Optional[int] = None


class ExportRequest(BaseModel):
    id_prg: int
    format: str = "xml"
    include_io: bool = True
    include_utilities: bool = True
    include_nodes: bool = True


class SchemaRequest(BaseModel):
    id_prg: int
    schema_type: str = "electrical"
    options: Optional[dict] = None
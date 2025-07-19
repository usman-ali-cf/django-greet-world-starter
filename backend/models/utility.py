"""
Utility models for the application
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import Base

class Utenza(Base):
    """Model for t_utenza table"""
    __tablename__ = 't_utenza'
    
    id_utenza = Column(Integer, primary_key=True, index=True)
    id_prg = Column(Integer, ForeignKey('t_progetti.id_prg'), nullable=False)
    id_nodo = Column(Integer, nullable=True)
    nome_utenza = Column(String(255), nullable=False)
    descrizione = Column(Text)
    categoria = Column(String(50))
    tipo_comando = Column(String(50), nullable=True)
    tensione = Column(String(20), nullable=True)
    zona = Column(String(100))
    DI = Column(Integer, default=0)
    DO = Column(Integer, default=0)
    AI = Column(Integer, default=0)
    AO = Column(Integer, default=0)
    FDI = Column(Integer, default=0)
    FDO = Column(Integer, default=0)
    potenza = Column(Float, default=0.0)
    id_cat = Column(Integer, nullable=True)
    id_sottocat = Column(Integer, nullable=True)
    id_opzione = Column(Integer, nullable=True)
    elaborata = Column(Integer, default=0)
    taglio = Column(String(50), nullable=True)
    
    # Relationships
    potenze = relationship("Potenza", back_populates="utenza", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Utenza(id={self.id_utenza}, nome='{self.nome_utenza}')>"


class Potenza(Base):
    """Model for t_potenza table"""
    __tablename__ = 't_potenza'
    
    id_potenza = Column(Integer, primary_key=True, index=True)
    id_utenza = Column(Integer, ForeignKey('t_utenza.id_utenza'), nullable=False)
    id_prg = Column(Integer, ForeignKey('t_progetti.id_prg'), nullable=False)
    id_nodo = Column(Integer, nullable=True)
    nome = Column(String(50), nullable=True)
    tipo = Column(String(50), nullable=True)
    DI = Column(Integer, default=0)
    DO = Column(Integer, default=0)
    potenza = Column(Float, default=0.0)
    tensione = Column(String(20))
    descrizione = Column(Text)
    zona = Column(String(50), nullable=True)
    elaborato = Column(String(1), nullable=True)  # binary(1) in SQLite, use String(1) for Postgres
    id_opzione_avviamento = Column(Integer, nullable=True)
    id_blocco = Column(Integer, nullable=True)
    Ox = Column(Float, nullable=True)
    Oy = Column(Float, nullable=True)
    dwg = Column(String(50), nullable=True)
    L = Column(Float, nullable=True)
    id_coordinamento = Column(Integer, nullable=True)
    NumeroFoglio = Column(Text, nullable=True)
    xml = Column(Text, nullable=True)
    
    # Relationships
    utenza = relationship("Utenza", back_populates="potenze")
    
    def __repr__(self):
        return f"<Potenza(id={self.id_potenza}, nome='{self.nome}', potenza={self.potenza})>"

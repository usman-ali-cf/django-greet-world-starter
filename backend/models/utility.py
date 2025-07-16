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
    nome_utenza = Column(String(255), nullable=False)
    descrizione = Column(Text)
    categoria = Column(String(50))
    tensione = Column(Float)
    zona = Column(String(100))
    DI = Column(Integer, default=0)
    DO = Column(Integer, default=0)
    AI = Column(Integer, default=0)
    AO = Column(Integer, default=0)
    FDI = Column(Integer, default=0)
    FDO = Column(Integer, default=0)
    potenza = Column(Float, default=0.0)
    
    # Relationships
    potenze = relationship("Potenza", back_populates="utenza", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Utenza(id={self.id_utenza}, nome='{self.nome_utenza}')>"


class Potenza(Base):
    """Model for t_potenza table"""
    __tablename__ = 't_potenza'
    
    id_potenza = Column(Integer, primary_key=True, index=True)
    id_prg = Column(Integer, ForeignKey('t_progetti.id_prg'), nullable=False)
    id_utenza = Column(Integer, ForeignKey('t_utenza.id_utenza'), nullable=False)
    nome = Column(String(255), nullable=False)
    potenza = Column(Float, nullable=False)
    tensione = Column(Float)
    descrizione = Column(Text)
    zona = Column(String(100))
    
    # Relationships
    utenza = relationship("Utenza", back_populates="potenze")
    
    def __repr__(self):
        return f"<Potenza(id={self.id_potenza}, nome='{self.nome}', potenza={self.potenza})>"

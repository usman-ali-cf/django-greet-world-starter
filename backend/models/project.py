"""
Project-related models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base


class Project(Base):
    __tablename__ = "t_progetti"
    
    id_prg = Column(Integer, primary_key=True, index=True)
    nome_progetto = Column(String, nullable=False)
    descrizione = Column(Text)
    data_creazione = Column(DateTime, default=func.now())
    utente = Column(String)
    
    # Relationships
    nodes = relationship("Node", back_populates="project", cascade="all, delete-orphan")


class Node(Base):
    __tablename__ = "t_nodo"
    
    id_nodo = Column(Integer, primary_key=True, index=True)
    nome_nodo = Column(String, nullable=False)
    tipo_nodo = Column(String, default="PLC")
    descrizione = Column(Text)
    id_prg = Column(Integer, ForeignKey("t_progetti.id_prg"), nullable=False)
    id_quadro = Column(Integer)
    
    # Relationships
    project = relationship("Project", back_populates="nodes")
    hardware_nodes = relationship("HardwareNode", back_populates="node", cascade="all, delete-orphan")


class HardwareNode(Base):
    __tablename__ = "t_nodo_hw"
    
    id_nodo_hw = Column(Integer, primary_key=True, index=True)
    id_nodo = Column(Integer, ForeignKey("t_nodo.id_nodo"), nullable=False)
    id_hw = Column(Integer, ForeignKey("t_cat_hw.id_hw"), nullable=False)
    slot = Column(Integer)
    quantita = Column(Integer, default=1)
    
    # Relationships
    node = relationship("Node", back_populates="hardware_nodes")
    hardware = relationship("Hardware", back_populates="hardware_nodes")
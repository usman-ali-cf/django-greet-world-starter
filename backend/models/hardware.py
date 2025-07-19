"""
Hardware and I/O related models
"""
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Hardware(Base):
    __tablename__ = "t_cat_hw"
    
    id_hw = Column(Integer, primary_key=True, index=True)
    nome_hw = Column(String, nullable=False)
    descrizione_hw = Column(Text)
    tipo = Column(String, nullable=False)
    DI = Column(Integer, default=0)
    DO = Column(Integer, default=0)
    AI = Column(Integer, default=0)
    AO = Column(Integer, default=0)
    F_DI = Column(Integer, default=0)  # F-DI in DB
    F_DO = Column(Integer, default=0)  # F-DO in DB
    Ox = Column(Float, default=0.0)
    Oy = Column(Float, default=0.0)
    L = Column(Float, default=0.0)
    H = Column(Float, default=0.0)
    blocco_grafico = Column(String)
    
    # Note: F-DI and F-DO columns use hyphens in DB, handle in queries
    
    # Relationships
    hardware_nodes = relationship("HardwareNode", back_populates="hardware")


class IO(Base):
    __tablename__ = "t_io"
    
    id_io = Column(Integer, primary_key=True, index=True)
    codice = Column(String, nullable=False)
    descrizione = Column(Text)
    tipo = Column(String, nullable=False)
    id_modulo = Column(Integer, ForeignKey("t_nodo_hw.id_nodo_hw"))
    indirizzo = Column(String)
    note = Column(Text)
    id_prg = Column(Integer, ForeignKey("t_progetti.id_prg"), nullable=False)
    
    # Additional relationships if needed
    # modulo = relationship("HardwareNode", foreign_keys=[id_modulo])
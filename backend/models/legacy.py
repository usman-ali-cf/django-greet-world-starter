from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Boolean
from models.base import Base

class CoordCaviAuxSez(Base):
    __tablename__ = 't_coord_cavi_aux_sez'
    id_coordinamento = Column(Integer, ForeignKey('t_coordinamento.id_coordinamento'), primary_key=True)
    articolo = Column(String(50))
    diametro = Column(Float)
    cg_cavo = Column(String(50))
    cg_diametro = Column(String(50))

class CoordCaviDaQuadro(Base):
    __tablename__ = 't_coord_cavi_da_quadro'
    id_coordinamento = Column(Integer, ForeignKey('t_coordinamento.id_coordinamento'), primary_key=True)
    articolo = Column(String(50))
    diametro = Column(Float)
    cg_cavo_multi = Column(String(50))
    cg_diametro = Column(String(50))

class CoordCaviInQuadro(Base):
    __tablename__ = 't_coord_cavi_in_quadro'
    id_coordinamento = Column(Integer, ForeignKey('t_coordinamento.id_coordinamento'), primary_key=True)
    articolo = Column(String(50))
    sezione = Column(Float)
    colore = Column(String(50))
    diametro = Column(String(50))

class CoordCavoSezMot(Base):
    __tablename__ = 't_coord_cavo_sez_mot'
    id_coordinamento = Column(Integer, ForeignKey('t_coordinamento.id_coordinamento'), primary_key=True)
    articolo = Column(String(50))
    cg_cable_multi = Column(String(50))
    diametro = Column(String(50))

class CoordContattori(Base):
    __tablename__ = 't_coord_contattori'
    id_coordinamento = Column(Integer, ForeignKey('t_coordinamento.id_coordinamento'), primary_key=True)
    articolo = Column(String(50))
    power_loss = Column(Float)
    line_c_power = Column(Float)
    line_c_filter = Column(String(50))

class CoordMotore(Base):
    __tablename__ = 't_coord_motore'
    id_coordinamento = Column(Integer, ForeignKey('t_coordinamento.id_coordinamento'), primary_key=True)
    potenza = Column(String(50))
    ampere = Column(String(50))
    speed = Column(String(50))
    connessione = Column(String(50))
    Volt = Column(String(50))

class CoordSalvamotore(Base):
    __tablename__ = 't_coord_salvamotore'
    id_coordinamento = Column(Integer, ForeignKey('t_coordinamento.id_coordinamento'), primary_key=True)
    articolo = Column(String(50))
    perdite_potenza = Column(String(50))
    aux_contacts = Column(String(50))
    kit_connection = Column(String(50))
    morsettiera = Column(String(50))
    size = Column(String(50))
    campo = Column(String(50))
    settaggio = Column(String(50))

class CoordSezionatori(Base):
    __tablename__ = 't_coord_sezionatori'
    id_coordinamento = Column(Integer, ForeignKey('t_coordinamento.id_coordinamento'), primary_key=True)
    articolo = Column(String(50))
    aux_contacts = Column(String(50))
    Ampere = Column(Float)
    kw_ac3 = Column(Float)
    kw_ac23 = Column(Float)
    H_mm = Column(Float)
    L_mm = Column(Float)
    P_mm = Column(Float)
    max_sezione_cavo = Column(Float)

class CoordTerminals(Base):
    __tablename__ = 't_coord_terminals'
    id_coordinamento = Column(Integer, ForeignKey('t_coordinamento.id_coordinamento'), primary_key=True)
    articolo = Column(String(50))
    power_loss = Column(Float)
    pe_terminal = Column(String(50))

class Coordinamento(Base):
    __tablename__ = 't_coordinamento'
    id_coordinamento = Column(Integer, primary_key=True, autoincrement=True)
    costruttore = Column(String(100), nullable=False)
    tensione = Column(String(50))
    potenza = Column(Float, nullable=False)
    ampere = Column(Float, nullable=False)
    tipo_avviamento = Column(String(50), nullable=False)
    componente = Column(String(50))
    nome_tabella = Column(String(50))

class NodiPrg(Base):
    __tablename__ = 't_nodi_prg'
    id_nodo = Column(Integer, primary_key=True, autoincrement=True)
    id_prg = Column(Integer, nullable=False)
    nome_nodo = Column(Text, nullable=False)
    descrizione = Column(Text)
    note = Column(Text)
    tipo = Column(String)

class Blocchi(Base):
    __tablename__ = 't_blocchi'
    id_blocco = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String(50))
    dwg = Column(String(50))
    Ox = Column(Float)
    Oy = Column(Float)
    componente = Column(String(50))
    descrizione = Column(Text)
    L = Column(Float)
    H = Column(Float)
    slot_max = Column(Integer, default=1)
    config_path = Column(Text)

class LibreriaSimb(Base):
    __tablename__ = 't_libreria_simb'
    id_simbolo = Column(Integer, primary_key=True, autoincrement=True)
    BlockName = Column(String(50))
    sigla = Column(String(10))
    Description_IT = Column(String(100))
    Description_EN = Column(String(100))
    Description_FR = Column(String(100))
    Description_DE = Column(String(100))
    Description_ES = Column(String(100))
    Description_CZ = Column(String(100))
    Description_PO = Column(String(100))
    Description_FI = Column(String(100))
    Description_HU = Column(String(100))
    Description_SL = Column(String(100))
    Description_PL = Column(String(100))
    State = Column(String(1), default='')
    utilizzato = Column(Integer, default=0)
    Ox = Column(Float)
    Oy = Column(Float)
    L = Column(Float)
    H = Column(Float)
    componente = Column(String(50))
    id_categoria = Column(String(50))
    id_sottocategoria = Column(String(50))
    tipo_simbolo = Column(String(50))
    Blocco_Grafico = Column(String(50))
    TipoIO = Column(String(50))

class FogliMemorizzati(Base):
    __tablename__ = 't_fogli_memorizzati'
    id_foglio = Column(Integer, primary_key=True, autoincrement=True)
    id_prg = Column(Integer, nullable=False)
    id_utenza = Column(Integer, nullable=True)
    dwg = Column(String(50))
    numero_foglio = Column(Integer)
    Ox = Column(Float, default=0)
    Oy = Column(Float, default=0)
    xml = Column(Text)

class TagBlocchi(Base):
    __tablename__ = 't_tag_blocchi'
    id_tag = Column(Integer, primary_key=True, autoincrement=True)
    id_blocco = Column(Integer)
    nome_tag = Column(String(50))
    quadro_tag = Column(String(50))

class BlocchiPotenza(Base):
    __tablename__ = 't_blocchi_potenza'
    id_blocco_potenza = Column(Integer, primary_key=True, autoincrement=True)
    id_prg = Column(Integer, nullable=False)
    id_utenza = Column(Integer, nullable=False)
    NumeroFoglio = Column(Text)
    blocco_grafico = Column(String(50))
    Ox = Column(Float)
    Oy = Column(Float)
    xml = Column(Text)

class Componenti(Base):
    __tablename__ = 't_componenti'
    id_componente = Column(Integer, primary_key=True, autoincrement=True)
    id_prg = Column(Integer, nullable=False)
    id_utenza = Column(Integer, nullable=False)
    id_potenza = Column(Integer)
    componente = Column(String(50))
    padre_figlio = Column(String(20))
    nome = Column(String(50))
    quadro = Column(String(50))
    taglia = Column(String(20))
    funzione1 = Column(String(50))
    funzione2 = Column(String(50))
    costruttore = Column(String(50))

class OpzioniAvviamento(Base):
    __tablename__ = 't_opzioni_avviamento'
    id_opzione = Column(Integer, primary_key=True, autoincrement=True)
    descrizione = Column(String(255), nullable=False)
    id_blocco = Column(Integer)

class UtenzeCat(Base):
    __tablename__ = 't_utenze_cat'
    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String(100), nullable=False)
    visibile = Column(Boolean, default=True)

class UtenzeSottocat(Base):
    __tablename__ = 't_utenze_sottocat'
    id_sottocategoria = Column(Integer, primary_key=True, autoincrement=True)
    id_categoria = Column(Integer, nullable=False)
    sottocategoria = Column(String(100), nullable=False)
    descrizione = Column(Text)
    visibile = Column(Boolean, default=True)

class UtenzeOpzioni(Base):
    __tablename__ = 't_utenze_opzioni'
    id_opzione = Column(Integer, primary_key=True, autoincrement=True)
    id_sottocategoria = Column(Integer, nullable=False)
    opzione = Column(String(100), nullable=False)
    script_py = Column(String(255))
    config_path = Column(String(255))
    visibile = Column(Boolean, default=True)

class SimboliDefault(Base):
    __tablename__ = 't_simboli_default'
    id_opzione = Column(Integer, primary_key=True)
    componente = Column(String(50), nullable=False)
    descrizione = Column(Text)
    id_simbolo = Column(Integer) 
    
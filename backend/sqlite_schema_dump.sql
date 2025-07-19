CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE `t_coord_cavi_aux_sez` (
  `id_coordinamento` integer  NOT NULL
,  `articolo` varchar(50) DEFAULT NULL
,  `diametro` float DEFAULT NULL
,  `cg_cavo` varchar(50) DEFAULT NULL
,  `cg_diametro` varchar(50) DEFAULT NULL
,  CONSTRAINT `t_coord_cavi_aux_sez_ibfk_1` FOREIGN KEY (`id_coordinamento`) REFERENCES `t_coordinamento` (`id_coordinamento`) ON DELETE CASCADE
);
CREATE TABLE `t_coord_cavi_da_quadro` (
  `id_coordinamento` integer  NOT NULL
,  `articolo` varchar(50) DEFAULT NULL
,  `diametro` float DEFAULT NULL
,  `cg_cavo_multi` varchar(50) DEFAULT NULL
,  `cg_diametro` varchar(50) DEFAULT NULL
,  CONSTRAINT `t_coord_cavi_da_quadro_ibfk_1` FOREIGN KEY (`id_coordinamento`) REFERENCES `t_coordinamento` (`id_coordinamento`) ON DELETE CASCADE
);
CREATE TABLE `t_coord_cavi_in_quadro` (
  `id_coordinamento` integer  NOT NULL
,  `articolo` varchar(50) DEFAULT NULL
,  `sezione` float DEFAULT NULL
,  `colore` varchar(50) DEFAULT NULL
,  `diametro` varchar(50) DEFAULT NULL
,  CONSTRAINT `t_coord_cavi_in_quadro_ibfk_1` FOREIGN KEY (`id_coordinamento`) REFERENCES `t_coordinamento` (`id_coordinamento`) ON DELETE CASCADE
);
CREATE TABLE `t_coord_cavo_sez_mot` (
  `id_coordinamento` integer  NOT NULL
,  `articolo` varchar(50) DEFAULT NULL
,  `cg_cable_multi` varchar(50) DEFAULT NULL
,  `diametro` varchar(50) DEFAULT NULL
,  CONSTRAINT `t_coord_cavo_sez_mot_ibfk_1` FOREIGN KEY (`id_coordinamento`) REFERENCES `t_coordinamento` (`id_coordinamento`) ON DELETE CASCADE
);
CREATE TABLE `t_coord_contattori` (
  `id_coordinamento` integer  NOT NULL
,  `articolo` varchar(50) DEFAULT NULL
,  `power_loss` float DEFAULT NULL
,  `line_c_power` float DEFAULT NULL
,  `line_c_filter` varchar(50) DEFAULT NULL
,  CONSTRAINT `t_coord_contattori_ibfk_1` FOREIGN KEY (`id_coordinamento`) REFERENCES `t_coordinamento` (`id_coordinamento`) ON DELETE CASCADE
);
CREATE TABLE `t_coord_motore` (
  `id_coordinamento` integer  NOT NULL
,  `potenza` varchar(50) DEFAULT NULL
,  `ampere` varchar(50) DEFAULT NULL
,  `speed` varchar(50) DEFAULT NULL
,  `connessione` varchar(50) DEFAULT NULL
,  `Volt` varchar(50) DEFAULT NULL
,  CONSTRAINT `t_coord_motore_ibfk_1` FOREIGN KEY (`id_coordinamento`) REFERENCES `t_coordinamento` (`id_coordinamento`) ON DELETE CASCADE
);
CREATE TABLE `t_coord_salvamotore` (
  `id_coordinamento` integer  NOT NULL
,  `articolo` varchar(50) DEFAULT NULL
,  `perdite_potenza` varchar(50) DEFAULT NULL
,  `aux_contacts` varchar(50) DEFAULT NULL
,  `kit_connection` varchar(50) DEFAULT NULL
,  `morsettiera` varchar(50) DEFAULT NULL
,  `size` varchar(50) DEFAULT NULL
,  `campo` varchar(50) DEFAULT NULL
,  `settaggio` varchar(50) DEFAULT NULL
,  CONSTRAINT `t_coord_salvamotore_ibfk_1` FOREIGN KEY (`id_coordinamento`) REFERENCES `t_coordinamento` (`id_coordinamento`) ON DELETE CASCADE
);
CREATE TABLE `t_coord_sezionatori` (
  `id_coordinamento` integer  NOT NULL
,  `articolo` varchar(50) DEFAULT NULL
,  `aux_contacts` varchar(50) DEFAULT NULL
,  `Ampere` float DEFAULT NULL
,  `kw_ac3` float DEFAULT NULL
,  `kw_ac23` float DEFAULT NULL
,  `H_mm` float DEFAULT NULL
,  `L_mm` float DEFAULT NULL
,  `P_mm` float DEFAULT NULL
,  `max_sezione_cavo` float DEFAULT NULL
,  CONSTRAINT `t_coord_sezionatori_ibfk_1` FOREIGN KEY (`id_coordinamento`) REFERENCES `t_coordinamento` (`id_coordinamento`) ON DELETE CASCADE
);
CREATE TABLE `t_coord_terminals` (
  `id_coordinamento` integer  NOT NULL
,  `articolo` varchar(50) DEFAULT NULL
,  `power_loss` float DEFAULT NULL
,  `pe_terminal` varchar(50) DEFAULT NULL
,  CONSTRAINT `t_coord_terminals_ibfk_1` FOREIGN KEY (`id_coordinamento`) REFERENCES `t_coordinamento` (`id_coordinamento`) ON DELETE CASCADE
);
CREATE TABLE `t_coordinamento` (
  `id_coordinamento` integer  NOT NULL PRIMARY KEY AUTOINCREMENT
,  `costruttore` varchar(100) NOT NULL
,  `tensione` varchar(50) DEFAULT NULL
,  `potenza` float NOT NULL
,  `ampere` float NOT NULL
,  `tipo_avviamento` varchar(50) NOT NULL
,  `componente` varchar(50) DEFAULT NULL
,  `nome_tabella` varchar(50) DEFAULT NULL
);
CREATE TABLE `t_nodo` (
  `id_nodo` integer  NOT NULL PRIMARY KEY AUTOINCREMENT
,  `nome_nodo` varchar(100) NOT NULL
,  `tipo_nodo` varchar(50) NOT NULL
,  `descrizione` text
,  `id_prg` integer  NOT NULL
,  `id_quadro` integer DEFAULT NULL
,  CONSTRAINT `t_nodo_ibfk_1` FOREIGN KEY (`id_prg`) REFERENCES `t_progetti` (`id_prg`) ON DELETE CASCADE
);
CREATE TABLE `t_potenza` (
  `id_potenza` integer  NOT NULL PRIMARY KEY AUTOINCREMENT
,  `id_utenza` integer  NOT NULL
,  `id_prg` integer  NOT NULL
,  `id_nodo` integer  DEFAULT NULL
,  `nome` varchar(50) DEFAULT NULL
,  `tipo` varchar(50) DEFAULT NULL
,  `DI` integer DEFAULT '0'
,  `DO` integer DEFAULT '0'
,  `potenza` float DEFAULT '0'
,  `tensione` varchar(20) DEFAULT NULL
,  `descrizione` text
,  `zona` varchar(50) DEFAULT NULL
,  `elaborato` binary(1) DEFAULT NULL
,  `id_opzione_avviamento` integer DEFAULT NULL
,  `id_blocco` integer  DEFAULT NULL
,  `Ox` float DEFAULT NULL
,  `Oy` float DEFAULT NULL
,  `dwg` varchar(50) DEFAULT NULL
,  `L` float DEFAULT NULL
,  `id_coordinamento` integer DEFAULT NULL
, NumeroFoglio TEXT, xml TEXT,  CONSTRAINT `t_potenza_ibfk_1` FOREIGN KEY (`id_utenza`) REFERENCES `t_utenza` (`id_utenza`) ON DELETE CASCADE
,  CONSTRAINT `t_potenza_ibfk_2` FOREIGN KEY (`id_prg`) REFERENCES `t_progetti` (`id_prg`) ON DELETE CASCADE
,  CONSTRAINT `t_potenza_ibfk_3` FOREIGN KEY (`id_blocco`) REFERENCES `t_blocchi` (`id_blocco`) ON DELETE SET NULL
);
CREATE TABLE `t_progetti` (
  `id_prg` integer  NOT NULL PRIMARY KEY AUTOINCREMENT
,  `nome_progetto` varchar(100) NOT NULL
,  `descrizione` text
,  `data_creazione` timestamp NULL DEFAULT current_timestamp
);
CREATE TABLE `t_quadro` (
  `id_quadro` integer  NOT NULL PRIMARY KEY AUTOINCREMENT
,  `nome` varchar(50) NOT NULL
,  `descrizione` text
);
CREATE TABLE `t_simboli_default` (
  `id_opzione` integer  NOT NULL
,  `componente` varchar(50) NOT NULL
,  `descrizione` text COLLATE BINARY
,  `id_simbolo` integer  DEFAULT NULL
);
CREATE INDEX "idx_t_coord_sezionatori_id_coordinamento" ON "t_coord_sezionatori" (`id_coordinamento`);
CREATE INDEX "idx_t_coord_salvamotore_id_coordinamento" ON "t_coord_salvamotore" (`id_coordinamento`);
CREATE INDEX "idx_t_coord_motore_id_coordinamento" ON "t_coord_motore" (`id_coordinamento`);
CREATE INDEX "idx_t_coord_contattori_id_coordinamento" ON "t_coord_contattori" (`id_coordinamento`);
CREATE INDEX "idx_t_coord_terminals_id_coordinamento" ON "t_coord_terminals" (`id_coordinamento`);
CREATE INDEX "idx_t_coord_cavi_in_quadro_id_coordinamento" ON "t_coord_cavi_in_quadro" (`id_coordinamento`);
CREATE INDEX "idx_t_coord_cavi_aux_sez_id_coordinamento" ON "t_coord_cavi_aux_sez" (`id_coordinamento`);
CREATE INDEX "idx_t_coord_cavo_sez_mot_id_coordinamento" ON "t_coord_cavo_sez_mot" (`id_coordinamento`);
CREATE INDEX "idx_t_coord_cavi_da_quadro_id_coordinamento" ON "t_coord_cavi_da_quadro" (`id_coordinamento`);
CREATE INDEX "idx_t_nodo_id_prg" ON "t_nodo" (`id_prg`);
CREATE INDEX "idx_t_potenza_id_utenza" ON "t_potenza" (`id_utenza`);
CREATE INDEX "idx_t_potenza_id_prg" ON "t_potenza" (`id_prg`);
CREATE INDEX "idx_t_potenza_t_potenza_ibfk_3" ON "t_potenza" (`id_blocco`);
CREATE TABLE t_nodi_prg (
    id_nodo    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_prg     INTEGER NOT NULL,
    nome_nodo  TEXT NOT NULL,
    descrizione TEXT,
    note       TEXT,
    tipo       TEXT,
    FOREIGN KEY (id_prg) REFERENCES t_progetti(id_prg) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "t_hw_nodo" (
	"id_nodo_hw"	INTEGER,
	"id_prg"	INTEGER NOT NULL DEFAULT 0,
	"id_nodo"	INTEGER NOT NULL,
	"id_hw"	INTEGER NOT NULL,
	"slot"	INTEGER,
	"quantita"	INTEGER DEFAULT 1,
	FOREIGN KEY("id_nodo") REFERENCES "t_nodi_prg"("id_nodo") ON DELETE CASCADE,
	FOREIGN KEY("id_hw") REFERENCES "t_cat_hw"("id_hw") ON DELETE CASCADE,
	PRIMARY KEY("id_nodo_hw" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "t_utenze_cat" (
	"id_categoria"	integer NOT NULL,
	"categoria"	varchar(100) NOT NULL,
	"visibile"	bool DEFAULT 1,
	PRIMARY KEY("id_categoria" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "t_utenze_sottocat" (
	"id_sottocategoria"	integer NOT NULL,
	"id_categoria"	integer NOT NULL,
	"sottocategoria"	varchar(100) NOT NULL,
	"descrizione"	text COLLATE BINARY,
	"visibile"	bool DEFAULT 1,
	CONSTRAINT "t_utenze_sottocat_ibfk_1" FOREIGN KEY("id_categoria") REFERENCES "t_utenze_cat"("id_categoria") ON DELETE CASCADE,
	PRIMARY KEY("id_sottocategoria" AUTOINCREMENT)
);
CREATE INDEX "idx_t_utenze_sottocat_id_categoria" ON "t_utenze_sottocat" (
	"id_categoria"
);
CREATE TABLE IF NOT EXISTS "t_utenze_opzioni" (
	"id_opzione"	integer NOT NULL,
	"id_sottocategoria"	integer NOT NULL,
	"opzione"	varchar(100) NOT NULL,
	"script_py"	varchar(255) DEFAULT NULL,
	"config_path"	varchar(255) DEFAULT NULL,
	"visibile"	bool DEFAULT 1,
	CONSTRAINT "t_utenze_opzioni_ibfk_1" FOREIGN KEY("id_sottocategoria") REFERENCES "t_utenze_sottocat"("id_sottocategoria") ON DELETE CASCADE,
	PRIMARY KEY("id_opzione" AUTOINCREMENT)
);
CREATE INDEX "idx_t_utenze_opzioni_id_sottocategoria" ON "t_utenze_opzioni" (
	"id_sottocategoria"
);
CREATE TABLE IF NOT EXISTS "t_opzioni_avviamento" (
	"id_opzione"	integer NOT NULL,
	"descrizione"	varchar(255) NOT NULL,
	"id_blocco"	integer DEFAULT NULL,
	PRIMARY KEY("id_opzione" AUTOINCREMENT),
	FOREIGN KEY("id_blocco") REFERENCES "t_blocchi"("id_blocco") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "t_tag_blocchi" (
	"id_tag"	integer NOT NULL,
	"id_blocco"	integer NOT NULL,
	"nome_tag"	varchar(50) DEFAULT NULL,
	"quadro_tag"	varchar(50) DEFAULT NULL,
	CONSTRAINT "_t_tag_blocchi_ibfk_1" FOREIGN KEY("id_blocco") REFERENCES "t_blocchi"("id_blocco") ON DELETE CASCADE,
	PRIMARY KEY("id_tag" AUTOINCREMENT)
);
CREATE INDEX "idx__t_tag_blocchi_id_blocco" ON "t_tag_blocchi" (
	"id_blocco"
);
CREATE TABLE IF NOT EXISTS "t_blocchi_potenza" (
	"id_blocco_potenza"	INTEGER,
	"id_prg"	INTEGER NOT NULL,
	"id_utenza"	INTEGER NOT NULL,
	"NumeroFoglio"	TEXT,
	"blocco_grafico"	VARCHAR(50),
	"Ox"	REAL,
	"Oy"	REAL,
	"xml"	TEXT,
	PRIMARY KEY("id_blocco_potenza" AUTOINCREMENT),
	FOREIGN KEY("id_prg") REFERENCES "t_progetti"("id_prg") ON DELETE CASCADE,
	FOREIGN KEY("id_utenza") REFERENCES "t_utenza"("id_utenza") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "t_componenti" (
	"id_componente"	integer NOT NULL,
	"id_prg"	integer NOT NULL,
	"id_utenza"	integer NOT NULL,
	"id_potenza"	integer DEFAULT NULL,
	"componente"	varchar(50) DEFAULT NULL,
	"padre_figlio"	varchar(20) DEFAULT NULL,
	"nome"	varchar(50) DEFAULT NULL,
	"quadro"	varchar(50) DEFAULT NULL,
	"taglia"	varchar(20) DEFAULT NULL,
	"funzione1"	varchar(50) DEFAULT NULL,
	"funzione2"	varchar(50) DEFAULT NULL,
	"costruttore"	varchar(50) DEFAULT NULL,
	"tipo"	varchar(50) DEFAULT NULL,
	"descrizione"	text,
	"potenza"	varchar(10) DEFAULT NULL,
	"xml"	TEXT DEFAULT NULL,
	CONSTRAINT "t_componenti_ibfk_2" FOREIGN KEY("id_utenza") REFERENCES "t_utenza"("id_utenza") ON DELETE CASCADE,
	CONSTRAINT "t_componenti_ibfk_1" FOREIGN KEY("id_prg") REFERENCES "t_progetti"("id_prg") ON DELETE CASCADE,
	PRIMARY KEY("id_componente" AUTOINCREMENT),
	CONSTRAINT "t_componenti_ibfk_3" FOREIGN KEY("id_potenza") REFERENCES "t_potenza"("id_potenza") ON DELETE CASCADE
);
CREATE INDEX "idx_t_componenti_id_prg" ON "t_componenti" (
	"id_prg"
);
CREATE INDEX "idx_t_componenti_id_utenza" ON "t_componenti" (
	"id_utenza"
);
CREATE INDEX "idx_t_componenti_t_componenti_ibfk_3" ON "t_componenti" (
	"id_potenza"
);
CREATE TABLE IF NOT EXISTS "t_blocchi" (
	"id_blocco"	integer NOT NULL,
	"categoria"	varchar(50) NOT NULL,
	"dwg"	varchar(50) DEFAULT NULL,
	"Ox"	float DEFAULT NULL,
	"Oy"	float DEFAULT NULL,
	"componente"	varchar(50) NOT NULL,
	"descrizione"	text,
	"L"	float DEFAULT NULL,
	"H"	float DEFAULT NULL,
	"slot_max"	INTEGER DEFAULT 1,
	"config_path"	TEXT DEFAULT NULL,
	PRIMARY KEY("id_blocco" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "t_fogli_memorizzati" (
	"id_foglio"	INTEGER NOT NULL,
	"id_prg"	INTEGER NOT NULL,
	"id_utenza"	INTEGER DEFAULT NULL,
	"dwg"	VARCHAR(50) NOT NULL,
	"numero_foglio"	INTEGER NOT NULL,
	"Ox"	REAL DEFAULT 0,
	"Oy"	REAL DEFAULT 0,
	"xml"	TEXT,
	FOREIGN KEY("id_prg") REFERENCES "t_progetti"("id_prg") ON DELETE CASCADE,
	FOREIGN KEY("id_utenza") REFERENCES "t_utenza"("id_utenza") ON DELETE CASCADE,
	PRIMARY KEY("id_foglio" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "t_cat_hw" (
	"id_hw"	INTEGER,
	"nome_hw"	TEXT NOT NULL,
	"descrizione_hw"	TEXT,
	"tipo"	TEXT,
	"DI"	INTEGER DEFAULT 0,
	"DO"	INTEGER DEFAULT 0,
	"AI"	INTEGER DEFAULT 0,
	"AO"	INTEGER DEFAULT 0,
	"F-DI"	INTEGER DEFAULT 0,
	"F-DO"	INTEGER DEFAULT 0,
	"Ox"	REAL DEFAULT 0.0,
	"Oy"	REAL DEFAULT 0.0,
	"L"	REAL DEFAULT 0.0,
	"H"	REAL DEFAULT 0.0,
	"blocco_grafico"	varchar(50) DEFAULT NULL,
	PRIMARY KEY("id_hw" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "t_io" (
	"id_io"	INTEGER NOT NULL,
	"id_prg"	INTEGER NOT NULL,
	"id_utenza"	INTEGER NOT NULL,
	"id_potenza"	INTEGER DEFAULT NULL,
	"id_nodo_hw"	INTEGER DEFAULT NULL,
	"id_quadro"	INTEGER DEFAULT NULL,
	"componente"	VARCHAR(50) DEFAULT NULL,
	"posizione"	INTEGER DEFAULT NULL,
	"descrizione"	TEXT NOT NULL DEFAULT NULL,
	"zona"	VARCHAR(50) DEFAULT NULL,
	"tensione"	VARCHAR(20) DEFAULT NULL,
	"taglio"	VARCHAR(50) DEFAULT NULL,
	"taglia"	VARCHAR(20) DEFAULT NULL,
	"xml"	TEXT DEFAULT NULL,
	"id_cat"	INTEGER DEFAULT NULL,
	"id_sottocat"	INTEGER DEFAULT NULL,
	"id_opzione"	INTEGER DEFAULT NULL,
	"Indirizzo"	INTEGER DEFAULT NULL,
	"Cpu"	VARCHAR(50) DEFAULT NULL,
	"Rack"	INTEGER DEFAULT NULL,
	"slot"	INTEGER DEFAULT NULL,
	"TipoIO"	VARCHAR(50) DEFAULT NULL,
	"Blocco_Grafico"	VARCHAR(50) NOT NULL DEFAULT NULL,
	"nPin"	INTEGER DEFAULT NULL,
	"ListaPin"	INTEGER DEFAULT NULL,
	"dwg"	VARCHAR(100) DEFAULT NULL,
	"quadro"	VARCHAR(50) DEFAULT NULL,
	"nome"	VARCHAR(50) DEFAULT NULL,
	"NUMM_PIN"	VARCHAR(10) DEFAULT NULL,
	"costruttore"	VARCHAR(50) DEFAULT NULL,
	"tipo"	VARCHAR(50) DEFAULT NULL,
	"Ox"	FLOAT DEFAULT NULL,
	"Oy"	FLOAT DEFAULT NULL,
	"Livello"	INTEGER DEFAULT NULL,
	"COLORE"	VARCHAR(50) DEFAULT NULL,
	"funzione1"	VARCHAR(50) DEFAULT NULL,
	"funzione2"	VARCHAR(50) DEFAULT NULL,
	FOREIGN KEY("dwg") REFERENCES "t_libreria_simb"("BlockName") ON DELETE SET NULL,
	PRIMARY KEY("id_io" AUTOINCREMENT),
	FOREIGN KEY("id_quadro") REFERENCES "t_quadro"("id_quadro") ON DELETE SET NULL,
	FOREIGN KEY("id_potenza") REFERENCES "t_potenza"("id_potenza") ON DELETE CASCADE,
	FOREIGN KEY("id_utenza") REFERENCES "t_utenza"("id_utenza") ON DELETE CASCADE,
	FOREIGN KEY("id_nodo_hw") REFERENCES "t_hw_nodo"("id_nodo_hw") ON DELETE SET NULL,
	FOREIGN KEY("id_prg") REFERENCES "t_progetti"("id_prg") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "t_libreria_simb" (
	"id_simbolo"	integer NOT NULL,
	"BlockName"	varchar(50) NOT NULL UNIQUE,
	"sigla"	Varchar(10),
	"Description_IT"	varchar(100) DEFAULT NULL,
	"Description_EN"	varchar(100) DEFAULT NULL,
	"Description_FR"	varchar(100) DEFAULT NULL,
	"Description_DE"	varchar(100) DEFAULT NULL,
	"Description_ES"	varchar(100) DEFAULT NULL,
	"Description_CZ"	varchar(100) DEFAULT NULL,
	"Description_PO"	varchar(100) DEFAULT NULL,
	"Description_FI"	varchar(100) DEFAULT NULL,
	"Description_HU"	varchar(100) DEFAULT NULL,
	"Description_SL"	varchar(100) DEFAULT NULL,
	"Description_PL"	varchar(100) DEFAULT NULL,
	"State"	char(1) DEFAULT '',
	"utilizzato"	integer NOT NULL DEFAULT '0',
	"Ox"	float DEFAULT NULL,
	"Oy"	float DEFAULT NULL,
	"L"	float DEFAULT NULL,
	"H"	float DEFAULT NULL,
	"componente"	varchar(50) DEFAULT NULL,
	"id_categoria"	varchar(50) DEFAULT NULL,
	"id_sottocategoria"	varchar(50) DEFAULT NULL,
	"tipo_simbolo"	varchar(50) DEFAULT NULL,
	"Blocco_Grafico"	varchar(50),
	"TipoIO"	varchar(50),
	PRIMARY KEY("id_simbolo" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "t_utenza" (
	"id_utenza"	integer NOT NULL,
	"id_prg"	integer NOT NULL,
	"id_nodo"	integer DEFAULT NULL,
	"nome_utenza"	varchar(100),
	"descrizione"	text,
	"categoria"	varchar(50) DEFAULT NULL,
	"tipo_comando"	varchar(50) DEFAULT NULL,
	"tensione"	varchar(20) DEFAULT NULL,
	"zona"	varchar(50) DEFAULT NULL,
	"DI"	integer DEFAULT '0',
	"DO"	integer DEFAULT '0',
	"AI"	integer DEFAULT '0',
	"AO"	integer DEFAULT '0',
	"FDI"	integer DEFAULT '0',
	"FDO"	integer DEFAULT '0',
	"potenza"	float DEFAULT '0',
	"id_cat"	integer DEFAULT NULL,
	"id_sottocat"	integer DEFAULT NULL,
	"id_opzione"	integer DEFAULT NULL,
	"elaborata"	integer DEFAULT '0',
	"taglio"	varchar(50),
	PRIMARY KEY("id_utenza" AUTOINCREMENT),
	CONSTRAINT "t_utenza_ibfk_2" FOREIGN KEY("id_nodo") REFERENCES "t_nodo"("id_nodo") ON DELETE CASCADE,
	CONSTRAINT "t_utenza_ibfk_1" FOREIGN KEY("id_prg") REFERENCES "t_progetti"("id_prg") ON DELETE CASCADE
);
CREATE INDEX "idx_t_utenza_id_prg" ON "t_utenza" (
	"id_prg"
);
CREATE INDEX "idx_t_utenza_t_utenza_ibfk_2" ON "t_utenza" (
	"id_nodo"
);

import logging
from db_config_sqlite import get_db_connection
def assegna_io_automaticamente(id_prg: int, id_nodo: int):
    """
    Scansione di tutti i moduli hardware del nodo e assegnazione automatica
    degli IO liberi (t_io.id_nodo_hw IS NULL) fino a saturare la capacità di
    ogni scheda.

    ● L’ordine di priorità con cui vengono riempiti i moduli è l’ordine dei
      loro slot (campo t_hw_nodo.slot).

    ● Per ogni modulo, gli IO della stessa tipologia (TipoIO) vengono presi
      in gruppi di posizione:
         1. interno_quadro
         2. pulsantiera
         3. bordo_macchina
         4. tutto il resto / NULL
      I gruppi sono concatenati in quest’ordine → assicurano che, se una
      scheda rimane parzialmente vuota, di solito “interno quadro” sia il
      primo ad essere servito.

    ● Capacità usate:
         – Input  Digitale  (DI16)        → colonna t_cat_hw.DI
         – Output Digitale  (DO16)        → colonna t_cat_hw.DO
         – Input  Digitale FS (FDI16)     → colonna t_cat_hw."F-DI"
         – Output Digitale FS (FDO16)     → colonna t_cat_hw."F-DO"
         – Input  Analogico (*AI4)        → colonna t_cat_hw.AI
         – Output Analogico (*AO4)        → colonna t_cat_hw.AO
      Nessuna tipologia viene “mischiata”: se il modulo è Fail-Safe
      consideriamo **solo** le colonne F-DI / F-DO e viceversa.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1️⃣  Recupero di tutti i moduli del nodo (con i campi capacità)
        query_moduli = """
            SELECT
                t_hw_nodo.id_nodo_hw,
                t_hw_nodo.id_hw,
                t_hw_nodo.slot,
                t_cat_hw.tipo AS modulo_tipo,          -- descrizione testuale (es. "Input Digitale")
                t_cat_hw.DI,
                t_cat_hw.DO,
                t_cat_hw.AI,
                t_cat_hw.AO,
                t_cat_hw."F-DI",
                t_cat_hw."F-DO"
            FROM t_hw_nodo
            JOIN t_cat_hw ON t_hw_nodo.id_hw = t_cat_hw.id_hw
            WHERE t_hw_nodo.id_prg = ? AND t_hw_nodo.id_nodo = ?
            ORDER BY t_hw_nodo.slot
        """
        cursor.execute(query_moduli, (id_prg, id_nodo))
        moduli = [dict(row) for row in cursor.fetchall()]

        if not moduli:
            return {"success": False,
                    "message": f"Nessun modulo associato al nodo {id_nodo} nel progetto {id_prg}."}

        # 2️⃣  Ciclo modulo per modulo (slot crescente)
        for modulo in moduli:
            modulo_tipo = modulo["modulo_tipo"]        # es. “Input Digitale Fail-Safe”

            # 2a. Mapping “tipo modulo” ➜ colonna capacità corrispondente
            if modulo_tipo == "Input Digitale":
                capacity_field = "DI"
            elif modulo_tipo == "Output Digitale":
                capacity_field = "DO"
            elif modulo_tipo == "Input Digitale Fail-Safe":
                capacity_field = "F-DI"
            elif modulo_tipo == "Output Digitale Fail-Safe":
                capacity_field = "F-DO"
            elif modulo_tipo in ("Input Analogico Corrente", "Input Analogico Tensione"):
                capacity_field = "AI"
            elif modulo_tipo in ("Output Analogico Corrente", "Output Analogico Tensione"):
                capacity_field = "AO"
            else:
                capacity_field = None    # tipo ignoto / non gestito

            # 2b. Skip se non troviamo la colonna o la capacità è NULL / 0
            if not capacity_field or not modulo.get(capacity_field):
                logging.info(f"Salto modulo {modulo['id_nodo_hw']} (tipo '{modulo_tipo}') – capacità non valida.")
                continue

            max_capacity = modulo[capacity_field]

            # 2c. Calcolo spazio rimanente nella scheda
            cursor.execute("""
                SELECT COUNT(*) AS cnt
                FROM t_io
                WHERE id_nodo_hw = ? AND TipoIO = ? AND id_prg = ?
            """, (modulo["id_nodo_hw"], modulo_tipo, id_prg))
            assigned_count = cursor.fetchone()["cnt"]
            spazio_rimanente = max_capacity - assigned_count
            if spazio_rimanente <= 0:
                continue   # scheda già piena

            # 2d. Estrazione IO liberi della stessa tipologia
            cursor.execute("""
                SELECT id_io, posizione
                FROM t_io
                WHERE id_nodo_hw IS NULL AND id_prg = ? AND TipoIO = ?
            """, (id_prg, modulo_tipo))
            io_non_assegnati = [dict(row) for row in cursor.fetchall()]
            if not io_non_assegnati:
                continue   # nessun IO disponibile di questo tipo

            # 2e. Ordiniamo per posizione → gruppi 1-4
            gruppo1 = [io for io in io_non_assegnati if io["posizione"] == "interno_quadro"]
            gruppo2 = [io for io in io_non_assegnati if io["posizione"] == "pulsantiera"]
            gruppo3 = [io for io in io_non_assegnati if io["posizione"] == "bordo_macchina"]
            gruppo4 = [io for io in io_non_assegnati if io["posizione"] not in
                       ("interno_quadro", "pulsantiera", "bordo_macchina")]
            io_ordinati = gruppo1 + gruppo2 + gruppo3 + gruppo4

            # 2f. Tagliamo per non eccedere la capacità residua
            da_assegnare = io_ordinati[:spazio_rimanente]

            # 2g. Aggiornamento effettivo su t_io
            for io_item in da_assegnare:
                cursor.execute("""
                    UPDATE t_io
                    SET id_nodo_hw = ?, slot = ?, Cpu = 'CPU1', Rack = '0'
                    WHERE id_io = ? AND id_prg = ?
                """, (modulo["id_nodo_hw"],
                      modulo["slot"],
                      io_item["id_io"],
                      id_prg))

            conn.commit()   # commit (modulo per modulo)

        # ► Fine ciclo moduli
        return {"success": True,
                "message": f"Assegnazione completata per il nodo {id_nodo} (progetto {id_prg})."}

    # 3️⃣  Gestione errori / rollback
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Errore in assegnazione IO: {e}")
        return {"success": False,
                "message": f"Errore durante l'assegnazione degli IO: {str(e)}"}

    # 4️⃣  Chiusura connessione
    finally:
        if conn:
            conn.close()

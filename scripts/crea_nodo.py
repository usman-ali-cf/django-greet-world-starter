import logging
import math
from datetime import datetime
from db_config_sqlite import get_db_connection




def crea_nodo_plc_automatico(id_prg):
    """
    Crea automaticamente un nuovo nodo PLC di default chiamato "CPU01" e,
    in base al conteggio degli IO in t_io per il progetto id_prg,
    inserisce nei moduli hardware (in t_hw_nodo) il numero necessario di schede.
    
    Per ogni tipologia di IO, il calcolo si basa sulla seguente logica:
    
      Tipologia                           | Scheda default         | Colonna capacità
      ----------------------------------------------------------------------------
      Input Digitale Fail-Safe            | FDI16                  | "F-DI"
      Output Digitale Fail-Safe           | FDO16                  | "F-DO"
      Input Digitale                      | DI16                   | "DI"
      Output Digitale                     | DO16                   | "DO"
      Input Analogico Corrente            | AI4 (4-20mA)           | "AI"
      Input Analogico Tensione            | AI4 (0-10V)            | "AI"
      Output Analogico Corrente           | AO4 (4-20mA)           | "AO"
      Output Analogico Tensione           | AO4 (0-10V)            | "AO"
    
    L'elaborazione avviene seguendo questo ordine:
      1. Input Digitale Fail-Safe
      2. Output Digitale Fail-Safe
      3. Input Digitale
      4. Output Digitale
      5. Input Analogico Corrente
      6. Input Analogico Tensione
      7. Output Analogico Corrente
      8. Output Analogico Tensione
      
    Se il conteggio degli IO per una tipologia supera la capacità della scheda,
    vengono inseriti il numero di moduli hardware necessari (calcolato con ceil(count/capacity)).
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if not id_prg:
            return {"error": "ID progetto non valido."}

        # 1️⃣ Verifica se esiste già il nodo CPU01
        nome_nodo = "CPU01"
        cursor.execute("""
            SELECT id_nodo FROM t_nodi_prg
            WHERE id_prg = ? AND nome_nodo = ?
        """, (id_prg, nome_nodo))
        row = cursor.fetchone()

        if row:
            id_nodo = row["id_nodo"]
            logging.info(f"Il nodo CPU01 esiste già con ID {id_nodo}.")
            cursor.execute("""
                SELECT COUNT(*) AS cnt
                FROM t_hw_nodo
                WHERE id_prg = ? AND id_nodo = ?
            """, (id_prg, id_nodo))
            count_moduli = cursor.fetchone()["cnt"]
            if count_moduli > 0:
                logging.info(f"Nodo CPU01 ha già {count_moduli} moduli. Li eliminiamo.")
                cursor.execute("""
                    DELETE FROM t_hw_nodo
                    WHERE id_prg = ? AND id_nodo = ?
                """, (id_prg, id_nodo))
                conn.commit()
        else:
            descrizione = "Nodo PLC creato automaticamente"
            note = ""
            tipo_nodo = "PLC"
            cursor.execute("""
                INSERT INTO t_nodi_prg (id_prg, nome_nodo, descrizione, note, tipo)
                VALUES (?, ?, ?, ?, ?)
            """, (id_prg, nome_nodo, descrizione, note, tipo_nodo))
            conn.commit()
            id_nodo = cursor.lastrowid
            logging.info(f"Creato nuovo nodo PLC con ID {id_nodo}")

        # 3️⃣ Definizione mappa tipologie, schede e capacità
        tipi_io = [
            "Input Digitale Fail-Safe",
            "Output Digitale Fail-Safe",
            "Input Digitale",
            "Output Digitale",
            "Input Analogico Corrente",
            "Input Analogico Tensione",
            "Output Analogico Corrente",
            "Output Analogico Tensione"
        ]
        default_schede = {
            "Input Digitale Fail-Safe": "FDI16",
            "Output Digitale Fail-Safe": "FDO16",
            "Input Digitale": "DI16",
            "Output Digitale": "DO16",
            "Input Analogico Corrente": "AI4 (4-20mA)",
            "Input Analogico Tensione": "AI4 (0-10V)",
            "Output Analogico Corrente": "AO4 (4-20mA)",
            "Output Analogico Tensione": "AO4 (0-10V)"
        }
        capacity_columns = {
            "Input Digitale Fail-Safe": "F-DI",
            "Output Digitale Fail-Safe": "F-DO",
            "Input Digitale": "DI",
            "Output Digitale": "DO",
            "Input Analogico Corrente": "AI",
            "Input Analogico Tensione": "AI",
            "Output Analogico Corrente": "AO",
            "Output Analogico Tensione": "AO"
        }

        # 4️⃣ Conteggio IO per ogni tipologia
        conteggi = {}
        for tipologia in tipi_io:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM t_io
                WHERE id_prg = ? AND TipoIO = ?
            """, (id_prg, tipologia))
            row = cursor.fetchone()
            conteggi[tipologia] = row["cnt"] if row else 0
        logging.info(f"Conteggi IO per tipologia: {conteggi}")

        # 5️⃣ Inserimento moduli hardware
        slot_counter = 1
        for tipologia in tipi_io:
            count_io = conteggi.get(tipologia, 0)
            if count_io <= 0:
                continue

            default_board = default_schede[tipologia]
            capacity_col  = capacity_columns[tipologia]

            # 🔧 QUOTING del nome colonna con "-" e alias a "capacity"
            col_quoted = f'"{capacity_col}" AS capacity'

            cursor.execute(f"""
                SELECT id_hw, nome_hw, {col_quoted}
                FROM t_cat_hw
                WHERE nome_hw = ?
            """, (default_board,))
            board = cursor.fetchone()
            if not board:
                logging.warning(f"Schema default {default_board} non trovato per tipologia {tipologia}.")
                continue

            capacity = board["capacity"]
            if not capacity or capacity <= 0:
                logging.warning(f"Capacità non valida per {default_board}.")
                continue

            num_moduli = math.ceil(count_io / capacity)
            logging.info(f"→ {tipologia}: {count_io} IO → {num_moduli} moduli ({capacity} per modulo)")

            for _ in range(num_moduli):
                cursor.execute("""
                    INSERT INTO t_hw_nodo (id_nodo, id_prg, id_hw, slot, quantita)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_nodo, id_prg, board["id_hw"], slot_counter, 1))
                slot_counter += 1

        conn.commit()
        return {
            "message": f"Nodo PLC 'CPU01' configurato con ID {id_nodo} e moduli assegnati.",
            "id_nodo": id_nodo
        }

    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Errore in creazione nodo PLC automatico: {e}")
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()
# ──────────────────────────────────────────────────────────────────────────
# scripts/carica_file_utenze_mock.py
#  • Reads the Excel file
#  • Inserts rows into T_utenza and (if potenza>0) T_potenza
#  • NO avviamento, NO PLC creation, NO IO auto-assign
# ──────────────────────────────────────────────────────────────────────────
import os
import logging
import pandas as pd
from flask import jsonify
from db_config_sqlite import get_db_connection

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

COLONNE_ESSENZIALI_UTENZE = [
    "nome_utenza", "descrizione", "tensione", "zona",
    "DI", "DO", "AI", "AO", "FDI", "FDO", "potenza"
]

# ──────────────────────────────────────────────────────────────────────────
# Helpers Excel
# ──────────────────────────────────────────────────────────────────────────
def carica_file_excel(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        logging.error("Excel non trovato: %s", path)
        return pd.DataFrame()

    try:
        df = pd.read_excel(path, sheet_name="FoglioUtenze")
        mancanti = [c for c in COLONNE_ESSENZIALI_UTENZE if c not in df.columns]
        if mancanti:
            logging.error("Colonne mancanti: %s", mancanti)
            return pd.DataFrame()
        return df
    except Exception as exc:
        logging.error("Errore lettura Excel: %s", exc)
        return pd.DataFrame()

def assegna_categoria(row):
    return "potenza" if (pd.notna(row["potenza"]) and row["potenza"] > 0) else "utenza"

# ──────────────────────────────────────────────────────────────────────────
# Helpers DB
# ──────────────────────────────────────────────────────────────────────────
def utenze_esistenti(id_prg: int) -> bool:
    conn = get_db_connection()
    cur = conn.execute("SELECT COUNT(*) FROM t_utenza WHERE id_prg=?", (id_prg,))
    exists = cur.fetchone()[0] > 0
    conn.close()
    return exists

def elimina_utenze(id_prg: int) -> None:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM t_potenza WHERE id_prg=?", (id_prg,))
    cur.execute("DELETE FROM t_utenza WHERE id_prg=?", (id_prg,))
    conn.commit()
    conn.close()
    logging.info("Utenze/potenze del progetto %s eliminate", id_prg)

def inserisci_utenze_db(df: pd.DataFrame, id_prg: int) -> int:
    conn = get_db_connection()
    cur = conn.cursor()

    q_utenza = """
        INSERT INTO t_utenza (
            id_prg, nome_utenza, descrizione, categoria,
            tensione, zona, DI, DO, AI, AO, FDI, FDO, potenza
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    q_potenza = """
        INSERT INTO t_potenza (
            id_prg, nome, id_utenza, potenza, tensione, descrizione, zona
        ) VALUES (?,?,?,?,?,?,?)
    """

    inserted = 0
    try:
        for _, r in df.iterrows():
            categoria = r["categoria"]
            cur.execute(q_utenza, (
                id_prg,
                r["nome_utenza"], r["descrizione"], categoria,
                r["tensione"], r["zona"],
                r["DI"], r["DO"], r["AI"], r["AO"],
                r["FDI"], r["FDO"], r["potenza"]
            ))
            id_utenza = cur.lastrowid

            if categoria == "potenza":
                cur.execute(q_potenza, (
                    id_prg, r["nome_utenza"], id_utenza,
                    r["potenza"], r["tensione"], r["descrizione"], r["zona"]
                ))
            inserted += 1

        conn.commit()
        logging.info("%d utenze inserite in progetto %s", inserted, id_prg)
    except Exception as exc:
        conn.rollback()
        logging.error("Errore inserimento utenze: %s", exc, exc_info=True)
        inserted = 0
    finally:
        conn.close()
    return inserted

# ──────────────────────────────────────────────────────────────────────────
# Funzione principale usata dalla route
# ──────────────────────────────────────────────────────────────────────────
def _process_excel_and_autoflow(id_prg: int, file_path: str):
    try:
        if utenze_esistenti(id_prg):
            elimina_utenze(id_prg)

        df = carica_file_excel(file_path)
        if df.empty:
            return jsonify({"message": "Excel non valido o vuoto"}), 400

        # aggiunge colonna categoria
        df["categoria"] = df.apply(assegna_categoria, axis=1)

        n = inserisci_utenze_db(df, id_prg)
        if n == 0:
            raise RuntimeError("Inserimento non riuscito")

        return jsonify({
            "message": f"Inserite {n} utenze nel progetto {id_prg}"
        }), 200

    except Exception as exc:
        logging.error("Errore _process_excel_and_autoflow: %s", exc, exc_info=True)
        return jsonify({"message": str(exc)}), 500

# ──────────────────────────────────────────────────────────────────────────
# Validatore front-end
# ──────────────────────────────────────────────────────────────────────────
def verifica_file_caricato(file_storage):
    if not file_storage or file_storage.filename == "":
        return False, "Nessun file selezionato"
    if not file_storage.filename.lower().endswith((".xlsx", ".xls", ".xlsm")):
        return False, "Formato non supportato"
    return True, "OK"

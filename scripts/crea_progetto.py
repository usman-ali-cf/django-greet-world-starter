from db_config_sqlite import get_db_connection

def crea_progetto(nome_progetto, descrizione_progetto, data_creazione):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO t_progetti (nome_progetto, descrizione, data_creazione) VALUES (?, ?, ?)",
            (nome_progetto, descrizione_progetto, data_creazione)
        )
        conn.commit()
        return "Progetto creato con successo!"
    except Exception as e:
        return f"Errore: {e}"
    finally:
        cursor.close()
        conn.close()

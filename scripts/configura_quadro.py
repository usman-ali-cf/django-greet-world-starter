from db_config_sqlite import get_db_connection

def configura_quadro(nome_quadro, tensione, info_ausiliari):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO T_nodo (nome_nodo, tipo_nodo, descrizione, id_prg) VALUES (%s, %s, %s, %s)",
            (nome_quadro, "Quadro", info_ausiliari, 1)  # ID progetto fisso per esempio
        )
        conn.commit()
        return "Quadro configurato con successo!"
    except Exception as e:
        return f"Errore: {e}"
    finally:
        cursor.close()
        conn.close()

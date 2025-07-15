#cd ProgettoSchemi_rev1.1_SQLite
#pyinstaller --onefile --add-data "mysqlite3.db;." --add-data "db_config_sqlite.py;." --add-data "templates;templates" --add-data "static;static"--add-data "file_utili;file_utili"  --add-data "scripts;scripts"--add-data "Scripts/config/opzioni_utenze;scripts/config/JSON_Blocchi" --add-data "scripts/config/opzioni_utenze;scripts/config/opzioni_utenze" --hidden-import=scripts app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, g, send_file, send_from_directory
from datetime import datetime
from scripts.crea_progetto import crea_progetto

from db_config_sqlite import get_db_connection
from scripts.carica_file_utenze_mock import _process_excel_and_autoflow, utenze_esistenti,  verifica_file_caricato
import shutil
import logging
import os, sys
from flask import session, current_app
from scripts.assegna_io import assegna_io_automaticamente
from scripts.crea_nodo import crea_nodo_plc_automatico
import json

app = Flask(__name__)

app.secret_key = "mock_secret"

@app.context_processor
def inject_id_prg():
    # Presupponendo che tu tenga in sessione l’id del progetto selezionato
    from flask import session
    return {
        "id_prg": session.get("id_progetto")
    }

@app.route('/set_session')
def set_session():
    session['username'] = 'utente'
    return "Sessione impostata"

@app.route('/clear_session')
def clear_session():
    session.clear()  # Rimuove tutti i dati
    return "Sessione cancellata"

@app.teardown_appcontext
def close_connection(exception):
    """Chiude la connessione al database al termine del contesto."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# ✅ Homepage con elenco dei progetti
@app.route('/')
def index():
    # Pulisce la sessione
    session.clear()
    
    conn = get_db_connection()
    cursor = conn.cursor()  # Per restituire i risultati come dizionario
    cursor.execute("SELECT id_prg, nome_progetto, descrizione FROM t_progetti")
    progetti = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    return render_template('index.html', progetti=progetti)

# -------------------  LISTA (GET)  -------------------
@app.route("/api/progetti")
def api_progetti():
    """Restituisce tutti i progetti in JSON (id, nome, descrizione, url)."""
    conn   = get_db_connection()
    cursor = conn.cursor()
    rows   = cursor.execute("""
        SELECT id_prg, nome_progetto, descrizione
        FROM t_progetti
        ORDER BY id_prg DESC
    """).fetchall()
    progetti = [
        {
            "id_prg": r["id_prg"],
            "nome":   r["nome_progetto"],
            "descrizione": r["descrizione"],
            "url_dettaglio": url_for(
                "route_seleziona_progetto", progetto_id=r["id_prg"]
            )
        }
        for r in rows
    ]
    return jsonify(progetti), 200


# -------------------  ELIMINA (DELETE)  -------------------
@app.route("/api/progetti/<int:id_prg>", methods=["DELETE"])
def api_elimina_progetto(id_prg):
    """
    Cancella il progetto e tutte le tabelle collegate.
    NB: qui mostro l’idea con CASCADE; adatta alle tue FK / tabelle.
    """
    conn   = get_db_connection()
    cursor = conn.cursor()
    try:
        # verifica esistenza
        cur = cursor.execute("SELECT 1 FROM t_progetti WHERE id_prg=?", (id_prg,))
        if not cur.fetchone():
            return jsonify({"error": "Progetto non trovato"}), 404

        # esempio: se cascata già a DB, basta cancellare su master
        cursor.execute("DELETE FROM t_progetti WHERE id_prg=?", (id_prg,))
        conn.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# --------- crea progetto (POST JSON) ----------
@app.route("/api/progetti", methods=["POST"])
def api_crea_progetto():
    data = request.get_json(silent=True) or {}
    nome = data.get("nome_progetto", "").strip()
    descr = data.get("descrizione_progetto", "").strip()
    if not nome or not descr:
        return jsonify({"error": "Dati mancanti"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO t_progetti (nome_progetto, descrizione)
            VALUES (?, ?)
        """, (nome, descr))
        conn.commit()
        return jsonify({"success": True, "id_prg": cursor.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

        
# ✅ Seleziona un progetto
@app.route('/progetto/<int:progetto_id>')
def route_seleziona_progetto(progetto_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM t_progetti WHERE id_prg = ?", (progetto_id,))
    progetto = cursor.fetchone()
    cursor.close()
    conn.close()

    if progetto:
        # Salva l'id_prg nella sessione
        session['id_progetto'] = progetto_id
        return render_template('progetto.html', progetto=progetto)
    
    return "Progetto non trovato", 404




#*******************************************************************************************
# Funzioni ausiliarie per la gestione dei file
#*******************************************************************************************
@app.route('/download_template')
def download_template():
    directory = os.path.join(app.root_path, 'file_utili')
    filename = 'Template.xlsx'
    return send_from_directory(directory=directory, path=filename, as_attachment=True)


# Configurazione Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# 📂 Cartella temporanea per i file caricati
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ================================================================
#   /progetto/<id_prg>/carica_file_utenze  –  revisione “auto-flow”
# ================================================================
@app.route('/progetto/<int:id_prg>/carica_file_utenze', methods=['GET', 'POST'])
def route_carica_file_utenze(id_prg):
    """
    • carica/valida excel utenze
    • se già presenti ⇒ chiede conferma eliminazione (come prima)
    • dopo il caricamento:
        1. inserisce/aggiorna utenze + potenza + IO            (carica_file_utenze)
        2. esegue la scelta/assegnazione avviamenti per ogni motore
        3. crea un nodo PLC di default (se non esiste)          (crea_nodo_plc_automatico)
        4. assegna tutti gli IO disponibili ai moduli del nodo  (assegna_io_automaticamente)
    Tutto è transaction-safe: se un passaggio fallisce si fa rollback
    e si restituisce HTTP 500 con il messaggio di errore.
    """
    # ---------- GET: semplice form upload ----------
    if request.method == 'GET':
        return render_template('carica_file_utenze.html', id_prg=id_prg)

    # ---------- POST multipart (upload da form) ----------
    if not request.is_json:
        file = request.files.get('file_utenze')
        valido, messaggio_validazione = verifica_file_caricato(file)
        if not valido:
            return jsonify({"message": messaggio_validazione}), 400

        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # se esistono utenze chiedo conferma
        if utenze_esistenti(id_prg):
            return render_template(
                'conferma_eliminazione.html',
                id_prg=id_prg,
                file_name=file.filename,
                file_path=file_path
            )

        # altrimenti procedo direttamente
        return _process_excel_and_autoflow(id_prg, file_path)

    # ---------- POST JSON (conferma eliminazione) ----------
    data = request.get_json(silent=True) or {}
    if not data.get('conferma') or not data.get('file_path'):
        return jsonify({"message": "Parametri JSON mancanti"}), 400

    return _process_excel_and_autoflow(id_prg, data['file_path'])

#*******************************************************************************************
# Funzioni per la gestione delle utenze
#*******************************************************************************************


# Configura Utenze
@app.route('/configura_utenze', methods=['GET'])
def route_configura_utenze():
    """
    Route per la configurazione delle utenze.
    """
    id_prg = request.args.get('id_prg')
    if not id_prg:
        return "Errore: ID progetto mancante", 400

    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Recupera elenco utenze ordinato: elaborata = 1 prima, poi il resto
        cursor.execute("""
            SELECT id_utenza, nome_utenza, descrizione, categoria, tipo_comando, tensione, zona, DI, DO, AI, AO, FDI, FDO, elaborata 
            FROM t_utenza 
            WHERE id_prg = ? AND categoria = 'utenza'
            ORDER BY elaborata DESC
        """, (id_prg,))
        utenze = [dict(row) for row in cursor.fetchall()]
        # Ordina in modo che quelle con elaborata=1 vengano prima
        #utenze.sort(key=lambda x: x.get('elaborata', 0), reverse=True)
        # Recupera elenco categorie
        cursor.execute("""
            SELECT id_categoria, categoria 
            FROM t_utenze_cat
            WHERE visibile = 1
        """)
        categorie = [dict(row) for row in cursor.fetchall()]
        session['utenza_params'] = {
            'id_sottocategoria': None,
            'id_opzione': None
        }
        # Renderizza il template con i dati
        return render_template(
            'configura_utenze.html',
            id_prg=id_prg,
            utenze=utenze,
            categorie=categorie
        )
    except Exception as e:
        logging.error(f"Errore nella route_configura_utenze: {e}")
        return "Errore interno del server", 500
    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------------------------
# API mock: pre-elaborazione utenze (non utilizzata in questa versione)
# --------------------------------------------------------------------
#not used
@app.route("/api/preelabora_utenze", methods=["POST"])
def preelabora_utenze():
    if "id_progetto" not in session:
        return jsonify({"error": "Nessun progetto selezionato"}), 400

    return jsonify({
        "message": "Mock: pre-elaborazione saltata (API non utilizzata)"
    }), 200




@app.route('/api/selezione_utenza', methods=['GET'])
def selezione_utenza():
    """
    API per restituire la selezione associata a un'utenza.
    """
    id_utenza = request.args.get('id_utenza')
    if not id_utenza:
        return jsonify({"error": "ID utenza mancante"}), 400

    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Recupera id_cat, id_sottocat e id_opzione per l'utenza
        cursor.execute("""
            SELECT id_cat, id_sottocat, id_opzione
            FROM t_utenza
            WHERE id_utenza = ?
        """, (id_utenza,))
        selezione = cursor.fetchone()

        if not selezione:
            return jsonify({"error": "Utenza non trovata"}), 404

        # ✅ Converti la tupla in un dizionario
        selezione_dict = {
            "id_cat": selezione[0],
            "id_sottocat": selezione[1],
            "id_opzione": selezione[2]
        }

        return jsonify({"selezione": selezione_dict}), 200

    except Exception as e:
        logging.error(f"Errore nell'API selezione_utenza: {e}")
        return jsonify({"error": "Errore interno del server"}), 500

    finally:
        cursor.close()
        conn.close()

# API per aggiornare la tabella delle utenze
@app.route('/api/aggiorna_tabella', methods=['GET'])
def aggiorna_tabella_utenze():
    """
    API per aggiornare la tabella delle utenze.
    """
    id_prg = request.args.get('id_prg')
    if not id_prg:
        return jsonify({"error": "ID progetto mancante"}), 400

    try:
        # Connessione al database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Recupera elenco utenze
        cursor.execute("""
            SELECT id_utenza, nome_utenza, descrizione, categoria, tipo_comando, tensione, zona, DI, DO, AI, AO, FDI, FDO, elaborata 
            FROM t_utenza 
            WHERE id_prg = ? AND categoria = 'utenza'
        """, (id_prg,))
        utenze = [dict(row) for row in cursor.fetchall()]
        # Ordina in modo che quelle con elaborata=1 vengano prima
        #utenze.sort(key=lambda x: x.get('elaborata', 0), reverse=True)
        return jsonify({"utenze": utenze}), 200

    except Exception as e:
        logging.error(f"Errore nell'API aggiorna_tabella_utenze: {e}")
        return jsonify({"error": "Errore interno del server"}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/api/sottocategorie', methods=['GET'])
def get_sottocategorie():
    id_categoria = request.args.get('id_categoria')
    if not id_categoria:
        return jsonify({"error": "ID categoria mancante"}), 400
        # Eliminiamo l'opzione

    session['utenza_params'] = {
        'id_sottocategoria': None,
        'id_opzione': None
        }
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_sottocategoria, sottocategoria
            FROM t_utenze_sottocat
            WHERE id_categoria = ? AND visibile = 1
        """, (id_categoria,))
        sottocategorie = [dict(row) for row in cursor.fetchall()]

        return jsonify(sottocategorie), 200
    except Exception as e:
        app.logger.error(f"Errore durante il recupero delle sottocategorie: {e}")
        return jsonify({"error": "Errore interno del server"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/reset_opzione', methods=['POST'])
def reset_opzione():
    """
    Semplice endpoint per resettare l'opzione dalla sessione
    se la sessione contiene 'utenza_params'.
    """
    try:
        # Recupera i parametri dalla sessione
        utenza_params = session.get('utenza_params', {})
        if not utenza_params:
            return jsonify({"message": "Nessun utenza_params in sessione, nulla da resettare"}), 200

        # Eliminiamo l'opzione
        if 'id_opzione' in utenza_params:
            utenza_params['id_opzione'] = None
        session['utenza_params'] = utenza_params  # Riesalva in sessione

        return jsonify({"message": "Opzione resettata dalla sessione"}), 200

    except Exception as e:
        app.logger.error(f"Errore nel reset_opzione: {e}")
        return jsonify({"error": "Errore interno del server"}), 500


@app.route('/api/opzioni', methods=['GET'])
def get_opzioni():
    id_sottocategoria = request.args.get('id_sottocategoria')
    if not id_sottocategoria:
        return jsonify({"error": "ID sottocategoria mancante"}), 400

    try:
        session['utenza_params'] = {
        'id_opzione': None
        }
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_opzione, opzione
            FROM t_utenze_opzioni
            WHERE id_sottocategoria = ? AND visibile = 1
        """, (id_sottocategoria,))
        opzioni = [dict(row) for row in cursor.fetchall()]

        app.logger.info(f"Opzioni per sottocategoria {id_sottocategoria}: {opzioni}")  # Log per debug
        return jsonify(opzioni), 200
    except Exception as e:
        app.logger.error(f"Errore durante il recupero delle opzioni: {e}")
        return jsonify({"error": "Errore interno del server"}), 500
    finally:
        cursor.close()
        conn.close()



# --------------------------------------------------------------------
# API mock: /api/dettagli
#  • Usa i contatori DI/DO/AI/AO dell’utenza
#  • Genera un elenco minimo di dettagli
# --------------------------------------------------------------------
@app.route("/api/dettagli", methods=["GET"])
def get_dettagli():
    id_prg            = request.args.get("id_prg")
    id_utenza         = request.args.get("id_utenza")
    id_categoria      = request.args.get("id_categoria")
    id_sottocategoria = request.args.get("id_sottocategoria")
    id_opzione        = request.args.get("id_opzione")

    if not all([id_prg, id_utenza, id_categoria, id_sottocategoria, id_opzione]):
        return jsonify({"error": "Parametri mancanti"}), 400

    # ── dati utenza ────────────────────────────────────────────────
    conn = get_db_connection()
    row  = conn.execute("""
        SELECT nome_utenza, zona, DI, DO, AI, AO
        FROM t_utenza
        WHERE id_utenza = ?
    """, (id_utenza,)).fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Utenza non trovata"}), 404

    dettagli = []

    def add_blocco(qta, tipo_base, label):
        for i in range(int(qta or 0)):
            dettagli.append({
                "tipo": tipo_base,
                "descrizione": f"{label}_{i+1} - {row['nome_utenza']}",
                "zona": row["zona"],
                "simboli": ["B1"]         # ← simbolo default
            })

    add_blocco(row["DI"], "Digital Input",  "DI")
    add_blocco(row["DO"], "Digital Output", "DO")
    add_blocco(row["AI"], "Analog Input",   "AI")
    add_blocco(row["AO"], "Analog Output",  "AO")

    # ── salva in sessione ─────────────────────────────────────────
    session["utenza_dettagli"] = dettagli
    session["utenza_params"] = {
        "id_prg":          id_prg,
        "id_utenza":       id_utenza,
        "id_categoria":    id_categoria,
        "id_sottocategoria": id_sottocategoria,
        "id_opzione":      id_opzione,
    }

    return jsonify({"dettagli": dettagli}), 200
# --------------------------------------------------------------------
# API mock /api/conferma – inserisce IO fissi ma completi
# --------------------------------------------------------------------
@app.route("/api/conferma", methods=["POST"])
def conferma():
    try:
        progetto_id   = session.get("id_progetto")
        utenza_params = session.get("utenza_params")     # dict con id_utenza ecc.
        dettagli      = session.get("utenza_dettagli")   # lista creata da /api/dettagli

        if not progetto_id or not utenza_params or not dettagli:
            return jsonify({"error": "Dati mancanti nella sessione"}), 400

        id_utenza        = utenza_params.get("id_utenza")
        id_cat           = utenza_params.get("id_categoria")
        id_sottocat      = utenza_params.get("id_sottocategoria")
        id_opzione       = utenza_params.get("id_opzione")

        conn = get_db_connection()
        cur  = conn.cursor()

        # cancella IO esistenti
        cur.execute("DELETE FROM t_io WHERE id_utenza = ?", (id_utenza,))

        for idx, det in enumerate(dettagli, start=1):
            cur.execute("""
                INSERT INTO t_io (
                    id_prg, id_utenza, id_cat, id_sottocat, id_opzione,
                    componente, descrizione, dwg, TipoIO, posizione,
                    Oy, Blocco_Grafico, quadro, nome
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                progetto_id,
                id_utenza,
                id_cat,
                id_sottocat,
                id_opzione,
                "default",                               # componente
                det.get("descrizione", f"IO {idx}"),
                "B1",                                    # simbolo fisso
                det.get("tipo", "Digital Input"),
                None,    # posizione
                None,    # Oy
                "BG",    # Blocco_Grafico (valore di default richiesto)
                None,    # quadro
                f"IO_{idx}"
            ))
        # ---- update t_utenza: flag elaborata = 1 ------------------
        cur.execute("""
            UPDATE t_utenza
               SET id_cat      = ?,
                   id_sottocat = ?,
                   id_opzione  = ?,
                   elaborata   = 1
             WHERE id_utenza = ?
        """, (id_cat, id_sottocat, id_opzione, id_utenza))
        conn.commit()
        tot = len(dettagli)

        return jsonify({
            "message": f"Mock: inseriti {tot} IO in t_io",
            "totale":  tot
        }), 200

    except Exception as exc:
        conn.rollback()
        app.logger.error("Errore /api/conferma (mock): %s", exc, exc_info=True)
        return jsonify({"error": str(exc)}), 500

    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass



# Configura Utenze I/O
@app.route('/configura_io', methods=['GET'])
def route_configura_io():
    id_prg = request.args.get('id_prg')
    if not id_prg:
        return "Errore: ID progetto mancante", 400
    return render_template('configura_io.html', id_prg=id_prg)



@app.route('/api/potenza', methods=['GET'])
def api_potenza():
    id_prg = request.args.get('id_prg')
    if not id_prg:
        return jsonify({"error": "ID progetto mancante"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_potenza, nome, potenza, tensione, descrizione, elaborato 
        FROM t_potenza
        WHERE id_prg = ?
    """, (id_prg,))
    utenze = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify({"utenze": utenze}), 200



@app.route('/configura_potenza', methods=['GET'])
def route_configura_potenza():
    id_prg = request.args.get('id_prg')
    if not id_prg:
        return "Errore: ID progetto mancante", 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Carica utenze di potenza
    cursor.execute("""
        SELECT id_potenza, nome, potenza, tensione, descrizione, elaborato 
        FROM t_potenza
        WHERE id_prg = ?
    """, (id_prg,))
    utenze = [dict(row) for row in cursor.fetchall()]
    
    # Carica opzioni di avviamento
    cursor.execute("""
        SELECT id_opzione, descrizione 
        FROM t_opzioni_avviamento
    """)
    opzioni = [dict(row) for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return render_template('configura_potenza.html', id_prg=id_prg, utenze=utenze, opzioni=opzioni)

#**************************************************************************************************************
#***************************** Configura Potenza  ***************************************************************
#**************************************************************************************************************
# ------------------------------------------------------------------
# MOCK: /configura_potenza/assegna_avviamento
# ------------------------------------------------------------------
@app.route("/configura_potenza/assegna_avviamento", methods=["POST"])
def route_assegna_avviamento():
    """
    Mock: assegna l’opzione d’avviamento.
    - body JSON: { "id_prg": 1, "id_potenza": 12, "opzione_avviamento": 2 }
    - esegue solo UPDATE su t_potenza (id_opzione_avviamento, elaborato)
    """
    # ---- estrai parametri -------------------------------------------------
    data = request.get_json(silent=True) or {}
    try:
        id_prg  = int(data.get("id_prg", 0))
        id_pot  = int(data.get("id_potenza", 0))
        opz     = int(data.get("opzione_avviamento", 0))
    except (TypeError, ValueError):
        return jsonify(status="error", message="Parametri non validi"), 400

    if not all([id_prg, id_pot, opz]):
        return jsonify(status="error", message="Parametri mancanti"), 400

    # ---- update DB --------------------------------------------------------
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        rows = cur.execute("""
            UPDATE t_potenza
               SET id_opzione_avviamento = ?,
                   elaborato            = 1
             WHERE id_prg = ? AND id_potenza = ?
        """, (opz, id_prg, id_pot)).rowcount
        conn.commit()

        if rows == 0:
            return jsonify(status="error",
                           message="Record t_potenza non trovato"), 404

        return jsonify(status="success",
                       updated_rows=rows,
                       id_potenza=id_pot,
                       opzione_avviamento=opz), 200

    except Exception as exc:
        conn.rollback()
        app.logger.error("Errore mock assegna_avviamento: %s", exc, exc_info=True)
        return jsonify(status="error", message=str(exc)), 500

    finally:
        cur.close()
        conn.close()


@app.route('/configura_potenza/get_opzione', methods=['GET'])
def route_get_opzione():
    from flask import request, jsonify
    
    id_potenza = request.args.get('id_potenza')
    if not id_potenza:
        return jsonify({"message": "Errore: ID potenza mancante."}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id_opzione_avviamento 
            FROM t_potenza 
            WHERE id_potenza = ?
        """, (id_potenza,))
        result = cursor.fetchone()
        return jsonify({"id_opzione_avviamento": result['id_opzione_avviamento'] if result else None})
    except Exception as e:
        print(e)
        return jsonify({"message": "Errore durante il recupero dell'opzione."}), 500
    finally:
        cursor.close()
        conn.close()

# ✅ Crea Quadro Elettrico
@app.route('/crea_quadro', methods=['GET'])
def route_crea_quadro():
    return render_template('configura_quadro.html')

#************************************************************************************************************** 
#***************************** Crea Nodi    *******************************************************************
#**************************************************************************************************************

# ✅ Crea Nodi e PLC
@app.route('/htmlpage_crea_nodo', endpoint='route_htmlpage_crea_nodo')
def route_crea_nodo():
    id_prg = request.args.get('id_prg')
    if not id_prg:
        return "Errore: ID progetto mancante", 400
    return render_template('crea_nodo.html', id_prg=id_prg)

# GET /api/lista_nodi: restituisce la lista dei nodi (tabella t_nodi_prg)
@app.route('/api/lista_nodi', methods=['GET'])
def lista_nodi():
    db = get_db_connection()
    # Prendi id_prg dalla sessione
    id_prg = session.get('id_progetto')
    if not id_prg:
        return jsonify({"error": "ID progetto non trovato in sessione"}), 400
    
    cursor = db.execute("SELECT id_nodo, nome_nodo, descrizione, note, tipo FROM t_nodi_prg WHERE id_prg = ?", (id_prg,))
    nodi_list = [dict(row) for row in cursor.fetchall()]
    return jsonify(nodi_list)

# POST /api/crea_nodo: crea un nuovo nodo in t_nodi_prg.
@app.route('/api/crea_nodo', methods=['POST'])
def crea_nodo():
    db = get_db_connection()
    data = request.get_json()
    
         # Prendi id_prg dalla sessione
    id_prg = session.get('id_progetto')
    if not id_prg:
        return jsonify({"error": "ID progetto non trovato in sessione"}), 400
    
    nome_nodo = data.get('nome_nodo')
    if not id_prg or not nome_nodo:
        return jsonify({"error": "id_prg e nome_nodo sono obbligatori"}), 400
    
    descrizione = data.get('descrizione', '')
    note = data.get('note', '')
    tipo = data.get('tipo', '')
    
    cursor = db.execute(
        "INSERT INTO t_nodi_prg (id_prg, nome_nodo, descrizione, note, tipo) VALUES (?, ?, ?, ?, ?)",
        (id_prg, nome_nodo, descrizione, note, tipo)
    )
    db.commit()
    return jsonify({"message": "Nodo creato", "id_nodo": cursor.lastrowid}), 201

# GET /api/catalogo_hw: restituisce la lista del catalogo hardware (t_cat_hw)
@app.route('/api/catalogo_hw', methods=['GET'])
def catalogo_hw():
    db = get_db_connection()
    cursor = db.execute("""
        SELECT id_hw, nome_hw, descrizione_hw, DI, DO, AI, AO, "F-DI", "F-DO"
        FROM t_cat_hw
    """)
    hw_list = [dict(row) for row in cursor.fetchall()]
    return jsonify(hw_list)

# GET /api/hw_nodo_list: restituisce i moduli hardware assegnati ad un nodo (tramite il parametro id_nodo)
@app.route('/api/hw_nodo_list', methods=['GET'])
def hw_nodo_list():
    id_nodo = request.args.get('id_nodo')
    if not id_nodo:
        return jsonify({"error": "Il parametro id_nodo è obbligatorio"}), 400

    # Prendi id_prg dalla sessione
    id_prg = session.get('id_progetto')
    if not id_prg:
        return jsonify({"error": "ID progetto non trovato in sessione"}), 400

    db = get_db_connection()
    query = """
        SELECT 
            t_hw_nodo.id_nodo_hw, 
            t_hw_nodo.id_nodo, 
            t_hw_nodo.id_hw, 
            t_hw_nodo.slot, 
            t_hw_nodo.quantita,
            t_cat_hw.nome_hw, 
            t_cat_hw.DI, 
            t_cat_hw.DO, 
            t_cat_hw.AI, 
            t_cat_hw.AO, 
            t_cat_hw."F-DI", 
            t_cat_hw."F-DO",
            t_cat_hw.tipo  -- ✅ AGGIUNTO: per filtrare gli IO non assegnati
        FROM t_hw_nodo
        JOIN t_cat_hw ON t_hw_nodo.id_hw = t_cat_hw.id_hw
        WHERE t_hw_nodo.id_nodo = ? AND t_hw_nodo.id_prg = ?
    """

    cursor = db.execute(query, (id_nodo, id_prg))
    nodo_hw_list = [dict(row) for row in cursor.fetchall()]
    return jsonify(nodo_hw_list)


# POST /api/hw_nodo_add: aggiunge un modulo hardware ad un nodo (inserisce in t_hw_nodo)
@app.route('/api/hw_nodo_add', methods=['POST'])
def hw_nodo_add():
    db = get_db_connection()  # Usa la tua funzione per ottenere la connessione
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Richiesta JSON non valida"}), 400
        
        id_nodo = data.get('id_nodo')
        id_hw = data.get('id_hw')
        quantita = data.get('quantita', 1)
        
        if not id_nodo or not id_hw:
            return jsonify({"error": "I campi id_nodo e id_hw sono obbligatori"}), 400

        # Prendi id_prg dalla sessione
        id_prg = session.get('id_progetto')
        if not id_prg:
            return jsonify({"error": "ID progetto non trovato in sessione"}), 400

        # Calcola il prossimo slot per questo nodo (incrementale)
        cursor = db.execute("SELECT MAX(slot) as max_slot FROM t_hw_nodo WHERE id_nodo = ?", (id_nodo,))
        row = cursor.fetchone()
        if row and row['max_slot'] is not None:
            slot = row['max_slot'] + 1
        else:
            slot = 1

        # Conversione di quantita in intero
        try:
            quantita = int(quantita)
        except ValueError:
            return jsonify({"error": "Il campo quantita deve essere un numero"}), 400

        # Inserisce i dati nella tabella t_hw_nodo, includendo anche id_prg
        cursor = db.execute(
            "INSERT INTO t_hw_nodo (id_nodo, id_prg, id_hw, slot, quantita) VALUES (?, ?, ?, ?, ?)",
            (id_nodo, id_prg, id_hw, slot, quantita)
        )
        db.commit()
        return jsonify({"message": "Hardware aggiunto al nodo", "id_nodo_hw": cursor.lastrowid}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()  # Stampa il traceback per il debug
        return jsonify({"error": str(e)}), 500

# DELETE /api/hw_nodo_list/<id_nodo_hw>: rimuove il modulo hardware assegnato (da t_hw_nodo)
@app.route('/api/hw_nodo_list/<int:id_nodo_hw>', methods=['DELETE'])
def hw_nodo_delete(id_nodo_hw):
    db = get_db_connection()
    try:
        # Recupera il record da eliminare per ottenere id_nodo e slot
        cursor = db.execute("SELECT id_nodo, slot FROM t_hw_nodo WHERE id_nodo_hw = ?", (id_nodo_hw,))
        record = cursor.fetchone()
        if record is None:
            return jsonify({"error": "Record non trovato"}), 404
        
        id_nodo = record["id_nodo"]
        deleted_slot = record["slot"]
        
        # Elimina il record
        db.execute("DELETE FROM t_hw_nodo WHERE id_nodo_hw = ?", (id_nodo_hw,))
        
        # Aggiorna tutti i record del nodo con slot maggiore di quello eliminato
        db.execute("UPDATE t_hw_nodo SET slot = slot - 1 WHERE id_nodo = ? AND slot > ?", (id_nodo, deleted_slot))
        
        db.commit()
        return jsonify({"message": "Hardware rimosso dal nodo", "id_nodo_hw": id_nodo_hw}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/crea_plc_automatico', methods=['POST'])
def crea_plc_automatico():
    """
    Route per la creazione automatica di un nodo PLC e l'assegnazione dei moduli hardware
    in base al conteggio degli IO per il progetto (id_prg in sessione).
    """
    try:
        id_prg = session.get('id_progetto')
        if not id_prg:
            return jsonify({"error": "ID progetto non trovato in sessione"}), 400
        
        risultato = crea_nodo_plc_automatico(id_prg)
        if "error" in risultato:
            return jsonify(risultato), 500
        else:
            return jsonify(risultato), 200
    except Exception as e:
        logging.error(f"Errore in route crea_plc_automatico: {e}")
        return jsonify({"error": str(e)}), 500


#************************************************************************************************************** 
#***************************** Assegna I/O ai Nodi*************************************************************
#**************************************************************************************************************
#GET /assegna_io: renderizza la pagina assegna_io.html
@app.route('/assegna_io', endpoint='route_assegna_io_nodi')
def route_assegna_io():
    id_prg = request.args.get('id_prg')
    if not id_prg:
        return "Errore: ID progetto mancante", 400
    return render_template('assegna_io.html', id_prg=id_prg)

#Restituisce gli I/O assegnati a un modulo.
#Il modulo viene identificato dal parametro id_modulo (che si assume venga salvato nel campo id_hw_nodo della tabella t_io).
@app.route('/api/io_unassigned', methods=['GET'])
def io_unassigned():
    id_prg = session.get("id_progetto")
    if not id_prg:
        return jsonify({"error": "ID progetto non in sessione"}), 400
    tipo_modulo = request.args.get('tipo')
    db = get_db_connection()
    try:
        # Se vuoi filtrare per tipo, fallo qui:
        if tipo_modulo:
            cursor = db.execute("""
                SELECT * FROM t_io 
                WHERE id_nodo_hw IS NULL 
                AND TipoIO = ? AND id_prg = ?
            """, (tipo_modulo,id_prg))
        else:
            cursor = db.execute("""
                SELECT * FROM t_io 
                WHERE id_nodo_hw IS NULL
            """)
        io_list = [dict(row) for row in cursor.fetchall()]
        return jsonify(io_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


#Restituisce gli I/O assegnati a un modulo.
#Il modulo viene identificato dal parametro id_modulo (che si assume venga salvato nel campo id_hw_nodo della tabella t_io).       
@app.route('/api/io_assigned', methods=['GET'])
def io_assigned():
    id_prg = session.get("id_progetto")
    if not id_prg:
        return jsonify({"error": "ID progetto non in sessione"}), 400
    
    id_modulo = request.args.get('id_modulo')  # in t_io, colonna id_nodo_hw
    if not id_modulo:
        return jsonify({"error": "Parametro 'id_modulo' mancante"}), 400

    db = get_db_connection()
    try:
        cursor = db.execute("""
            SELECT * FROM t_io
            WHERE id_nodo_hw = ? AND id_prg = ?
        """, (id_modulo,id_prg))
        io_list = [dict(row) for row in cursor.fetchall()]
        return jsonify(io_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


#a logica aggiorna la riga in t_io impostando id_nodo_hw e 
#calcolando il nuovo slot per quel modulo (calcolato come MAX(slot)+1 per quel modulo).
@app.route('/api/io_assign', methods=['POST'])
def io_assign():
    id_prg = session.get("id_progetto")
    if not id_prg:
        return jsonify({"error": "ID progetto non in sessione"}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Richiesta JSON non valida"}), 400

    id_io = data.get('id_io')
    id_modulo = data.get('id_modulo')  # questo è il valore di t_hw_nodo.id_nodo_hw
    if not id_io or not id_modulo:
        return jsonify({"error": "I campi 'id_io' e 'id_modulo' sono obbligatori"}), 400

    db = get_db_connection()
    try:
        # 1. Recupera il tipo IO dal record t_io
        cursor = db.execute("""
            SELECT TipoIO
            FROM t_io
            WHERE id_io = ?
        """, (id_io,))
        row_io = cursor.fetchone()
        if not row_io:
            return jsonify({"error": f"Nessun IO trovato con id_io={id_io}"}), 404
        io_tipo = row_io['TipoIO']

        # 2. Recupera il tipo del modulo e la capacità dalla tabella t_cat_hw tramite t_hw_nodo
        cursor = db.execute("""
            SELECT t_cat_hw.tipo AS modulo_tipo, t_cat_hw.DI, t_cat_hw.DO, t_cat_hw.AI, t_cat_hw.AO, t_cat_hw."F-DI", t_cat_hw."F-DO"
            FROM t_hw_nodo
            JOIN t_cat_hw ON t_hw_nodo.id_hw = t_cat_hw.id_hw
            WHERE t_hw_nodo.id_nodo_hw = ?
        """, (id_modulo,))
        row_modulo = cursor.fetchone()
        if not row_modulo:
            return jsonify({"error": f"Nessun modulo trovato con id_nodo_hw={id_modulo}"}), 404

        modulo_tipo = row_modulo['modulo_tipo']  # es. "Digital Input"
        capacity_field = None

        # 3. Mappa il tipo del modulo al campo capacità
        if modulo_tipo in ("Digital Input", "Input Digitale"):
            capacity_field = "DI"
        elif modulo_tipo in ("Digital Output", "Output Digitale"):
            capacity_field = "DO"
        elif modulo_tipo in ("Analog Input", "Input Analogico"):
            capacity_field = "AI"
        elif modulo_tipo in ("Analog Output", "Output Analogico"):
            capacity_field = "AO"
        # Aggiungi altri casi se necessari

        if not capacity_field:
            return jsonify({"error": f"Tipo di modulo non gestito: {modulo_tipo}"}), 400

        # 4. Verifica che il TipoIO dell'IO corrisponda al tipo del modulo
        if io_tipo != modulo_tipo:
            return jsonify({
                "message": f"L'assegnazione non è consentita: il TipoIO dell'IO ({io_tipo}) non corrisponde al tipo del modulo ({modulo_tipo})."
            }), 200

        # 5. Recupera la capacità massima per quel tipo e conta quanti IO già assegnati a questo modulo
        max_capacity = row_modulo[capacity_field]
        if not max_capacity or max_capacity <= 0:
            return jsonify({"error": f"Il modulo non supporta {modulo_tipo}."}), 400

        cursor = db.execute("""
            SELECT COUNT(*) as count_assigned
            FROM t_io
            WHERE id_nodo_hw = ? AND TipoIO = ?
        """, (id_modulo, modulo_tipo))
        row_count = cursor.fetchone()
        assigned_count = row_count['count_assigned'] if row_count else 0

        if assigned_count >= max_capacity:
            return jsonify({
                "message": f"Capacità superata per {modulo_tipo} ({assigned_count}/{max_capacity} già assegnati)."
            }), 200

        # 6. Aggiorna il record IO, assegnando il modulo (senza gestire lo slot)
        db.execute("""
            UPDATE t_io
            SET id_nodo_hw = ?
            WHERE id_io = ?
        """, (id_modulo, id_io))
        db.commit()
        return jsonify({"message": "IO assegnato con successo", "id_io": id_io}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()



# DELETE /api/io_assign: rimuove l'assegnazione di un IO da un modulo.

@app.route('/api/io_assign', methods=['DELETE'])
def io_remove():

    id_prg = session.get("id_progetto")
    if not id_prg:
        return jsonify({"error": "ID progetto non in sessione"}), 400
    id_io = request.args.get('id_io')
    if not id_io:
        return jsonify({"error": "Parametro 'id_io' mancante"}), 400

    db = get_db_connection()
    try:
        db.execute("UPDATE t_io SET id_nodo_hw = NULL, slot = NULL WHERE id_io = ?", (id_io,))
        db.commit()
        return jsonify({"message": "IO rimosso dall'assegnazione", "id_io": id_io}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()



@app.route("/api/assegna_io_automatico", methods=["POST"])
def route_assegna_io_automatico():
    """
    Esempio di chiamata:
    POST /api/assegna_io_automatico
    Body JSON: { "id_nodo": 123 }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Richiesta JSON non valida"}), 400

    id_nodo = data.get("id_nodo")
    if not id_nodo:
        return jsonify({"error": "Manca id_nodo"}), 400

    # Recuperiamo id_prg dalla session (oppure dal body, come preferisci).
    id_prg = session.get("id_progetto")
    if not id_prg:
        return jsonify({"error": "ID progetto non in sessione"}), 400

    risultato = assegna_io_automaticamente(id_prg, id_nodo)
    if risultato["success"]:
        return jsonify(risultato), 200
    else:
        return jsonify(risultato), 500
# ================================================================
#  MOCK  /api/export_io  – genera un XML fittizio in export_files
# ================================================================
@app.route("/api/export_io", methods=["POST"])
def api_export_io():
    id_prg = session.get("id_progetto")
    if not id_prg:
        return jsonify(error="ID progetto non trovato in sessione"), 400

    # directory export_files accanto all’eseguibile / sorgente
    base_path   = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.getcwd()
    export_dir  = os.path.join(base_path, "export_files")
    os.makedirs(export_dir, exist_ok=True)

    file_path   = os.path.join(export_dir, "export_io.xml")

    # contenuto XML di esempio (puoi cambiare a piacere)
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<IOExport progetto="{id_prg}">
    <Signal name="DI_1" type="DigitalInput"/>
    <Signal name="DI_2" type="DigitalInput"/>
    <Signal name="DO_1" type="DigitalOutput"/>
    <Signal name="DO_2" type="DigitalOutput"/>
</IOExport>"""

    # scrive (o sovrascrive) il file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(xml_content)

    return jsonify(
        message="Mock export generato",
        file="export_io.xml"
    ), 200


# ================================================================
#  MOCK  /download/export_io.xml  – restituisce il file generato
# ================================================================
@app.route("/download/export_io.xml")
def download_export_io():
    base_path  = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.getcwd()
    export_dir = os.path.join(base_path, "export_files")
    xml_path   = os.path.join(export_dir, "export_io.xml")

    if not os.path.exists(xml_path):
        return "File export_io.xml non generato: esegui prima /api/export_io.", 404

    # invia direttamente il file dal dossier export_files
    return send_from_directory(export_dir, "export_io.xml", as_attachment=True)


# ================================================================
#  MOCK  /api/genera_schema  – produce Schema_elettrico.csv fittizio
# ================================================================
@app.route("/api/genera_schema", methods=["POST"])
def genera_schema():
    id_prg = session.get("id_progetto")
    if not id_prg:
        return jsonify(error="ID progetto non trovato in sessione"), 400

    # cartella export_files accanto all’app
    base_path  = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.getcwd()
    export_dir = os.path.join(base_path, "export_files")
    os.makedirs(export_dir, exist_ok=True)

    csv_name   = "Schema_elettrico.csv"
    csv_path   = os.path.join(export_dir, csv_name)

    # CSV d’esempio: intestazione + 3 righe
    rows = [
        ["Foglio", "Tipo",    "Descrizione"],
        ["F1",     "Legenda", "Legenda simboli"],
        ["F2",     "Potenza", "Motori e carichi"],
        ["F3",     "IO",      "Ingressi / Uscite"]
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        for r in rows:
            f.write(";".join(r) + "\n")        # separatore ; come nei file reali

    return jsonify(
        message="Mock CSV generato con successo",
        file=csv_name
    ), 200


# ================================================================
#  UTILITY MANAGEMENT ENDPOINTS
# ================================================================

# GET /api/utenze: Get available utilities for a project
@app.route('/api/utenze', methods=['GET'])
def get_available_utilities():
    id_prg = session.get("id_progetto")
    if not id_prg:
        return jsonify({"error": "ID progetto non in sessione"}), 400
    
    db = get_db_connection()
    try:
        cursor = db.execute("""
            SELECT id_utenza, nome, tipo, stato
            FROM t_utenze
            WHERE id_prg = ?
        """, (id_prg,))
        utilities = [dict(row) for row in cursor.fetchall()]
        return jsonify(utilities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# POST /api/assegna_utenza: Assign a utility to a module
@app.route('/api/assegna_utenza', methods=['POST'])
def assign_utility():
    id_prg = session.get("id_progetto")
    if not id_prg:
        return jsonify({"error": "ID progetto non in sessione"}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Richiesta JSON non valida"}), 400
    
    id_utenza = data.get('id_utenza')
    id_modulo = data.get('id_modulo')
    if not id_utenza or not id_modulo:
        return jsonify({"error": "I campi 'id_utenza' e 'id_modulo' sono obbligatori"}), 400
    
    db = get_db_connection()
    try:
        # Check if utility is already assigned
        cursor = db.execute("""
            SELECT COUNT(*) as count
            FROM t_utenze_modulo
            WHERE id_utenza = ? AND id_modulo = ?
        """, (id_utenza, id_modulo))
        row = cursor.fetchone()
        if row['count'] > 0:
            return jsonify({"error": "L'utenza è già assegnata a questo modulo"}), 400
        
        # Insert the assignment
        db.execute("""
            INSERT INTO t_utenze_modulo (id_utenza, id_modulo, id_prg)
            VALUES (?, ?, ?)
        """, (id_utenza, id_modulo, id_prg))
        db.commit()
        return jsonify({"message": "Utenza assegnata con successo"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# POST /api/salva_assegnazioni: Save multiple utility assignments
@app.route('/api/salva_assegnazioni', methods=['POST'])
def save_assignments():
    id_prg = session.get("id_progetto")
    if not id_prg:
        return jsonify({"error": "ID progetto non in sessione"}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Richiesta JSON non valida"}), 400
    
    assignments = data.get('assignments', [])
    if not assignments:
        return jsonify({"error": "Nessuna assegnazione da salvare"}), 400
    
    db = get_db_connection()
    try:
        # Start transaction
        db.execute("BEGIN TRANSACTION")
        
        # Delete existing assignments for this project
        db.execute("DELETE FROM t_utenze_modulo WHERE id_prg = ?", (id_prg,))
        
        # Insert new assignments
        for assignment in assignments:
            id_utenza = assignment.get('id_utenza')
            id_modulo = assignment.get('id_modulo')
            if not id_utenza or not id_modulo:
                continue
                
            db.execute("""
                INSERT INTO t_utenze_modulo (id_utenza, id_modulo, id_prg)
                VALUES (?, ?, ?)
            """, (id_utenza, id_modulo, id_prg))
        
        db.commit()
        return jsonify({"message": "Assegnazioni salvate con successo"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# ================================================================
#  MOCK  /download/<filename>  – serve qualsiasi file in export_files
# ================================================================
@app.route("/download/<path:filename>")
def download_schema_file(filename):
    base_path  = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.getcwd()
    export_dir = os.path.join(base_path, "export_files")
    file_path  = os.path.join(export_dir, filename)

    if not os.path.exists(file_path):
        return f"Il file {filename} non esiste in {export_dir}.", 404

    # restituisce il file così com'è
    return send_from_directory(export_dir, filename, as_attachment=True)
@app.route('/assegna_potenza_nodi', methods=['GET'])
def route_assegna_potenza_nodi():
    return render_template('assegna_potenza_nodi.html')


# Avvia il server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


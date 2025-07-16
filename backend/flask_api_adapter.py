
"""
Flask API adapter to provide compatibility with React frontend
This bridges the existing Flask backend with the React frontend expectations
"""
from flask import Flask, jsonify, request, session, send_file
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
CORS(app, origins=['http://localhost:5173'])

# Database configuration
DATABASE_PATH = 'database.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with required tables"""
    conn = get_db_connection()
    
    # Create projects table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS progetti (
            id_prg INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_progetto TEXT NOT NULL,
            descrizione_progetto TEXT,
            data_creazione DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create nodes table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS nodi (
            id_nodo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_prg INTEGER,
            nome_nodo TEXT NOT NULL,
            descrizione TEXT,
            FOREIGN KEY (id_prg) REFERENCES progetti (id_prg)
        )
    ''')
    
    # Create hardware catalog table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS catalogo_hw (
            id_hw INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_hw TEXT NOT NULL,
            descrizione_hw TEXT,
            tipo TEXT,
            DI INTEGER DEFAULT 0,
            DO INTEGER DEFAULT 0,
            AI INTEGER DEFAULT 0,
            AO INTEGER DEFAULT 0
        )
    ''')
    
    # Create node hardware assignments table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS nodo_hw (
            id_nodo_hw INTEGER PRIMARY KEY AUTOINCREMENT,
            id_nodo INTEGER,
            id_hw INTEGER,
            slot INTEGER,
            quantita INTEGER DEFAULT 1,
            FOREIGN KEY (id_nodo) REFERENCES nodi (id_nodo),
            FOREIGN KEY (id_hw) REFERENCES catalogo_hw (id_hw)
        )
    ''')
    
    # Create IO table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS io (
            id_io INTEGER PRIMARY KEY AUTOINCREMENT,
            id_prg INTEGER,
            descrizione TEXT,
            tipo TEXT,
            id_modulo INTEGER,
            FOREIGN KEY (id_prg) REFERENCES progetti (id_prg),
            FOREIGN KEY (id_modulo) REFERENCES nodo_hw (id_nodo_hw)
        )
    ''')
    
    # Insert sample data
    cursor = conn.cursor()
    
    # Sample projects
    cursor.execute("SELECT COUNT(*) FROM progetti")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO progetti (nome_progetto, descrizione_progetto) 
            VALUES ('Progetto Test 1', 'Descrizione del progetto di test')
        """)
        cursor.execute("""
            INSERT INTO progetti (nome_progetto, descrizione_progetto) 
            VALUES ('Progetto Test 2', 'Altro progetto di esempio')
        """)
    
    # Sample hardware
    cursor.execute("SELECT COUNT(*) FROM catalogo_hw")
    if cursor.fetchone()[0] == 0:
        hw_items = [
            ('CPU_315-2DP', 'CPU principale Siemens', 'CPU', 0, 0, 0, 0),
            ('DI_16x24VDC', 'Modulo ingressi digitali 16 canali', 'DI', 16, 0, 0, 0),
            ('DO_16x24VDC', 'Modulo uscite digitali 16 canali', 'DO', 0, 16, 0, 0),
            ('AI_8x0-10V', 'Modulo ingressi analogici 8 canali', 'AI', 0, 0, 8, 0),
            ('AO_4x0-10V', 'Modulo uscite analogiche 4 canali', 'AO', 0, 0, 0, 4)
        ]
        cursor.executemany("""
            INSERT INTO catalogo_hw (nome_hw, descrizione_hw, tipo, DI, DO, AI, AO) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, hw_items)
    
    conn.commit()
    conn.close()

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Simple login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Simple authentication (replace with real auth)
    if username == 'admin' and password == 'admin':
        session['user'] = username
        return jsonify({
            'access_token': 'mock-jwt-token',
            'token_type': 'bearer',
            'user': {
                'username': username,
                'full_name': 'Administrator'
            }
        })
    else:
        return jsonify({'detail': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout endpoint"""
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """Get current user info"""
    if 'user' in session:
        return jsonify({
            'username': session['user'],
            'full_name': 'Administrator'
        })
    return jsonify({'detail': 'Not authenticated'}), 401

# Projects endpoints
@app.route('/api/progetti', methods=['GET'])
def get_projects():
    """Get all projects"""
    conn = get_db_connection()
    projects = conn.execute('''
        SELECT id_prg, nome_progetto, descrizione_progetto, data_creazione
        FROM progetti ORDER BY data_creazione DESC
    ''').fetchall()
    conn.close()
    
    return jsonify([{
        'id_prg': project['id_prg'],
        'nome_progetto': project['nome_progetto'],
        'descrizione_progetto': project['descrizione_progetto'],
        'data_creazione': project['data_creazione'],
        'url_dettaglio': f'/project/{project["id_prg"]}'
    } for project in projects])

@app.route('/api/progetti', methods=['POST'])
def create_project():
    """Create new project"""
    data = request.get_json()
    nome = data.get('nome_progetto')
    descrizione = data.get('descrizione_progetto')
    
    if not nome or not descrizione:
        return jsonify({'error': 'Nome e descrizione sono richiesti'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO progetti (nome_progetto, descrizione_progetto)
        VALUES (?, ?)
    ''', (nome, descrizione))
    
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'id_prg': project_id,
        'message': 'Progetto creato con successo'
    })

@app.route('/api/progetti/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete project"""
    conn = get_db_connection()
    conn.execute('DELETE FROM progetti WHERE id_prg = ?', (project_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Progetto eliminato con successo'})

@app.route('/api/progetto/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get project details"""
    conn = get_db_connection()
    project = conn.execute('''
        SELECT id_prg, nome_progetto, descrizione_progetto, data_creazione
        FROM progetti WHERE id_prg = ?
    ''', (project_id,)).fetchone()
    conn.close()
    
    if not project:
        return jsonify({'error': 'Progetto non trovato'}), 404
    
    return jsonify({
        'id_prg': project['id_prg'],
        'nome_progetto': project['nome_progetto'],
        'descrizione': project['descrizione_progetto'],
        'data_creazione': project['data_creazione']
    })

# Nodes endpoints
@app.route('/api/lista_nodi', methods=['GET'])
def get_nodes():
    """Get all nodes"""
    conn = get_db_connection()
    nodes = conn.execute('''
        SELECT id_nodo, nome_nodo, descrizione
        FROM nodi ORDER BY nome_nodo
    ''').fetchall()
    conn.close()
    
    return jsonify([{
        'id_nodo': node['id_nodo'],
        'nome_nodo': node['nome_nodo'],
        'descrizione': node['descrizione']
    } for node in nodes])

@app.route('/api/crea_nodo', methods=['POST'])
def create_node():
    """Create new node"""
    data = request.get_json()
    nome_nodo = data.get('nome_nodo')
    descrizione = data.get('descrizione', '')
    id_prg = data.get('id_prg', 1)  # Default to project 1
    
    if not nome_nodo:
        return jsonify({'error': 'Nome nodo è richiesto'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nodi (id_prg, nome_nodo, descrizione)
        VALUES (?, ?, ?)
    ''', (id_prg, nome_nodo, descrizione))
    
    node_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'id_nodo': node_id,
        'message': 'Nodo creato con successo'
    })

# Hardware endpoints
@app.route('/api/catalogo_hw', methods=['GET'])
def get_hardware_catalog():
    """Get hardware catalog"""
    conn = get_db_connection()
    hardware = conn.execute('''
        SELECT id_hw, nome_hw, descrizione_hw, tipo, DI, DO, AI, AO
        FROM catalogo_hw ORDER BY nome_hw
    ''').fetchall()
    conn.close()
    
    return jsonify([{
        'id_hw': hw['id_hw'],
        'nome_hw': hw['nome_hw'],
        'descrizione_hw': hw['descrizione_hw'],
        'tipo': hw['tipo'],
        'DI': hw['DI'],
        'DO': hw['DO'],
        'AI': hw['AI'],
        'AO': hw['AO']
    } for hw in hardware])

@app.route('/api/hw_nodo_list', methods=['GET'])
def get_node_hardware():
    """Get hardware assigned to a node"""
    id_nodo = request.args.get('id_nodo')
    
    conn = get_db_connection()
    hardware = conn.execute('''
        SELECT nh.id_nodo_hw, nh.slot, ch.nome_hw, ch.tipo, ch.DI, ch.DO
        FROM nodo_hw nh
        JOIN catalogo_hw ch ON nh.id_hw = ch.id_hw
        WHERE nh.id_nodo = ?
        ORDER BY nh.slot
    ''', (id_nodo,)).fetchall()
    conn.close()
    
    return jsonify([{
        'id_nodo_hw': hw['id_nodo_hw'],
        'slot': hw['slot'],
        'nome_hw': hw['nome_hw'],
        'tipo': hw['tipo'],
        'DI': hw['DI'],
        'DO': hw['DO']
    } for hw in hardware])

@app.route('/api/hw_nodo_add', methods=['POST'])
def assign_hardware_to_node():
    """Assign hardware to node"""
    data = request.get_json()
    id_nodo = data.get('id_nodo')
    id_hw = data.get('id_hw')
    quantita = data.get('quantita', 1)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get next available slot
    cursor.execute('''
        SELECT COALESCE(MAX(slot), 0) + 1 as next_slot
        FROM nodo_hw WHERE id_nodo = ?
    ''', (id_nodo,))
    next_slot = cursor.fetchone()['next_slot']
    
    cursor.execute('''
        INSERT INTO nodo_hw (id_nodo, id_hw, slot, quantita)
        VALUES (?, ?, ?, ?)
    ''', (id_nodo, id_hw, next_slot, quantita))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Hardware assegnato con successo'})

@app.route('/api/hw_nodo_list/<int:hw_id>', methods=['DELETE'])
def remove_hardware_from_node(hw_id):
    """Remove hardware from node"""
    conn = get_db_connection()
    conn.execute('DELETE FROM nodo_hw WHERE id_nodo_hw = ?', (hw_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Hardware rimosso con successo'})

# IO endpoints
@app.route('/api/io_unassigned', methods=['GET'])
def get_unassigned_io():
    """Get unassigned IO"""
    tipo = request.args.get('tipo', '')
    
    conn = get_db_connection()
    # Mock IO data for demonstration
    io_data = [
        {'id_io': 1, 'descrizione': 'Pulsante Start Motore 1', 'tipo': 'DI'},
        {'id_io': 2, 'descrizione': 'Pulsante Stop Motore 1', 'tipo': 'DI'},
        {'id_io': 3, 'descrizione': 'Sensore Temperatura', 'tipo': 'AI'},
        {'id_io': 4, 'descrizione': 'Valvola Principale', 'tipo': 'DO'},
        {'id_io': 5, 'descrizione': 'Lampada Allarme', 'tipo': 'DO'}
    ]
    conn.close()
    
    # Filter by type if specified
    if tipo:
        io_data = [io for io in io_data if io['tipo'] == tipo]
    
    return jsonify(io_data)

@app.route('/api/io_assigned', methods=['GET'])
def get_assigned_io():
    """Get IO assigned to a module"""
    id_modulo = request.args.get('id_modulo')
    
    # Mock assigned IO data
    assigned_io = []
    
    return jsonify(assigned_io)

@app.route('/api/io_assign', methods=['POST'])
def assign_io():
    """Assign IO to module"""
    data = request.get_json()
    id_io = data.get('id_io')
    id_modulo = data.get('id_modulo')
    
    # Mock assignment logic
    return jsonify({'message': 'IO assegnato con successo'})

@app.route('/api/io_assign', methods=['DELETE'])
def unassign_io():
    """Unassign IO from module"""
    id_io = request.args.get('id_io')
    
    # Mock unassignment logic
    return jsonify({'message': 'IO rimosso con successo'})

@app.route('/api/crea_plc_automatico', methods=['POST'])
def create_automatic_plc():
    """Create PLC automatically"""
    # Mock automatic PLC creation
    return jsonify({'message': 'PLC creato automaticamente con successo'})

if __name__ == '__main__':
    init_database()
    app.run(debug=True, port=5000)

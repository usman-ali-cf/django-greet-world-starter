import sqlite3
import os
import sys

# Determina il percorso del database in base a dove si trova l'eseguibile
if getattr(sys, 'frozen', False):  # Se il programma è in un EXE (PyInstaller)
    BASE_DIR = sys._MEIPASS  # Cartella temporanea usata da PyInstaller
    DB_FILE = os.path.join(os.path.dirname(sys.executable), "mysqlite3.db")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Percorso normale durante sviluppo
    DB_FILE = os.path.join(BASE_DIR, "mysqlite3.db")

print(f"[DEBUG] Il database si trova in: {DB_FILE}")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Permette di accedere ai risultati per nome colonna
    conn.execute("PRAGMA foreign_keys = ON;")  # Abilita foreign keys
    return conn


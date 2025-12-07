import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'registro.db')


def conectar_db():
    try:
        if not os.path.exists(os.path.dirname(DB_PATH)):
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        conn.execute('PRAGMA foreign_keys = ON;')
        conn.execute('PRAGMA journal_mode = WAL;')
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        raise


def init_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutores (
            id_tutor INTEGER PRIMARY KEY AUTOINCREMENT,
            rol TEXT NOT NULL,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ninos (
            id_nino INTEGER PRIMARY KEY AUTOINCREMENT,
            id_tutor INTEGER NOT NULL,
            genero TEXT NOT NULL CHECK(genero IN ('Ajolotito','Ajolotita')),
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            password_figuras TEXT NOT NULL,
            FOREIGN KEY (id_tutor) REFERENCES tutores(id_tutor) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

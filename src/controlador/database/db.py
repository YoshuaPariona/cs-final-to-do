import sqlite3

def get_connection():
    return sqlite3.connect("tareas.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Tablas: usuarios, grupos, tipo_tareas, tareas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grupos (
        idGrupo INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tareas (
        idTarea INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        idGrupo INTEGER,
        FOREIGN KEY (idGrupo) REFERENCES grupos(idGrupo)
    )
    ''')
    # Agrega más según lo que ya tienes
    conn.commit()
    conn.close()
from src.database.db import get_connection

def crear_grupo(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO grupos (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()

def listar_grupos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grupos")
    grupos = cursor.fetchall()
    conn.close()
    return grupos
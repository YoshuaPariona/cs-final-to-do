import sqlite3
import os

DB_FILE = "./todo_app.db"
SCHEMA_FILE = "./src/controlador/database/todo.sql"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica si alguna tabla ya existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()

    if not tablas:  # Si no hay ninguna tabla, crea desde schema.sql
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            sql_script = f.read()
            cursor.executescript(sql_script)
            print("[DB] Base de datos inicializada desde schema.sql")
    else:
        print("[DB] Base de datos ya inicializada")

    conn.commit()
    conn.close()

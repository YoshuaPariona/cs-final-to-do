import sqlite3
import hashlib

# Conexión a la base de datos
def get_connection():
    return sqlite3.connect("tareas.db")

# Hashear contraseña antes de guardar
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verificar contraseña al hacer login
def check_password(password, hashed):
    return hash_password(password) == hashed

# Validar si un ID existe en una tabla
def validar_id_existente(tabla, campo_id, valor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT 1 FROM {tabla} WHERE {campo_id} = ?', (valor_id,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

# Validar estado de la tarea
def estado_valido(estado):
    return estado in ["pendiente", "completada"]

# Validar prioridad de la tarea
def prioridad_valida(prioridad):
    return prioridad in ["baja", "media", "alta"]

def xd():
    pass

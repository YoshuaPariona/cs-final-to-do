import sqlite3
from src.logica.utils import get_connection, hash_password, check_password

def registrar_usuario(nombre, email, contraseña, modo_oscuro=False):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, contraseña, modoOscuro)
            VALUES (?, ?, ?, ?)
        ''', (nombre, email, hash_password(contraseña), modo_oscuro))
        conn.commit()
        print("Usuario registrado con éxito.")
    except sqlite3.IntegrityError:
        print("Error: El correo ya está registrado.")
    finally:
        conn.close()


def login(email, contraseña):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT idUsuario, contraseña FROM usuarios WHERE email = ?', (email,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and check_password(contraseña, resultado[1]):
        print(f"Login exitoso. Tu ID de usuario es: {resultado[0]}")
        return resultado[0]
    else:
        print("Email o contraseña incorrectos.")
        return None
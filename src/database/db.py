import sqlite3

def get_connection():
    return sqlite3.connect("tareas.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla: usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT UNIQUE,
        contraseña TEXT,
        modoOscuro BOOLEAN
    )
    ''')

    # Tabla: grupos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grupos (
        idGrupo INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
    )
    ''')

    # Tabla: tipo_tareas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tipo_tareas (
        idTipoTarea INTEGER PRIMARY KEY AUTOINCREMENT,
        nombreTipo TEXT,
        descripcion TEXT
    )
    ''')

    # Tabla: tareas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tareas (
        idTarea INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descripcion TEXT,
        fechaCreacion TIMESTAMP,
        fechaVencimiento TIMESTAMP,
        estado TEXT,
        prioridad TEXT,
        tipo TEXT,
        idUsuario INTEGER,
        idGrupo INTEGER,
        idTipoTarea INTEGER,
        FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario),
        FOREIGN KEY (idGrupo) REFERENCES grupos(idGrupo),
        FOREIGN KEY (idTipoTarea) REFERENCES tipo_tareas(idTipoTarea)
    )
    ''')

    conn.commit()
    conn.close()
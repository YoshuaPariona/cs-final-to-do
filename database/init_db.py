import sqlite3

def init_db():
    conn = sqlite3.connect("tareas.db")
    cursor = conn.cursor()

    usuarios = [
        ("Juan", "juan@mail.com", "1234", True),
        ("Ana", "ana@mail.com", "abcd", False),
        ("Luis", "luis@mail.com", "pass", True)
    ]

    grupos = [
        ("Trabajo",),
        ("Estudio",),
        ("Hogar",)
    ]

    tipos = [
        ("Personal", "Tarea individual"),
        ("Equipo", "Tarea hecha en grupo"),
        ("Urgente", "Tarea que requiere atención inmediata")
    ]

    tareas = [
        ("Tarea 1", "Descripción 1", "2025-05-05", "2025-05-10", "Pendiente", "Alta", "Individual", 1, 1, 1),
        ("Tarea 2", "Descripción 2", "2025-05-05", "2025-05-08", "Completada", "Media", "Grupal", 1, 2, 2),
        ("Tarea 3", "Descripción 3", "2025-05-06", "2025-05-09", "Pendiente", "Baja", "Individual", 2, 2, 1),
        ("Tarea 4", "Descripción 4", "2025-05-06", "2025-05-12", "Pendiente", "Alta", "Grupal", 3, 3, 3),
    ]

    tareas_sin_grupo = [
        ("Tarea sin grupo 1", "Descripción genérica", "2025-05-05", "2025-05-07", "Pendiente", "Media", "Individual", 1,
         None, 1),
        (
        "Tarea sin grupo 2", "Descripción genérica", "2025-05-06", "2025-05-08", "Pendiente", "Alta", "Grupal", 2, None,
        2),
        ("Tarea sin grupo 3", "Descripción genérica", "2025-05-07", "2025-05-10", "Completada", "Baja", "Individual", 3,
         None, 1),
        (
        "Tarea sin grupo 4", "Descripción genérica", "2025-05-08", "2025-05-12", "Pendiente", "Alta", "Grupal", 1, None,
        3)
    ]

    # Leer y ejecutar el esquema
    with open("schema.sql", "r", encoding="utf-8") as f:
        schema = f.read()
        cursor.executescript(schema)

    # Insertar datos de ejemplo
    cursor.executemany("INSERT INTO usuarios (nombre, email, contraseña, modoOscuro) VALUES (?, ?, ?, ?)", usuarios)
    cursor.executemany("INSERT INTO grupos (nombre) VALUES (?)", grupos)
    cursor.executemany("INSERT INTO tipo_tareas (nombreTipo, descripcion) VALUES (?, ?)", tipos)
    cursor.executemany("""INSERT INTO tareas 
        (titulo, descripcion, fechaCreacion, fechaVencimiento, estado, prioridad, tipo, idUsuario, idGrupo, idTipoTarea)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", tareas)

    cursor.executemany("""INSERT INTO tareas 
        (titulo, descripcion, fechaCreacion, fechaVencimiento, estado, prioridad, tipo, idUsuario, idGrupo, idTipoTarea)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", tareas_sin_grupo)

    conn.commit()
    conn.close()
    print("Base de datos inicializada con datos de prueba.")

def mostrar_tareas():
    conn = sqlite3.connect("tareas.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tareas.titulo, grupos.nombre 
        FROM tareas 
        LEFT JOIN grupos ON tareas.idGrupo = grupos.idGrupo
    """)
    for titulo, grupo in cursor.fetchall():
        nombre_grupo = grupo if grupo is not None else "Sin grupo"
        print(f"Nombre: {titulo} | Grupo: {nombre_grupo}")
    conn.close()

if __name__ == "__main__":
    init_db()
    mostrar_tareas()

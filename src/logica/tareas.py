from src.logica.utils import  get_connection, validar_id_existente, estado_valido, prioridad_valida
from datetime import datetime

# Crear grupo
def crear_grupo(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO grupos (nombre) VALUES (?)', (nombre,))
    conn.commit()
    conn.close()
    print(f"Grupo '{nombre}' creado con éxito.")

# Ver todos los grupos
def ver_grupos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM grupos')
    grupos = cursor.fetchall()
    conn.close()
    print("Grupos disponibles:")
    for grupo in grupos:
        print(f"{grupo[0]} - {grupo[1]}")

# Crear tarea
def crear_tarea(titulo, descripcion, fecha_vencimiento, prioridad, estado, tipo, idUsuario, idGrupo=None, idTipoTarea=None):
    if not estado_valido(estado):
        print("Estado no válido. Usa 'pendiente' o 'completada'.")
        return
    if not prioridad_valida(prioridad):
        print("Prioridad no válida. Usa 'baja', 'media' o 'alta'.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tareas (titulo, descripcion, fechaCreacion, fechaVencimiento, estado, prioridad, tipo, idUsuario, idGrupo, idTipoTarea)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, descripcion, datetime.now(), fecha_vencimiento, estado, prioridad, tipo, idUsuario, idGrupo, idTipoTarea))
    conn.commit()
    conn.close()
    print("Tarea creada con éxito.")
    print(f"Tarea creada con éxito. ID: {cursor.lastrowid}")

# Marcar tarea como completada o pendiente2
def cambiar_estado_tarea(idTarea, nuevo_estado):
    if not estado_valido(nuevo_estado):
        print("Estado inválido.")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tareas SET estado = ? WHERE idTarea = ?', (nuevo_estado, idTarea))
    if cursor.rowcount == 0:
        print("No se encontró la tarea.")
    else:
        print("Estado actualizado.")
    conn.commit()
    conn.close()

# Ver tareas del usuario
def ver_tareas_usuario(idUsuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT idTarea, titulo, estado, prioridad, fechaVencimiento FROM tareas
        WHERE idUsuario = ?
    ''', (idUsuario,))
    tareas = cursor.fetchall()
    conn.close()

    if tareas:
        print("\nTus tareas:")
        for tarea in tareas:
            print(f"{tarea[0]}. {tarea[1]} - {tarea[2]} - Prioridad: {tarea[3]} - Vence: {tarea[4]}")
    else:
        print("No tienes tareas registradas.")

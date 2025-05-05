import sqlite3
from collections import defaultdict

def mostrar_tareas():
    conn = sqlite3.connect("database/tareas.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tareas.titulo, tareas.descripcion, grupos.nombre 
        FROM tareas 
        LEFT JOIN grupos ON tareas.idGrupo = grupos.idGrupo
    """)

    tareas_por_grupo = defaultdict(list)

    for titulo, descripcion, grupo in cursor.fetchall():
        nombre_grupo = grupo if grupo is not None else "Sin grupo"
        tareas_por_grupo[nombre_grupo].append((titulo, descripcion))

    conn.close()
    return tareas_por_grupo

def cambiar_grupo_tarea(id_tarea, id_grupo):
    conn = sqlite3.connect("database/tareas.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tareas 
        SET idGrupo = ? 
        WHERE idTarea = ?
    """, (id_grupo, id_tarea))

    conn.commit()
    conn.close()

def obtener_tareas():
    conn = sqlite3.connect("database/tareas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT idTarea, titulo FROM tareas")
    tareas = cursor.fetchall()
    conn.close()
    return tareas

def obtener_grupos():
    conn = sqlite3.connect("database/tareas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT idGrupo, nombre FROM grupos")
    grupos = cursor.fetchall()
    conn.close()
    return grupos

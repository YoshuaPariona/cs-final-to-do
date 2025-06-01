from models.models import Tarea
from repositories import tareas_repo
from datetime import datetime

def crear_nueva_tarea(titulo, descripcion, idUsuario=None, idGrupo=None, idTipoTarea=None):
    nueva = Tarea(
        titulo=titulo,
        descripcion=descripcion,
        fechaVencimiento=datetime.utcnow(),
        estado="pendiente",
        prioridad="media",
        tipo="normal",
        idUsuario=idUsuario,
        idGrupo=idGrupo,
        idTipoTarea=idTipoTarea
    )
    return tareas_repo.create_tarea(nueva)

def listar_todas_las_tareas():
    return tareas_repo.get_all_tareas()

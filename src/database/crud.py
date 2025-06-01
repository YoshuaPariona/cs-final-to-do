from database import SessionLocal
from models.models import Tarea

# Create
def create_tarea(tarea: Tarea):
    session = SessionLocal()
    session.add(tarea)
    session.commit()
    session.refresh(tarea)
    session.close()
    return tarea

# Read - all
def get_all_tareas():
    session = SessionLocal()
    tareas = session.query(Tarea).all()
    session.close()
    return tareas

# Read one
def get_tarea_by_id(idTarea: int):
    session = SessionLocal()
    tarea = session.query(Tarea).get(idTarea)
    session.close()
    return tarea

# Delete
def delete_tarea(idTarea: int):
    session = SessionLocal()
    tarea = session.query(Tarea).get(idTarea)
    if tarea:
        session.delete(tarea)
        session.commit()
    session.close()


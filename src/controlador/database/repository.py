from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from typing import List, Optional

from .db import SessionLocal
from ..logica.models import Usuario, Tarea, TipoTarea, Grupo
from src.modelo.task import TaskStatus  # Si usas enums personalizados

class Repository:

    def __init__(self):
        self.db: Session = SessionLocal()

    def save_user(self, user: Usuario) -> bool:
        try:
            existing_user = self.db.query(Usuario).filter_by(email=user.email).first()
            if existing_user:
                existing_user.nombre = user.nombre
                existing_user.contraseña = user.contraseña
                existing_user.modoOscuro = user.modoOscuro
            else:
                self.db.add(user)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Error al guardar usuario: {e}")
            self.db.rollback()
            return False

    def get_user(self, email: str) -> Optional[Usuario]:
        try:
            return self.db.query(Usuario).filter_by(email=email).first()
        except SQLAlchemyError as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def delete_user(self, email: str) -> bool:
        try:
            user = self.get_user(email)
            if not user:
                return False
            self.db.delete(user)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Error al eliminar usuario: {e}")
            self.db.rollback()
            return False

    def save_task(self, task: Tarea) -> bool:
        try:
            user = self.db.query(Usuario).get(task.idUsuario)
            if not user:
                print("Usuario no existe.")
                return False

            if task.idTarea:
                existing_task = self.db.query(Tarea).filter_by(idTarea=task.idTarea).first()
                if existing_task:
                    for attr, value in task.__dict__.items():
                        if not attr.startswith('_'):
                            setattr(existing_task, attr, value)
                else:
                    return False
            else:
                self.db.add(task)

            self.db.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Error al guardar tarea: {e}")
            self.db.rollback()
            return False

    def get_user_tasks(self, idUsuario: int) -> List[Tarea]:
        try:
            return self.db.query(Tarea).filter_by(idUsuario=idUsuario).all()
        except SQLAlchemyError as e:
            print(f"Error al obtener tareas: {e}")
            return []

    def delete_task(self, idTarea: int, idUsuario: int) -> bool:
        try:
            task = self.db.query(Tarea).filter_by(idTarea=idTarea, idUsuario=idUsuario).first()
            if not task:
                return False
            self.db.delete(task)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Error al eliminar tarea: {e}")
            self.db.rollback()
            return False

    def cleanup_completed_tasks(self):
        try:
            fecha_limite = datetime.utcnow() - timedelta(days=5)
            tareas_a_borrar = self.db.query(Tarea).filter(
                Tarea.estado == TaskStatus.COMPLETED.value,
                Tarea.fechaVencimiento < fecha_limite
            ).all()
            for tarea in tareas_a_borrar:
                self.db.delete(tarea)
            self.db.commit()
        except SQLAlchemyError as e:
            print(f"Error al limpiar tareas completadas: {e}")
            self.db.rollback()

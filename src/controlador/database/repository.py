"""
Este módulo define la clase Repository, que gestiona las operaciones de base de datos
para usuarios y tareas utilizando SQLAlchemy. Proporciona métodos para guardar,
obtener, actualizar y eliminar usuarios y tareas, así como para limpiar tareas completadas.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from typing import List, Optional

from .db import SessionLocal
from ..logica.models import Usuario, Tarea, TipoTarea, Grupo
from src.modelo.task import TaskStatus

class Repository:
    """
    Clase que gestiona las operaciones de base de datos para usuarios y tareas.
    Utiliza SQLAlchemy para interactuar con la base de datos.
    """

    def __init__(self):
        """
        Inicializa una nueva sesión de base de datos.
        """
        self.db: Session = SessionLocal()

    def save_user(self, user: Usuario) -> bool:
        """
        Guarda un usuario en la base de datos. Si el usuario ya existe, lo actualiza.

        Parámetros:
        user (Usuario): El usuario a guardar o actualizar.

        Retorna:
        bool: True si la operación fue exitosa, False en caso contrario.
        """
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

    def get_email(self, email: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su correo electrónico.

        Parámetros:
        email (str): El correo electrónico del usuario a buscar.

        Retorna:
        Optional[Usuario]: El usuario encontrado o None si no existe.
        """
        try:
            return self.db.query(Usuario).filter_by(email=email).first()
        except SQLAlchemyError as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def delete_user(self, email: str) -> bool:
        """
        Elimina un usuario de la base de datos por su correo electrónico.

        Parámetros:
        email (str): El correo electrónico del usuario a eliminar.

        Retorna:
        bool: True si la operación fue exitosa, False en caso contrario.
        """
        try:
            user = self.get_email(email)
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
        """
        Guarda una tarea en la base de datos.

        Parámetros:
        task (Tarea): La tarea a guardar.

        Retorna:
        bool: True si la operación fue exitosa, False en caso contrario.
        """
        try:
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            return True
        except SQLAlchemyError as e:
            print(f"Error al guardar tarea: {e}")
            self.db.rollback()
            return False

    def get_user_tasks(self, Email: int) -> List[Tarea]:
        """
        Obtiene todas las tareas de un usuario por su correo electrónico.

        Parámetros:
        Email (str): El correo electrónico del usuario.

        Retorna:
        List[Tarea]: Una lista de tareas del usuario.
        """
        try:
            return self.db.query(Tarea).filter_by(email = Email).all()
        except SQLAlchemyError as e:
            print(f"Error al obtener tareas: {e}")
            return []

    def get_user_by_username(self, nombre: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su nombre de usuario.

        Parámetros:
        nombre (str): El nombre de usuario a buscar.

        Retorna:
        Optional[Usuario]: El usuario encontrado o None si no existe.
        """
        try:
            return self.db.query(Usuario).filter_by(nombre=nombre).first()
        except SQLAlchemyError as e:
            print(f"Error al obtener usuario por nombre: {e}")
            return None

    def delete_task(self, idTarea: int, idUsuario: int) -> bool:
        """
        Elimina una tarea de la base de datos.

        Parámetros:
        idTarea (int): El ID de la tarea a eliminar.
        idUsuario (int): El ID del usuario dueño de la tarea.

        Retorna:
        bool: True si la operación fue exitosa, False en caso contrario.
        """
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
        """
        Elimina tareas completadas que han excedido el tiempo de retención.
        """
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

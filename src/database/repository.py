from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from typing import List, Optional

from .db import SessionLocal
from src.models.models import Usuario, Tarea, TipoTarea, Grupo
from src.models.task import TaskStatus  # Si usas enums personalizados


class Repository:
    """
    Clase que maneja la persistencia de datos para usuarios y tareas.
    """

    def __init__(self):
        """Inicializa una sesión de base de datos."""
        self.db: Session = SessionLocal()

    def save_user(self, user: Usuario) -> bool:
        """
        Guarda o actualiza un usuario en la base de datos.

        Args:
            user (Usuario): Objeto usuario a guardar.

        Returns:
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
        Obtiene un usuario por su email.

        Args:
            email (str): Email del usuario.

        Returns:
            Optional[Usuario]: Usuario encontrado o None si no existe.
        """
        try:
            return self.db.query(Usuario).filter_by(email=email).first()
        except SQLAlchemyError as e:
            print(f"Error al obtener email: {e}")
            return None

    def get_user(self, email: str, password: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su email.

        Args:
            email (str): Email del usuario.

        Returns:
            Optional[Usuario]: Usuario encontrado o None si no existe.
        """
        try:
            return self.db.query(Usuario).filter_by(email=email, contraseña=password).first()
        except SQLAlchemyError as e:
            print(f"Error al obtener usuario: {e}")
            return None


    def delete_user(self, email: str) -> bool:
        """
        Elimina un usuario por su email.

        Args:
            email (str): Email del usuario a eliminar.

        Returns:
            bool: True si se eliminó, False si no existe o error.
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

        Args:
            task (Tarea): Objeto tarea a guardar.

        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        try:
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)  # Obtener ID generado
            return True
        except SQLAlchemyError as e:
            print(f"Error al guardar tarea: {e}")
            self.db.rollback()
            return False

    def get_user_tasks(self, Email: int) -> List[Tarea]:
        """
        Obtiene todas las tareas asociadas a un email de usuario.

        Args:
            Email (int): Email del usuario (debería ser str?).

        Returns:
            List[Tarea]: Lista de tareas.
        """
        try:
            return self.db.query(Tarea).filter_by(email=Email).all()
        except SQLAlchemyError as e:
            print(f"Error al obtener tareas: {e}")
            return []

    def get_user_by_username(self, nombre: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su nombre.

        Args:
            nombre (str): Nombre del usuario.

        Returns:
            Optional[Usuario]: Usuario encontrado o None.
        """
        try:
            return self.db.query(Usuario).filter_by(nombre=nombre).first()
        except SQLAlchemyError as e:
            print(f"Error al obtener usuario por nombre: {e}")
            return None

    def delete_task(self, idTarea: int, idUsuario: int) -> bool:
        """
        Elimina una tarea por su ID y el ID del usuario.

        Args:
            idTarea (int): ID de la tarea.
            idUsuario (int): ID del usuario propietario.

        Returns:
            bool: True si se eliminó, False si no existe o error.
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
        Elimina las tareas completadas hace más de 5 días.
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

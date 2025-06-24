from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from typing import List, Optional

from .db import SessionLocal
from src.models.models import Usuario, Tarea, TipoTarea, Grupo, Event
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

    def get_user(self, username_or_email: str, password: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su email o nombre de usuario y contraseña.
        """
        try:
            if '@' in username_or_email:
                return self.db.query(Usuario).filter_by(email=username_or_email, contraseña=password).first()
            else:
                return self.db.query(Usuario).filter_by(nombre=username_or_email, contraseña=password).first()
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

    def get_user_tasks(self, user_identifier) -> List[Tarea]:
        """
        Obtiene todas las tareas asociadas a un usuario (por email o idUsuario).
        """
        try:
            # Si es un email, buscar el usuario y obtener su idUsuario
            if isinstance(user_identifier, str) and '@' in user_identifier:
                user = self.get_email(user_identifier)
                if not user:
                    return []
                user_id = user.idUsuario
            elif isinstance(user_identifier, int):
                user_id = user_identifier
            else:
                return []
            return self.db.query(Tarea).filter_by(idUsuario=user_id).all()
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

    def seed_initial_users(self):
        """
        Crea los usuarios iniciales Admin y User si no existen.
        """
        try:
            admin = self.get_email('admin@gmail.com')
            if not admin:
                admin_user = Usuario(nombre='Admin', email='admin@gmail.com', contraseña='admin', modoOscuro=False)
                self.db.add(admin_user)
            user = self.get_email('user@example.com')
            if not user:
                normal_user = Usuario(nombre='User', email='user@example.com', contraseña='user123', modoOscuro=False)
                self.db.add(normal_user)
            self.db.commit()
        except Exception as e:
            print(f"Error al crear usuarios iniciales: {e}")

    def seed_initial_tasks(self):
        """
        Crea una tarea demo para cada usuario inicial si no existen tareas.
        """
        try:
            admin = self.get_email('admin@gmail.com')
            user = self.get_email('user@example.com')
            if admin:
                tareas_admin = self.get_user_tasks(admin.idUsuario)
                if not tareas_admin:
                    tarea = Tarea(
                        titulo='Demo Admin Task',
                        descripcion='Tarea de ejemplo para Admin',
                        fechaCreacion=datetime.utcnow(),
                        fechaVencimiento=datetime.utcnow(),
                        estado='todo',
                        prioridad='Importante',
                        tipo='General',
                        idUsuario=admin.idUsuario
                    )
                    self.db.add(tarea)
            if user:
                tareas_user = self.get_user_tasks(user.idUsuario)
                if not tareas_user:
                    tarea = Tarea(
                        titulo='Demo User Task',
                        descripcion='Tarea de ejemplo para User',
                        fechaCreacion=datetime.utcnow(),
                        fechaVencimiento=datetime.utcnow(),
                        estado='todo',
                        prioridad='Normal',
                        tipo='General',
                        idUsuario=user.idUsuario
                    )
                    self.db.add(tarea)
            self.db.commit()
        except Exception as e:
            print(f"Error al crear tareas iniciales: {e}")

    def save_event(self, event):
        try:
            self.db.add(event)
            self.db.commit()
            self.db.refresh(event)
            return True
        except Exception as e:
            print(f"Error al guardar evento: {e}")
            self.db.rollback()
            return False

    def get_user_events(self, user_identifier):
        try:
            if isinstance(user_identifier, str) and '@' in user_identifier:
                user = self.get_email(user_identifier)
                if not user:
                    return []
                user_id = user.idUsuario
            elif isinstance(user_identifier, int):
                user_id = user_identifier
            else:
                return []
            return self.db.query(Event).filter_by(idUsuario=user_id).all()
        except Exception as e:
            print(f"Error al obtener eventos: {e}")
            return []

    def delete_event(self, idEvento, user_identifier):
        try:
            if isinstance(user_identifier, str) and '@' in user_identifier:
                user = self.get_email(user_identifier)
                if not user:
                    return False
                user_id = user.idUsuario
            elif isinstance(user_identifier, int):
                user_id = user_identifier
            else:
                return False
            event = self.db.query(Event).filter_by(idEvento=idEvento, idUsuario=user_id).first()
            if not event:
                return False
            self.db.delete(event)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar evento: {e}")
            self.db.rollback()
            return False

from datetime import datetime
from typing import List, Optional, Tuple

from src.models.models import *
from src.models.user import User
from src.models.task import Task, TaskPriority, TaskStatus
from src.database.repository import Repository


class TaskController:
    """
    Controlador principal de la aplicación para gestión de usuarios y tareas.
    """

    def __init__(self):
        """s
        Inicializa el controlador con un repositorio y sin usuario logueado.
        """
        self.repository = Repository()
        self.current_user = None
        # Seed de usuarios y tareas iniciales
        self.repository.seed_initial_users()
        self.repository.seed_initial_tasks()

    # Controladores de usuarios

    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario.

        Args:
            username (str): Nombre de usuario.
            email (str): Correo electrónico del usuario.
            password (str): Contraseña del usuario.

        Returns:
            Tuple[bool, str]: Éxito y mensaje de resultado.
        """
        user = User(username=username, email=email, password=password)  # Modelo de logica de negocio
        is_valid, error_msg = user.validate()
        if not is_valid:
            return False, error_msg

        if self.repository.get_email(email):
            return False, "El correo ya está en uso"

        db_user = Usuario(nombre=username, email=email, contraseña=password, modoOscuro=False) # Modelo alchemy

        if self.repository.save_user(db_user):
            return True, "Usuario registrado exitosamente"
        return False, "Error al registrar usuario"

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Inicia sesión para un usuario.

        Args:
            username (str): Nombre o correo del usuario.
            password (str): Contraseña del usuario.

        Returns:
            Tuple[bool, str]: Éxito y mensaje de resultado.
        """
        user = self.repository.get_user(username, password)
        if not user:
            return False, "Usuario no encontrado"

        if user.contraseña != password:
            return False, "Contraseña incorrecta"

        self.current_user = user.email  # Guardar usuario logueado por email
        return True, "Inicio de sesión exitoso", {"email": user.email, "name": user.nombre}

    def logout(self):
        """
        Cierra la sesión del usuario actual.
        """
        self.current_user = None

    # Controladores de tareas

    def create_task(
        self,
        name: str,
        description: str,
        start_date: datetime,
        end_date: datetime,
        priority: str,
    ) -> Tuple[bool, str]:
        """
        Crea una nueva tarea para el usuario autenticado.

        Args:
            name (str): Nombre de la tarea.
            description (str): Descripción de la tarea.
            start_date (datetime): Fecha de inicio.
            end_date (datetime): Fecha de finalización.
            priority (str): Prioridad de la tarea.

        Returns:
            Tuple[bool, str]: Éxito y mensaje de resultado.
        """
        if not self.current_user:
            return False, "Usuario no autenticado"
        user = self.repository.get_email(self.current_user)
        if not user:
            return False, "Usuario no encontrado"
        from src.models.models import Tarea
        tarea = Tarea(
            titulo=name,
            descripcion=description,
            fechaCreacion=start_date,
            fechaVencimiento=end_date,
            estado='todo',
            prioridad=priority,
            tipo='General',
            idUsuario=user.idUsuario
        )
        if self.repository.save_task(tarea):
            return True, "Tarea creada exitosamente"
        return False, "Error al crear la tarea"

    def update_task(
        self,
        task_id: int,
        name: str,
        description: str,
        start_date: datetime,
        end_date: datetime,
        priority: str,
        status: str,
    ) -> Tuple[bool, str]:
        """
        Actualiza una tarea existente del usuario autenticado.

        Args:
            task_id (int): ID de la tarea a actualizar.
            name (str): Nuevo nombre.
            description (str): Nueva descripción.
            start_date (datetime): Nueva fecha de inicio.
            end_date (datetime): Nueva fecha de finalización.
            priority (str): Nueva prioridad.

        Returns:
            Tuple[bool, str]: Éxito y mensaje de resultado.
        """
        if not self.current_user:
            return False, "Usuario no autenticado"
        user = self.repository.get_email(self.current_user)
        if not user:
            return False, "Usuario no encontrado"
        from src.models.models import Tarea
        tarea = self.repository.db.query(Tarea).filter_by(idTarea=task_id, idUsuario=user.idUsuario).first()
        if not tarea:
            return False, "Tarea no encontrada"
        tarea.titulo = name
        tarea.descripcion = description
        tarea.fechaCreacion = start_date
        tarea.fechaVencimiento = end_date
        tarea.prioridad = priority
        self.repository.db.commit()
        return True, "Tarea actualizada exitosamente"

    def complete_task(self, task_id: int) -> Tuple[bool, str]:
        """
        Marca una tarea como completada.

        Args:
            task_id (int): ID de la tarea a completar.

        Returns:
            Tuple[bool, str]: Éxito y mensaje de resultado.
        """
        if not self.current_user:
            return False, "Usuario no autenticado"

        try:
            tasks = self.repository.get_user_tasks(self.current_user)
            task = next((t for t in tasks if t.task_id == task_id), None)
            if not task:
                return False, "Tarea no encontrada"

            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()

            if self.repository.save_task(task):
                return True, "Tarea completada exitosamente"
            return False, "Error al completar la tarea"

        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

    def delete_task(self, task_id: int) -> Tuple[bool, str]:
        """
        Elimina una tarea del usuario autenticado.

        Args:
            task_id (int): ID de la tarea a eliminar.

        Returns:
            Tuple[bool, str]: Éxito y mensaje de resultado.
        """
        if not self.current_user:
            return False, "Usuario no autenticado"

        if self.repository.delete_task(task_id, self.current_user):
            return True, "Tarea eliminada exitosamente"
        return False, "Error al eliminar la tarea"

    def get_tasks(self, filter_completed: bool = False) -> List[Task]:
        """
        Obtiene todas las tareas del usuario actual.

        Args:
            filter_completed (bool, optional): Si True, filtra tareas completadas.
                                               Actualmente no usado. Defaults to False.

        Returns:
            List[Task]: Lista de tareas.
        """
        if not self.current_user:
            return []
        return self.repository.get_user_tasks(self.current_user)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Obtiene una tarea por su ID para el usuario autenticado.

        Args:
            task_id (int): ID de la tarea.

        Returns:
            Optional[Task]: Tarea encontrada o None.
        """
        if not self.current_user:
            return None

        tasks = self.repository.get_user_tasks(self.current_user)
        return next((t for t in tasks if t.task_id == task_id), None)

    def cleanup_completed_tasks(self):
        """Elimina tareas completadas hace más de X días."""
        self.repository.cleanup_completed_tasks()

    def get_tasks_by_user(
        self, username: str, filter_completed: bool = False
    ) -> List[Task]:
        """
        Obtiene tareas de un usuario dado sin necesidad de login.

        Args:
            username (str): Nombre de usuario.
            filter_completed (bool, optional): Si True, filtra tareas completadas.
                                               Defaults to False.

        Returns:
            List[Task]: Lista de tareas.
        """
        user = self.repository.get_user_tasks(username)
        if not user:
            return []

        tasks = self.repository.get_user_tasks(username)
        if filter_completed:
            return [t for t in tasks if t.status != TaskStatus.COMPLETED]
        return tasks

    def get_user_tasks(self) -> List[Task]:
        """
        Obtiene tareas del usuario autenticado.

        Returns:
            List[Task]: Lista de tareas o vacía si no autenticado.
        """
        if self.current_user is None:
            return []
        return self.repository.get_user_tasks(self.current_user)

    def create_event(self, title, description, date, time, priority):
        if not self.current_user:
            return False, "Usuario no autenticado"
        from src.models.models import Event
        user = self.repository.get_email(self.current_user)
        if not user:
            return False, "Usuario no encontrado"
        event = Event(
            titulo=title,
            descripcion=description,
            fecha=date,
            hora=time,
            prioridad=priority,
            idUsuario=user.idUsuario
        )
        if self.repository.save_event(event):
            return True, "Evento creado exitosamente"
        return False, "Error al crear evento"

    def get_user_events(self):
        if not self.current_user:
            return []
        return self.repository.get_user_events(self.current_user)

    def delete_event(self, event_id):
        if not self.current_user:
            return False, "Usuario no autenticado"
        if self.repository.delete_event(event_id, self.current_user):
            return True, "Evento eliminado exitosamente"
        return False, "Error al eliminar evento"

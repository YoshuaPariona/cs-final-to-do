"""
Este módulo define el controlador principal para la gestión de usuarios y tareas en la aplicación.
Utiliza un repositorio para interactuar con la base de datos y proporciona métodos para registrar usuarios,
iniciar sesión, y gestionar tareas como creación, actualización, eliminación y obtención.
"""

from datetime import datetime
from typing import List, Optional, Tuple

from src.modelo.user import User
from src.modelo.task import Task, TaskPriority, TaskStatus
from src.controlador.database.repository import Repository


class TaskController:
    """
    Controlador principal de la aplicación para gestionar usuarios y tareas.
    """

    def __init__(self):
        """
        Inicializa el controlador con una instancia del repositorio y establece el usuario actual como None.
        """
        self.repository = Repository()
        self.current_user = None

    # Controladores de usuarios
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario en el sistema.

        Parámetros:
        username (str): Nombre de usuario.
        email (str): Correo electrónico del usuario.
        password (str): Contraseña del usuario.

        Retorna:
        Tuple[bool, str]: Una tupla que indica el éxito o fracaso de la operación y un mensaje descriptivo.
        """
        user = User(username=username, email=email, password=password)
        is_valid, error_msg = user.validate()
        if not is_valid:
            return False, error_msg

        if self.repository.get_email(email):
            return False, "El correo ya está en uso"

        db_user = User(nombre=username, email=email, contraseña=password, modoOscuro=False)

        if self.repository.save_user(db_user):
            return True, "Usuario registrado exitosamente"
        return False, "Error al registrar usuario"

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Inicia sesión para un usuario existente.

        Parámetros:
        username (str): Nombre de usuario.
        password (str): Contraseña del usuario.

        Retorna:
        Tuple[bool, str]: Una tupla que indica el éxito o fracaso de la operación y un mensaje descriptivo.
        """
        user = self.repository.get_email(username)
        if not user:
            return False, "Usuario no encontrado"

        if user.contraseña != password:
            return False, "Contraseña incorrecta"

        self.current_user = user.email  # <- esto es clave
        return True, "Inicio de sesión exitoso"

    def logout(self):
        """
        Cierra la sesión del usuario actual.
        """
        self.current_user = None

    # Controladores de tareas
    def create_task(self, name: str, description: str, start_date: datetime,
                    end_date: datetime, priority: str) -> Tuple[bool, str]:
        """
        Crea una nueva tarea para el usuario actual.

        Parámetros:
        name (str): Nombre de la tarea.
        description (str): Descripción de la tarea.
        start_date (datetime): Fecha de inicio de la tarea.
        end_date (datetime): Fecha de finalización de la tarea.
        priority (str): Prioridad de la tarea.

        Retorna:
        Tuple[bool, str]: Una tupla que indica el éxito o fracaso de la operación y un mensaje descriptivo.
        """
        if not self.current_user:
            return False, "Usuario no autenticado"

        try:
            task = Task(
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                priority=TaskPriority(priority),
                user_id=self.current_user
            )

            is_valid, error_msg = task.validate()
            if not is_valid:
                return False, error_msg

            if self.repository.save_task(task):
                return True, "Tarea creada exitosamente"

            return False, "Error al crear la tarea"

        except ValueError as e:
            return False, f"Error de validación: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

    def update_task(self, task_id: int, name: str, description: str,
                    start_date: datetime, end_date: datetime,
                    priority: str) -> Tuple[bool, str]:
        """
        Actualiza una tarea existente.

        Parámetros:
        task_id (int): ID de la tarea a actualizar.
        name (str): Nuevo nombre de la tarea.
        description (str): Nueva descripción de la tarea.
        start_date (datetime): Nueva fecha de inicio de la tarea.
        end_date (datetime): Nueva fecha de finalización de la tarea.
        priority (str): Nueva prioridad de la tarea.

        Retorna:
        Tuple[bool, str]: Una tupla que indica el éxito o fracaso de la operación y un mensaje descriptivo.
        """
        if not self.current_user:
            return False, "Usuario no autenticado"

        try:
            # Obtener tarea existente
            tasks = self.repository.get_user_tasks(self.current_user)
            task = next((t for t in tasks if t.task_id == task_id), None)
            if not task:
                return False, "Tarea no encontrada"

            # Actualizar campos
            task.name = name
            task.description = description
            task.start_date = start_date
            task.end_date = end_date
            task.priority = TaskPriority(priority)

            is_valid, error_msg = task.validate()
            if not is_valid:
                return False, error_msg

            if self.repository.save_task(task):
                return True, "Tarea actualizada exitosamente"
            return False, "Error al actualizar la tarea"

        except ValueError as e:
            return False, f"Error de validación: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

    def complete_task(self, task_id: int) -> Tuple[bool, str]:
        """
        Marca una tarea como completada.

        Parámetros:
        task_id (int): ID de la tarea a marcar como completada.

        Retorna:
        Tuple[bool, str]: Una tupla que indica el éxito o fracaso de la operación y un mensaje descriptivo.
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
        Elimina una tarea de la base de datos.

        Parámetros:
        task_id (int): ID de la tarea a eliminar.

        Retorna:
        Tuple[bool, str]: Una tupla que indica el éxito o fracaso de la operación y un mensaje descriptivo.
        """
        if not self.current_user:
            return False, "Usuario no autenticado"

        if self.repository.delete_task(task_id, self.current_user):
            return True, "Tarea eliminada exitosamente"
        return False, "Error al eliminar la tarea"

    def get_tasks(self, filter_completed: bool = False) -> List[Task]:
        """
        Obtiene las tareas del usuario actual.

        Parámetros:
        filter_completed (bool): Si es True, filtra las tareas completadas.

        Retorna:
        List[Task]: Una lista de tareas del usuario actual.
        """
        if not self.current_user:
            return []
        return self.repository.get_user_tasks(self.current_user)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Obtiene una tarea por su ID.

        Parámetros:
        task_id (int): ID de la tarea a obtener.

        Retorna:
        Optional[Task]: La tarea encontrada o None si no existe.
        """
        if not self.current_user:
            return None

        tasks = self.repository.get_user_tasks(self.current_user)
        return next((t for t in tasks if t.task_id == task_id), None)

    def cleanup_completed_tasks(self):
        """
        Limpia las tareas completadas antiguas de la base de datos.
        """
        self.repository.cleanup_completed_tasks()

    def get_tasks_by_user(self, username: str, filter_completed: bool = False) -> List[Task]:
        """
        Obtiene las tareas de un usuario por su nombre de usuario.

        Parámetros:
        username (str): Nombre de usuario.
        filter_completed (bool): Si es True, filtra las tareas completadas.

        Retorna:
        List[Task]: Una lista de tareas del usuario.
        """
        user = self.repository.get_user_tasks(username)
        if not user:
            return []

        tasks = self.repository.get_user_tasks(username)
        if filter_completed:
            return [t for t in tasks if t.status != TaskStatus.COMPLETED]
        return tasks

    def get_user_tasks(self):
        """
        Obtiene las tareas del usuario actual.

        Retorna:
        List[Task]: Una lista de tareas del usuario actual.
        """
        if self.current_user is None:
            return []
        return self.repository.get_user_tasks(self.current_user)

from datetime import datetime
from typing import List, Optional, Tuple

from src.modelo.user import User
from src.modelo.task import Task, TaskPriority, TaskStatus
from src.controlador.database.repository import Repository

class TaskController:
    """Controlador principal de la aplicación"""

    def __init__(self):
        self.repository = Repository()
        self.current_user: Optional[str] = None
    
    # Controladores de usuarios
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """Registrar nuevo usuario"""
        # Crear y validar usuario
        user = User(username=username, email=email, password=password)
        is_valid, error_msg = user.validate()
        if not is_valid:
            return False, error_msg

        # Verificar si el usuario ya existe
        if self.repository.get_user(username):
            return False, "El nombre de usuario ya está en uso"

        # Guardar usuario
        if self.repository.save_user(user):
            return True, "Usuario registrado exitosamente"
        return False, "Error al registrar usuario"

    def login(self, username: str, password: str, remember: bool = False) -> Tuple[bool, str]:
        """Autenticar usuario"""
        user = self.repository.get_user(username)
        if not user:
            return False, "Usuario no encontrado"

        if user.password != password:  # En producción usar hash
            return False, "Contraseña incorrecta"

        # Actualizar último login y remember me
        user.last_login = datetime.now()
        user.remember_me = remember
        self.repository.save_user(user)

        self.current_user = username
        return True, "Login exitoso"

    def logout(self):
        """Cerrar sesión"""
        self.current_user = None

    # Controladores de tareas
    def create_task(self, name: str, description: str, start_date: datetime,
                    end_date: datetime, priority: str) -> Tuple[bool, str]:
        """Crear nueva tarea"""
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
        """Actualizar tarea existente"""
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
        """Marcar tarea como completada"""
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
        """Eliminar tarea"""
        if not self.current_user:
            return False, "Usuario no autenticado"

        if self.repository.delete_task(task_id, self.current_user):
            return True, "Tarea eliminada exitosamente"
        return False, "Error al eliminar la tarea"

    def get_tasks(self, filter_completed: bool = False) -> List[Task]:
        """Obtener tareas del usuario actual"""
        if not self.current_user:
            return []

        tasks = self.repository.get_user_tasks(self.current_user)
        if filter_completed:
            return [t for t in tasks if t.status != TaskStatus.COMPLETED]
        return tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Obtener tarea por ID"""
        if not self.current_user:
            return None

        tasks = self.repository.get_user_tasks(self.current_user)
        return next((t for t in tasks if t.task_id == task_id), None)

    def cleanup_completed_tasks(self):
        """Limpiar tareas completadas antiguas"""
        self.repository.cleanup_completed_tasks()

    def get_tasks_by_user(self, username: str, filter_completed: bool = False) -> List[Task]:
        """Obtener tareas por nombre de usuario (sin necesidad de login actual)"""
        user = self.repository.get_user(username)
        if not user:
            return []

        tasks = self.repository.get_user_tasks(username)
        if filter_completed:
            return [t for t in tasks if t.status != TaskStatus.COMPLETED]
        return tasks
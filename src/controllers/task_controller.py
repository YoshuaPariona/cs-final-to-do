from datetime import datetime
from typing import List, Optional, Tuple
from src.models.models import Usuario, Tarea, Event
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
        if self.repository.get_user_by_email(email):
            return False, "El correo ya está en uso"
        db_user = Usuario(nombre=username, email=email, contraseña=password, modoOscuro=False) # Modelo alchemy

        if self.repository.create_user(username, email, password):
            return True, "Usuario registrado exitosamente"
        return False, "Error al registrar usuario"

    def login(self, email: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Inicia sesión para un usuario.

        Args:
            email (str): Correo del usuario.
            password (str): Contraseña del usuario.

        Returns:
            Tuple[bool, str]: Éxito y mensaje de resultado.
        """
        user = self.repository.get_user_by_email(email)
        if not user:
            return False, "Usuario no encontrado", None

        if user.contraseña != password:
            return False, "Contraseña incorrecta", None

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
        status: str = 'todo',  # Permitir status opcional, default 'todo'
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
        user = self.repository.get_user_by_email(self.current_user)
        if not user:
            return False, "Usuario no encontrado"
        # Usar el método del repositorio para crear la tarea
        tarea = self.repository.create_task(
            titulo=name,
            descripcion=description,
            fechaCreacion=start_date,
            fechaVencimiento=end_date,
            estado=status,
            prioridad=priority,
            tipo='General',
            idUsuario=user.idUsuario
        )
        if tarea:
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
        user = self.repository.get_user_by_email(self.current_user)
        if not user:
            return False, "Usuario no encontrado"
        tarea = self.repository.db.query(Tarea).filter_by(idTarea=task_id, idUsuario=user.idUsuario).first()
        if not tarea:
            return False, "Tarea no encontrada"
        tarea.titulo = name
        tarea.descripcion = description
        tarea.fechaCreacion = start_date
        tarea.fechaVencimiento = end_date
        tarea.prioridad = priority
        tarea.estado = status
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
        user = self.repository.get_user_by_email(self.current_user)
        if not user:
            return False, "Usuario no encontrado"
        tarea = self.repository.db.query(Tarea).filter_by(idTarea=task_id, idUsuario=user.idUsuario).first()
        if not tarea:
            return False, "Tarea no encontrada"
        tarea.estado = 'completed'
        tarea.fechaVencimiento = datetime.now()
        self.repository.db.commit()
        return True, "Tarea completada exitosamente"

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
        user = self.repository.get_user_by_email(self.current_user)
        if not user:
            return False, "Usuario no encontrado"
        if self.repository.delete_task(task_id, user.idUsuario):
            return True, "Tarea eliminada exitosamente"
        return False, "Error al eliminar la tarea"

    def get_tasks(self, filter_completed: bool = False) -> List[Tarea]:
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
        user = self.repository.get_user_by_email(self.current_user)
        if not user:
            return []
        tareas = self.repository.get_tasks_by_user(user.idUsuario)
        if filter_completed:
            return [t for t in tareas if t.estado != 'completed']
        return tareas

    def get_task_by_id(self, task_id: int) -> Optional[Tarea]:
        """
        Obtiene una tarea por su ID para el usuario autenticado.

        Args:
            task_id (int): ID de la tarea.

        Returns:
            Optional[Task]: Tarea encontrada o None.
        """
        if not self.current_user:
            return None
        user = self.repository.get_user_by_email(self.current_user)
        if not user:
            return None
        return self.repository.db.query(Tarea).filter_by(idTarea=task_id, idUsuario=user.idUsuario).first()

    def cleanup_completed_tasks(self):
        """Elimina tareas completadas hace más de X días."""
        self.repository.cleanup_completed_tasks()

    def create_event(self, title, description, date, time, priority):
        if not self.current_user:
            return False, "Usuario no autenticado"
        user = self.repository.get_user_by_email(self.current_user)
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
        user = self.repository.get_user_by_email(self.current_user)
        if not user:
            return []
        return self.repository.get_user_events(user.idUsuario)

    def get_user_tasks(self, *args, **kwargs):
        return self.get_tasks(*args, **kwargs)

    def delete_event(self, event_id):
        if not self.current_user:
            return False, "Usuario no autenticado"
        user = self.repository.get_user_by_email(self.current_user)
        if not user:
            return False, "Usuario no encontrado"
        if self.repository.delete_event(event_id, user.idUsuario):
            return True, "Evento eliminado exitosamente"
        return False, "Error al eliminar evento"

    def seed_initial_tasks(self):
        """Crea tareas demo para los usuarios iniciales si no existen."""
        try:
            admin = self.get_user_by_email('admin@gmail.com')
            user = self.get_user_by_email('user@example.com')
            if admin and not self.get_tasks_by_user(admin.idUsuario):
                self.create_task(
                    titulo='Demo Admin Task',
                    descripcion='Tarea de ejemplo para Admin',
                    fechaCreacion=datetime.utcnow(),
                    fechaVencimiento=datetime.utcnow(),
                    estado='todo',
                    prioridad='Importante',
                    tipo='General',
                    idUsuario=admin.idUsuario
                )
            if user and not self.get_tasks_by_user(user.idUsuario):
                self.create_task(
                    titulo='Demo User Task',
                    descripcion='Tarea de ejemplo para User',
                    fechaCreacion=datetime.utcnow(),
                    fechaVencimiento=datetime.utcnow(),
                    estado='todo',
                    prioridad='Normal',
                    tipo='General',
                    idUsuario=user.idUsuario
                )
        except Exception as e:
            print(f"Error al crear tareas iniciales: {e}")
            
    def seed_initial_users(self):
        """Crea usuarios demo si no existen."""
        try:
            if not self.get_user_by_email('admin@gmail.com'):
                self.create_user('Admin', 'admin@gmail.com', 'admin', False)
            if not self.get_user_by_email('user@example.com'):
                self.create_user('User', 'user@example.com', 'user123', False)
        except Exception as e:
            print(f"Error al crear usuarios iniciales: {e}")
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskPriority(Enum):
    """
    Enumeración que representa las prioridades posibles para una tarea.

    Atributos:
        IMPORTANT: Tarea de alta prioridad.
        NORMAL: Tarea de prioridad media.
        POSTPONABLE: Tarea que puede posponerse.
    """
    IMPORTANT = "Importante"
    NORMAL = "Normal"
    POSTPONABLE = "Postponible"


class TaskStatus(Enum):
    """
    Enumeración que representa los estados posibles de una tarea.

    Atributos:
        TODO: Tarea pendiente por realizar.
        COMPLETED: Tarea completada.
        PENDING: Tarea en espera.
    """
    TODO = "todo"
    COMPLETED = "completed"
    PENDING = "pending"


@dataclass
class Task:
    """
    Modelo de datos para representar una tarea en el sistema.

    Atributos:
        name (str): Nombre de la tarea.
        description (str): Descripción detallada de la tarea.
        start_date (datetime): Fecha y hora de inicio.
        end_date (datetime): Fecha y hora de finalización.
        priority (TaskPriority): Prioridad asignada.
        status (TaskStatus): Estado actual de la tarea.
        created_at (datetime): Fecha de creación de la tarea.
        completed_at (Optional[datetime]): Fecha en la que se completó la tarea.
        user_id (str): Identificador del usuario que creó la tarea.
        task_id (Optional[int]): Identificador único de la tarea.
    """
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    priority: TaskPriority
    status: TaskStatus = TaskStatus.TODO
    created_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None
    user_id: str = ""
    task_id: Optional[int] = None

    def validate(self) -> tuple[bool, str]:
        """
        Valida que los atributos de la tarea sean correctos.

        Returns:
            tuple[bool, str]: Una tupla con un booleano que indica si la tarea es válida,
                              y un mensaje de error en caso contrario.
        """
        if not self.name or len(self.name.strip()) < 1:
            return False, "El nombre de la tarea es requerido"

        if not self.description:
            return False, "La descripción es requerida"

        if not self.start_date or not self.end_date:
            return False, "Las fechas de inicio y fin son requeridas"

        if self.end_date < self.start_date:
            return False, "La fecha de fin no puede ser anterior a la fecha de inicio"

        if not isinstance(self.priority, TaskPriority):
            return False, "Prioridad inválida"

        return True, ""

    def calculate_duration(self) -> str:
        """
        Calcula la duración de la tarea en días, horas y minutos.

        Returns:
            str: Cadena descriptiva con la duración.
        """
        if not self.start_date or not self.end_date:
            return "No calculado"

        duration = self.end_date - self.start_date
        days = duration.days
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60

        parts = []
        if days > 0:
            parts.append(f"{days} día{'s' if days != 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hora{'s' if hours != 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minuto{'s' if minutes != 1 else ''}")

        return " y ".join(parts) if parts else "Menos de 1 minuto"

    def to_dict(self) -> dict:
        """
        Convierte la tarea a un diccionario serializable.

        Returns:
            dict: Representación en diccionario de la tarea.
        """
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "user_id": self.user_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Crea una instancia de Task a partir de un diccionario.

        Args:
            data (dict): Diccionario con los datos de la tarea.

        Returns:
            Task: Instancia creada de la clase Task.
        """
        return cls(
            task_id=data.get("task_id"),
            name=data["name"],
            description=data["description"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            priority=TaskPriority(data["priority"]),
            status=TaskStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=datetime.fromisoformat(
                data["completed_at"]
            ) if data.get("completed_at") else None,
            user_id=data["user_id"]
        )

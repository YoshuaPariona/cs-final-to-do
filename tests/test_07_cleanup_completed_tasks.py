"""
Prueba unitaria para verificar que el método de limpieza de tareas completadas
se ejecuta correctamente, incluso si no hay tareas registradas.
"""

import sys
import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Agrega el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.task import TaskPriority, TaskStatus, Task
from src.controllers.task_controller import TaskController
from src.models.models import Base


class TestCleanupCompletedTasks(unittest.TestCase):
    """
    Prueba que valida el método cleanup_completed_tasks del controlador.
    """

    def setUp(self):
        """
        Configura una base de datos SQLite en memoria y
        conecta el controlador a esta base temporal.
        """
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)

        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_cleanup_completed_tasks(self):
        """
        Ejecuta la limpieza de tareas completadas.
        Este test pasa si no se genera ninguna excepción, incluso si no hay tareas.
        """
        self.controller.cleanup_completed_tasks()

        # El test es exitoso si no ocurre error durante la ejecución
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()

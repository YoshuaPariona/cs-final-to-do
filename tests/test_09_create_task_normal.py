"""
Prueba unitaria para verificar que no se puede crear una tarea con prioridad
'normal' si no hay un usuario autenticado en sesión.
"""

import sys
import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Agrega el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.task import TaskPriority
from src.controllers.task_controller import TaskController
from src.models.models import Base


class TestCreateTaskNormal(unittest.TestCase):
    """
    Prueba que valida el intento de crear una tarea con prioridad normal sin usuario logueado.
    """

    def setUp(self):
        """
        Configura una base de datos SQLite en memoria y
        asocia el controlador a esta base temporal.
        """
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)

        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_create_task_normal(self):
        """
        Intenta crear una tarea con prioridad 'NORMAL' sin haber iniciado sesión.
        Se espera que falle y que no se cree ninguna tarea.
        """
        success, message = self.controller.create_task(
            name="Tarea normal",
            description="Tarea con prioridad normal",
            start_date=datetime(2026, 12, 29),
            end_date=datetime(2026, 12, 30),
            priority=TaskPriority.NORMAL.value
        )

        # Verifica que se rechace por falta de autenticación
        self.assertFalse(success)
        self.assertEqual(message, "Usuario no autenticado")

        # Verifica que no se haya creado ninguna tarea
        tasks = self.controller.get_user_tasks()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()

"""
Prueba unitaria para verificar que no se puede crear una tarea con prioridad
'postponible' si no hay un usuario autenticado en sesión.
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


class TestCreateTaskPostponable(unittest.TestCase):
    """
    Prueba que valida el intento de crear una tarea con prioridad postponible sin estar logueado.
    """

    def setUp(self):
        """
        Configura una base de datos SQLite en memoria y asocia
        el controlador a esta base de prueba.
        """
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)

        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_create_task_postponable(self):
        """
        Intenta crear una tarea con prioridad 'POSTPONIBLE' sin autenticación.
        Se espera que la operación falle con el mensaje correspondiente.
        """
        success, message = self.controller.create_task(
            name="Tarea postponible",
            description="Tarea con prioridad postponible",
            start_date=datetime(2026, 12, 29),
            end_date=datetime(2026, 12, 30),
            priority=TaskPriority.POSTPONABLE.value
        )

        # Validación esperada: sin sesión activa, no se permite crear tarea
        self.assertFalse(success)
        self.assertEqual(message, "Usuario no autenticado")


if __name__ == "__main__":
    unittest.main()

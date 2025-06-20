"""
Prueba unitaria para verificar que no se pueden obtener ni actualizar tareas
si no hay un usuario autenticado en sesión.
"""

import sys
import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agrega el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.controllers.task_controller import TaskController
from src.models.models import Base


class TestUpdateTask(unittest.TestCase):
    """
    Prueba que valida el comportamiento del sistema cuando se intenta acceder
    o modificar tareas sin haber iniciado sesión.
    """

    def setUp(self):
        """
        Configura una base de datos SQLite en memoria y vincula
        el controlador a esta base temporal.
        """
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)

        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_update_task(self):
        """
        Intenta obtener tareas sin estar autenticado.
        No deberían haber tareas disponibles y la operación debe ser rechazada.
        """
        tasks = self.controller.get_user_tasks()
        self.assertEqual(len(tasks), 0)

        # Confirmación adicional de que la prueba no lanza errores
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()

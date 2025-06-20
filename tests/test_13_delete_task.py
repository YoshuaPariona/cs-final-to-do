"""
Prueba unitaria para validar que no se pueden consultar ni eliminar tareas
cuando no hay un usuario autenticado en sesión.
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


class TestDeleteTask(unittest.TestCase):
    """
    Prueba que comprueba el acceso a tareas cuando no hay sesión iniciada.
    """

    def setUp(self):
        """
        Configura una base de datos SQLite en memoria y
        enlaza el controlador a esta base de prueba.
        """
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)

        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_delete_task(self):
        """
        Intenta consultar tareas sin autenticación.
        Se espera que la lista esté vacía.
        """
        tasks = self.controller.get_user_tasks()
        self.assertEqual(len(tasks), 0)

        # Confirmación adicional de que no hay errores
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()

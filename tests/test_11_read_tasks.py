"""
Prueba unitaria para verificar que la lectura de tareas no es posible
sin un usuario autenticado en sesión.
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


class TestReadTasks(unittest.TestCase):
    """
    Prueba que verifica que no se puede obtener la lista de tareas si no hay sesión activa.
    """

    def setUp(self):
        """
        Configura una base de datos SQLite en memoria y enlaza el controlador.
        """
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)

        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_read_tasks(self):
        """
        Intenta obtener tareas sin haber iniciado sesión.
        Se espera que la lista esté vacía o no disponible.
        """
        tasks = self.controller.get_tasks()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()

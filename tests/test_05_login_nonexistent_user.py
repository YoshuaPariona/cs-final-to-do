"""
Prueba unitaria para verificar que el sistema rechaza
el inicio de sesión de un usuario que no existe.
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


class TestLoginNonexistentUser(unittest.TestCase):
    """
    Prueba que simula un intento de inicio de sesión con un correo no registrado.
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

    def test_login_nonexistent_user(self):
        """
        Intenta iniciar sesión con un correo que no existe.
        Verifica que el sistema indique que el usuario no fue encontrado.
        """
        success, message, _ = self.controller.login("login123@example.com", "password123")

        self.assertFalse(success)
        self.assertIn("no encontrado", message.lower())


if __name__ == "__main__":
    unittest.main()

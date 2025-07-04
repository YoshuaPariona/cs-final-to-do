"""
Prueba unitaria para verificar que el método de logout funciona correctamente,
incluso cuando no hay un usuario logueado (caso de sesión nula).
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


class TestLogout(unittest.TestCase):
    """
    Prueba que valida el comportamiento del método logout del controlador.
    """

    def setUp(self):
        """
        Configura una base de datos SQLite en memoria y
        asocia el controlador con esta base temporal.
        """
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)

        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_logout(self):
        """
        Simula un intento de login y luego ejecuta logout.
        """
        self.controller.register_user("testuser", "test@example.com", "password123")
        self.controller.login("test@example.com", "password123")

        # current_user debe ser el email tras login
        self.assertEqual(self.controller.current_user, "test@example.com")

        # Ejecutar logout debe dejar current_user en None
        self.controller.logout()
        self.assertIsNone(self.controller.current_user)


if __name__ == "__main__":
    unittest.main()

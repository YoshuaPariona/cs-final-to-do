"""
Prueba unitaria para verificar que el inicio de sesión funciona correctamente
cuando el usuario existe y proporciona las credenciales correctas.
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


class TestLoginSuccess(unittest.TestCase):
    """
    Prueba que simula un inicio de sesión exitoso con credenciales correctas.
    """

    def setUp(self):
        """
        Configura una base de datos SQLite en memoria y
        reemplaza el repositorio del controlador con esta sesión.
        """
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)

        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_login_success(self):
        """
        Registra un usuario y luego intenta iniciar sesión.
        """
        self.controller.register_user("loginuser", "login@example.com", "password123")

        # Intentar login con el mismo correo y contraseña
        success, message, _ = self.controller.login("login@example.com", "password123")

        self.assertTrue(success)
        self.assertEqual(message, "Inicio de sesión exitoso")


if __name__ == "__main__":
    unittest.main()

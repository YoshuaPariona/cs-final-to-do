"""
Prueba unitaria para verificar que el sistema detecta un intento
de registro duplicado usando el mismo correo electrónico.
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


class TestRegisterUserDuplicate(unittest.TestCase):
    """
    Prueba que simula un intento de registro de usuario con email duplicado.
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

    def test_register_user_duplicate(self):
        """
        Intenta registrar dos usuarios con el mismo correo.
        Verifica que el segundo intento falle por duplicidad.
        """
        # Primer registro
        self.controller.register_user("testuser", "test@example.com", "password123")

        # Segundo registro con el mismo correo
        success, message = self.controller.register_user(
            username="testuser2",
            email="test@example.com",  # Email duplicado
            password="password123"
        )

        self.assertFalse(success)
        self.assertEqual(message, "El correo ya está en uso")


if __name__ == "__main__":
    unittest.main()

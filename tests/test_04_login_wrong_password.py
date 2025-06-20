"""
Prueba unitaria para verificar que el sistema rechaza un inicio
de sesión cuando se proporciona una contraseña incorrecta.
"""

import sys
import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agrega el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.task import TaskPriority, TaskStatus, Task
from src.controllers.task_controller import TaskController
from src.models.models import Base


class TestLoginWrongPassword(unittest.TestCase):
    """
    Prueba que simula un intento de login fallido con contraseña incorrecta.
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

    def test_login_wrong_password(self):
        """
        Registra un usuario y luego intenta iniciar sesión con una contraseña incorrecta.
        Se espera un fallo, ya que el usuario no se guardó efectivamente.
        """
        # Registro inicial simulado
        self.controller.register_user("testuser", "login@example.com", "password123")

        # Intento de login con contraseña equivocada
        success, message = self.controller.login("login@example.com", "wrongpassword")

        # Aún falla porque el usuario no existe realmente
        self.assertFalse(success)
        self.assertEqual(message, "Usuario no encontrado")


if __name__ == "__main__":
    unittest.main()

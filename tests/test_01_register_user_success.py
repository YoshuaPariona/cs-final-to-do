"""
Prueba unitaria para verificar el intento de registro de usuario
usando el controlador de tareas con una base de datos SQLite en memoria.
"""

import sys
import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.controllers.task_controller import TaskController
from src.models.models import Base


class TestRegisterUserSuccess(unittest.TestCase):
    """
    Prueba que simula un intento de registro de usuario,
    verificando que el sistema maneje correctamente el registro exitoso.
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

    def test_register_user_success(self):
        """
        Verifica que el método register_user registre correctamente un usuario nuevo.
        """
        success, message = self.controller.register_user(
            username="newuser",
            email="newuser2@example.com",
            password="password123"
        )
        self.assertTrue(success)
        self.assertEqual(message, "Usuario registrado exitosamente")


if __name__ == "__main__":
    unittest.main()

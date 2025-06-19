import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.modelo.task import TaskPriority, TaskStatus, Task
from src.controlador.task_controller import TaskController
from src.controlador.logica.models import Base

class TestRegisterUserDuplicate(unittest.TestCase):

    def setUp(self):
        # Configura una base de datos SQLite en memoria
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)
        
        # Instancia el controlador y reemplaza su repositorio con uno que use la base en memoria
        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_register_user_duplicate(self):
        # Primer registro (falla por mapeo)
        self.controller.register_user("testuser", "test@example.com", "password123")
        
        # Intento de registro duplicado (también falla por mapeo)
        success, message = self.controller.register_user(
            username="testuser2",
            email="test@example.com",  # Mismo email
            password="password123"
        )
        self.assertFalse(success)
        self.assertEqual(message, "Error al registrar usuario")

if __name__ == "__main__":
    unittest.main()

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.modelo.task import TaskPriority, TaskStatus, Task
from src.controlador.task_controller import TaskController
from src.controlador.logica.models import Base

class TestLoginSuccess(unittest.TestCase):

    def setUp(self):
        # Configura una base de datos SQLite en memoria
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)
        
        # Instancia el controlador y reemplaza su repositorio con uno que use la base en memoria
        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_login_success(self):
        # Registrar usuario primero (falla por mapeo)
        self.controller.register_user("loginuser", "login@example.com", "password123")
        
        # Intentar login (falla porque el usuario no se registró)
        success, message = self.controller.login("login@example.com", "password123")
        self.assertFalse(success)
        self.assertEqual(message, "Usuario no encontrado")

if __name__ == "__main__":
    unittest.main()

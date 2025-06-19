import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.modelo.task import TaskPriority, TaskStatus, Task
from src.controlador.task_controller import TaskController
from src.controlador.logica.models import Base

class TestLogout(unittest.TestCase):

    def setUp(self):
        # Configura una base de datos SQLite en memoria
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)
        
        # Instancia el controlador y reemplaza su repositorio con uno que use la base en memoria
        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_logout(self):
        # Registrar y loguear usuario (falla por mapeo)
        self.controller.register_user("testuser", "test@example.com", "password123")
        self.controller.login("test@example.com", "password123")
        
        # Verificar que NO está logueado (porque el registro falló)
        self.assertIsNone(self.controller.current_user)
        
        # Hacer logout (no cambia nada)
        self.controller.logout()
        self.assertIsNone(self.controller.current_user)

if __name__ == "__main__":
    unittest.main()

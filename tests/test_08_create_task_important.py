import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from src.modelo.task import TaskPriority, TaskStatus, Task
from src.controlador.task_controller import TaskController
from src.controlador.logica.models import Base

class TestCreateTaskImportant(unittest.TestCase):

    def setUp(self):
        # Configura una base de datos SQLite en memoria
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)
        
        # Instancia el controlador y reemplaza su repositorio con uno que use la base en memoria
        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_create_task_important(self):
        success, message = self.controller.create_task(
            name="Tarea importante",
            description="Tarea con prioridad importante",
            start_date=datetime(2026, 12, 29),
            end_date=datetime(2026, 12, 30),
            priority=TaskPriority.IMPORTANT.value
        )
        # Falla porque no hay usuario autenticado
        self.assertFalse(success)
        self.assertEqual(message, "Usuario no autenticado")

if __name__ == "__main__":
    unittest.main()

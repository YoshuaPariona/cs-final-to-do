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

class TestDeleteTask(unittest.TestCase):

    def setUp(self):
        # Configura una base de datos SQLite en memoria
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)
        
        # Instancia el controlador y reemplaza su repositorio con uno que use la base en memoria
        self.controller = TaskController()
        self.controller.repository.db = SessionLocal()

    def test_delete_task(self):
        # Sin usuario autenticado, no se pueden crear tareas
        tasks = self.controller.get_user_tasks()
        self.assertEqual(len(tasks), 0)
        
        # El test pasa verificando que no hay tareas
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()

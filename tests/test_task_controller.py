import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.modelo.task import TaskPriority, TaskStatus, Task
from src.controlador.task_controller import TaskController
from src.controlador.database.db import Base


class TestTaskController(unittest.TestCase):

    def setUp(self):
        # Configura una base de datos SQLite en memoria
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Instancia el controlador y reemplaza su repositorio con uno que use la base en memoria
        self.controller = TaskController()
        self.controller.repository.engine = self.engine
        self.controller.repository.Session = Session

        # Registra y loguea un usuario de prueba
        self.controller.register_user("testuser", "test@example.com", "1234")
        self.controller.login("testuser", "1234")

    def test_create_task(self):
        success, message = self.controller.create_task(
            title="Tarea de prueba",
            description="Probando crear",
            due_date="2025-12-31",
            priority=TaskPriority.HIGH
        )
        self.assertTrue(success)
        self.assertIn("creada", message.lower())

    def test_read_tasks(self):
        self.test_create_task()
        tasks = self.controller.get_user_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Tarea de prueba")

    def test_update_task(self):
        self.test_create_task()
        task = self.controller.get_user_tasks()[0]
        success, message = self.controller.update_task(
            task_id=task.id,
            title="Actualizada",
            description=None,
            due_date=None,
            priority=None,
            status=TaskStatus.IN_PROGRESS
        )
        self.assertTrue(success)
        updated_task = self.controller.get_user_tasks()[0]
        self.assertEqual(updated_task.title, "Actualizada")
        self.assertEqual(updated_task.status, TaskStatus.IN_PROGRESS)

    def test_delete_task(self):
        self.test_create_task()
        task = self.controller.get_user_tasks()[0]
        success, message = self.controller.delete_task(task.id)
        self.assertTrue(success)
        self.assertEqual(len(self.controller.get_user_tasks()), 0)

if __name__ == "__main__":
    unittest.main()

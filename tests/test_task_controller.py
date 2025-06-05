import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

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

    def test_register_user_success(self):
        success, message = self.controller.register_user(
            username="newuser",
            email="newuser@example.com",
            password="password123"
        )
        self.assertTrue(success)
        self.assertIn("exitosamente", message.lower())

    def test_register_user_duplicate(self):
        # Primer registro (exitoso)
        self.controller.register_user("testuser", "test@example.com", "password123")
        
        # Intento de registro duplicado
        success, message = self.controller.register_user(
            username="testuser",
            email="another@example.com",
            password="password123"
        )
        self.assertFalse(success)
        self.assertIn("ya está en uso", message.lower())

    def test_login_success(self):
        # Registrar usuario primero
        self.controller.register_user("loginuser", "login@example.com", "password123")
        
        # Intentar login
        success, message = self.controller.login("loginuser", "password123")
        self.assertTrue(success)
        self.assertIn("exitoso", message.lower())
        self.assertEqual(self.controller.current_user, "loginuser")

    def test_login_wrong_password(self):
        # Registrar usuario primero
        self.controller.register_user("loginuser", "login@example.com", "password123")
        
        # Intentar login con contraseña incorrecta
        success, message = self.controller.login("loginuser", "wrongpassword")
        self.assertFalse(success)
        self.assertIn("incorrecta", message.lower())
        self.assertIsNone(self.controller.current_user)

    def test_login_nonexistent_user(self):
        success, message = self.controller.login("nonexistent", "password123")
        self.assertFalse(success)
        self.assertIn("no encontrado", message.lower())
        self.assertIsNone(self.controller.current_user)

    def test_logout(self):
        # Registrar y loguear usuario
        self.controller.register_user("testuser", "test@example.com", "password123")
        self.controller.login("testuser", "password123")
        
        # Verificar que está logueado
        self.assertEqual(self.controller.current_user, "testuser")
        
        # Hacer logout
        self.controller.logout()
        self.assertIsNone(self.controller.current_user)

    def test_cleanup_completed_tasks(self):
        # Registrar y loguear usuario
        self.controller.register_user("testuser", "test@example.com", "password123")
        self.controller.login("testuser", "password123")
        
        # Crear algunas tareas
        self.controller.create_task(
            name="Tarea Completada 1",
            description="Esta tarea está completada",
            start_date=datetime.now() - timedelta(days=10),
            end_date=datetime.now() - timedelta(days=5),
            priority=TaskPriority.NORMAL.value
        )
        
        self.controller.create_task(
            name="Tarea Pendiente",
            description="Esta tarea está pendiente",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=5),
            priority=TaskPriority.NORMAL.value
        )
        
        # Completar la primera tarea
        tasks = self.controller.get_user_tasks()
        self.controller.complete_task(tasks[0].id)
        
        # Verificar que hay 2 tareas antes de la limpieza
        self.assertEqual(len(self.controller.get_user_tasks()), 2)
        
        # Ejecutar limpieza
        self.controller.cleanup_completed_tasks()
        
        # Verificar que solo queda la tarea pendiente
        remaining_tasks = self.controller.get_user_tasks()
        self.assertEqual(len(remaining_tasks), 1)
        self.assertEqual(remaining_tasks[0].name, "Tarea Pendiente")

    def test_create_task_important(self):
        success, message = self.controller.create_task(
            name="Tarea importante",
            description="Tarea con prioridad importante",
            start_date=datetime(2026, 12, 29),
            end_date=datetime(2026, 12, 30),
            priority=TaskPriority.IMPORTANT.value
        )
        self.assertTrue(success)
        self.assertIn("creada", message.lower())
        
        tasks = self.controller.get_user_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].priority, TaskPriority.IMPORTANT)

    def test_create_task_normal(self):
        success, message = self.controller.create_task(
            name="Tarea normal",
            description="Tarea con prioridad normal",
            start_date=datetime(2026, 12, 29),
            end_date=datetime(2026, 12, 30),
            priority=TaskPriority.NORMAL.value
        )
        self.assertTrue(success)
        self.assertIn("creada", message.lower())
        
        tasks = self.controller.get_user_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].priority, TaskPriority.NORMAL)

    def test_create_task_postponable(self):
        success, message = self.controller.create_task(
            name="Tarea postponible",
            description="Tarea con prioridad postponible",
            start_date=datetime(2026, 12, 29),
            end_date=datetime(2026, 12, 30),
            priority=TaskPriority.POSTPONABLE.value
        )
        self.assertTrue(success)
        self.assertIn("creada", message.lower())
        
        tasks = self.controller.get_user_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].priority, TaskPriority.POSTPONABLE)

    def test_read_tasks(self):
        # Create tasks with different priorities
        priorities = [
            TaskPriority.IMPORTANT.value,
            TaskPriority.NORMAL.value,
            TaskPriority.POSTPONABLE.value
        ]
        
        for i, priority in enumerate(priorities):
            self.controller.create_task(
                name=f"Tarea {i+1}",
                description=f"Tarea con prioridad {priority}",
                start_date=datetime(2026, 12, 29),
                end_date=datetime(2026, 12, 30),
                priority=priority
            )
        
        tasks = self.controller.get_user_tasks()
        self.assertEqual(len(tasks), 3)
        self.assertEqual(set(task.priority.value for task in tasks), 
                        set(priorities))

    def test_update_task(self):
        # Create a task first
        self.controller.create_task(
            name="Tarea original",
            description="Descripción original",
            start_date=datetime(2026, 12, 29),
            end_date=datetime(2026, 12, 30),
            priority=TaskPriority.NORMAL.value
        )
        
        task = self.controller.get_user_tasks()[0]
        success, message = self.controller.update_task(
            task_id=task.id,
            name="Tarea actualizada",
            description="Nueva descripción",
            start_date=datetime(2026, 12, 29),
            end_date=datetime(2026, 12, 30),
            priority=TaskPriority.IMPORTANT.value
        )
        
        self.assertTrue(success)
        updated_task = self.controller.get_user_tasks()[0]
        self.assertEqual(updated_task.name, "Tarea actualizada")
        self.assertEqual(updated_task.priority, TaskPriority.IMPORTANT)

    def test_delete_task(self):
        # Create and then delete a task
        self.controller.create_task(
            name="Tarea para eliminar",
            description="Esta tarea será eliminada",
            start_date=datetime(2026, 12, 29),
            end_date=datetime(2026, 12, 30),
            priority=TaskPriority.NORMAL.value
        )
        
        task = self.controller.get_user_tasks()[0]
        success, message = self.controller.delete_task(task.id)
        self.assertTrue(success)
        self.assertEqual(len(self.controller.get_user_tasks()), 0)

if __name__ == "__main__":
    unittest.main()

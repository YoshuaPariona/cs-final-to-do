import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional
from pathlib import Path

from src.modelo.user import User
from src.modelo.task import Task, TaskStatus

class Repository:
    """Clase para manejar la persistencia de datos usando SQLite"""

    def __init__(self, db_path: str = "./todo_app.db"):
        self.db_path = db_path
        self.init_database()
 
    def save_user(self, user: User) -> bool:
        """Guardar o actualizar usuario en la base de datos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO users 
                    (username, email, password, created_at, remember_me, last_login)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user.username,
                    user.email,
                    user.password,
                    user.created_at.isoformat(),
                    1 if user.remember_me else 0,
                    user.last_login.isoformat() if user.last_login else None
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error guardando usuario: {e}")
            return False

    def get_user(self, username: str) -> Optional[User]:
        """Obtener usuario por nombre de usuario"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                row = cursor.fetchone()
                
                if row:
                    return User(
                        username=row[0],
                        email=row[1],
                        password=row[2],
                        created_at=datetime.fromisoformat(row[3]),
                        remember_me=bool(row[4]),
                        last_login=datetime.fromisoformat(row[5]) if row[5] else None
                    )
                return None
        except Exception as e:
            print(f"Error obteniendo usuario: {e}")
            return None

    def save_task(self, task: Task) -> bool:
        """Guardar o actualizar tarea en la base de datos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if task.task_id is None:
                    # Nueva tarea
                    cursor.execute("""
                        INSERT INTO tasks 
                        (name, description, start_date, end_date, priority, status,
                         created_at, completed_at, user_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        task.name,
                        task.description,
                        task.start_date.isoformat(),
                        task.end_date.isoformat(),
                        task.priority.value,
                        task.status.value,
                        task.created_at.isoformat(),
                        task.completed_at.isoformat() if task.completed_at else None,
                        task.user_id
                    ))
                    task.task_id = cursor.lastrowid
                else:
                    # Actualizar tarea existente
                    cursor.execute("""
                        UPDATE tasks SET
                        name = ?, description = ?, start_date = ?, end_date = ?,
                        priority = ?, status = ?, completed_at = ?
                        WHERE task_id = ? AND user_id = ?
                    """, (
                        task.name,
                        task.description,
                        task.start_date.isoformat(),
                        task.end_date.isoformat(),
                        task.priority.value,
                        task.status.value,
                        task.completed_at.isoformat() if task.completed_at else None,
                        task.task_id,
                        task.user_id
                    ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error guardando tarea: {e}")
            return False

    def get_user_tasks(self, username: str) -> List[Task]:
        """Obtener todas las tareas de un usuario"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (username,))
                rows = cursor.fetchall()
                
                tasks = []
                for row in rows:
                    task = Task(
                        task_id=row[0],
                        name=row[1],
                        description=row[2],
                        start_date=datetime.fromisoformat(row[3]),
                        end_date=datetime.fromisoformat(row[4]),
                        priority=row[5],
                        status=TaskStatus(row[6]),
                        created_at=datetime.fromisoformat(row[7]),
                        completed_at=datetime.fromisoformat(row[8]) if row[8] else None,
                        user_id=row[9]
                    )
                    tasks.append(task)
                return tasks
        except Exception as e:
            print(f"Error obteniendo tareas: {e}")
            return []

    def delete_task(self, task_id: int, user_id: str) -> bool:
        """Eliminar una tarea"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM tasks WHERE task_id = ? AND user_id = ?",
                    (task_id, user_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error eliminando tarea: {e}")
            return False

    def cleanup_completed_tasks(self):
        """Eliminar tareas completadas hace más de 5 días"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                five_days_ago = (datetime.now() - timedelta(days=5)).isoformat()
                
                cursor.execute("""
                    DELETE FROM tasks 
                    WHERE status = ? AND completed_at < ?
                """, (TaskStatus.COMPLETED.value, five_days_ago))
                
                conn.commit()
        except Exception as e:
            print(f"Error limpiando tareas completadas: {e}")

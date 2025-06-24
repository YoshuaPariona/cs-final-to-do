import os
import webview
from datetime import datetime
from src.controllers.task_controller import TaskController as TC

class Api:
    def __init__(self):
        self.controller = TC()
        # Seed de usuarios iniciales
        self.controller.repository.seed_initial_users()

    def get_item(self, action: str, data: dict) -> dict:
        if action == 'get_user':
            username_or_email = data.get('email')
            password = data.get('password')
            success, message, *info = self.controller.login(username_or_email, password)
            return {
                "success": success,
                "message": message,
                "user": info[0] if info else None
            }
        elif action == 'get_tasks':
            tasks = self.controller.get_user_tasks()
            return {
                "success": True,
                "tasks": [self._task_to_dict(t) for t in tasks]
            }
        elif action == 'get_task':
            task_id = int(data.get('task_id'))
            task = self.controller.get_task_by_id(task_id)
            if not task:
                return {"success": False, "message": "Tarea no encontrada"}
            task_dict = self._task_to_dict(task)
            return {
                "success": True,
                "task": task_dict,
                "status": task_dict.get('status')
            }
        elif action == 'get_events':
            events = self.controller.get_user_events()
            return {
                "success": True,
                "events": [self._event_to_dict(e) for e in events]
            }
        return {"success": False, "message": "Acción desconocida"}

    def add_item(self, action: str, data: dict) -> dict:
        if action == 'create_user':
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            success, message = self.controller.register_user(name, email, password)
            return {"success": success, "message": message}
        elif action == 'create_task':
            # Convertir fechas y enums
            try:
                start_date = datetime.fromisoformat(data.get('start_date'))
                end_date = datetime.fromisoformat(data.get('end_date'))
                priority = data.get('priority')
                success, message = self.controller.create_task(
                    name=data.get('name'),
                    description=data.get('description'),
                    start_date=start_date,
                    end_date=end_date,
                    priority=priority
                )
                tasks = self.controller.get_user_tasks()
                created_task = None
                if tasks:
                    created_task = max(tasks, key=lambda t: getattr(t, 'task_id', getattr(t, 'idTarea', 0)))
                created_status = self._task_to_dict(created_task).get('status') if created_task else None
                return {"success": success, "message": message, "tasks": [self._task_to_dict(t) for t in tasks], "created_status": created_status}
            except Exception as e:
                return {"success": False, "message": str(e)}
        elif action == 'create_event':
            success, message = self.controller.create_event(
                title=data.get('title'),
                description=data.get('description'),
                date=data.get('date'),
                time=data.get('time'),
                priority=data.get('priority')
            )
            events = self.controller.get_user_events()
            return {"success": success, "message": message, "events": [self._event_to_dict(e) for e in events]}
        return {"success": False, "message": "Acción desconocida"}

    def update_item(self, action: str, data: dict) -> dict:
        if action == 'update_task':
            try:
                task_id = int(data.get('task_id'))
                start_date = datetime.fromisoformat(data.get('start_date'))
                end_date = datetime.fromisoformat(data.get('end_date'))
                priority = data.get('priority')
                success, message = self.controller.update_task(
                    task_id=task_id,
                    name=data.get('name'),
                    description=data.get('description'),
                    start_date=start_date,
                    end_date=end_date,
                    priority=priority,
                    estado=data.set('status')
                )
                tasks = self.controller.get_user_tasks()
                updated_task = next((t for t in tasks if getattr(t, 'task_id', getattr(t, 'idTarea', None)) == task_id), None)
                updated_status = None
                if updated_task:
                    updated_status = self._task_to_dict(updated_task).get('status')
                return {"success": success, "message": message, "tasks": [self._task_to_dict(t) for t in tasks], "updated_status": updated_status}
            except Exception as e:
                return {"success": False, "message": str(e)}
        return {"success": False, "message": "Acción desconocida"}

    def remove_item(self, action: str, data: dict) -> dict:
        if action == 'delete_task':
            try:
                task_id = int(data.get('task_id'))
                success, message = self.controller.delete_task(task_id)
                tasks = self.controller.get_user_tasks()
                return {"success": success, "message": message, "tasks": [self._task_to_dict(t) for t in tasks]}
            except Exception as e:
                return {"success": False, "message": str(e)}
        elif action == 'delete_event':
            event_id = int(data.get('event_id'))
            success, message = self.controller.delete_event(event_id)
            events = self.controller.get_user_events()
            return {"success": success, "message": message, "events": [self._event_to_dict(e) for e in events]}
        return {"success": False, "message": "Acción desconocida"}

    def toggle_item(self, action: str, data: dict) -> dict:
        if action == 'complete_task':
            try:
                task_id = int(data.get('task_id'))
                success, message = self.controller.complete_task(task_id)
                tasks = self.controller.get_user_tasks()
                return {"success": success, "message": message, "tasks": [self._task_to_dict(t) for t in tasks]}
            except Exception as e:
                return {"success": False, "message": str(e)}
        return {"success": False, "message": "Acción desconocida"}

    def _task_to_dict(self, t):
        def iso(val):
            if isinstance(val, datetime):
                return val.isoformat()
            return val
        # Mapeo de estado backend -> frontend
        raw_status = getattr(t, 'status', getattr(t, 'estado', None))
        status_map = {
            'todo': 'new',
            'pending': 'progress',
            'completed': 'completed',
            'new': 'new',
            'progress': 'progress',
            'complete': 'completed',
        }
        status = status_map.get(str(raw_status).lower(), str(raw_status).lower())
        return {
            "id": getattr(t, 'task_id', getattr(t, 'idTarea', None)),
            "name": getattr(t, 'name', getattr(t, 'titulo', None)),
            "description": getattr(t, 'description', getattr(t, 'descripcion', None)),
            "priority": getattr(t, 'priority', getattr(t, 'prioridad', None)),
            "status": status,
            "start_date": iso(getattr(t, 'start_date', getattr(t, 'fechaCreacion', None))),
            "end_date": iso(getattr(t, 'end_date', getattr(t, 'fechaVencimiento', None))),
            "created_at": iso(getattr(t, 'created_at', getattr(t, 'fechaCreacion', None))),
            "completed_at": iso(getattr(t, 'completed_at', None)),
        }

    def _event_to_dict(self, e):
        return {
            "id": getattr(e, 'idEvento', None),
            "title": getattr(e, 'titulo', None),
            "description": getattr(e, 'descripcion', None),
            "date": getattr(e, 'fecha', None),
            "time": getattr(e, 'hora', None),
            "priority": getattr(e, 'prioridad', None),
        }

    def toggle_fullscreen(self) -> None:
        webview.windows[0].toggle_fullscreen()


def load_interface() -> None:
    api = Api()
    webview.create_window(
        'TODO APP',
        './src/views/static/index.html',
        js_api=api,
        min_size=(1280, 720)
    )
    webview.start(debug=True, gui='qt')

# if __name__ == '__main__':
#     load_interface()

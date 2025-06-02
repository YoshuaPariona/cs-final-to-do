import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import calendar
import threading
import time

# Configuración global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TaskManager:
    """Gestor de datos para tareas y usuarios"""
    
    def __init__(self):
        self.users_file = "users.json"
        self.tasks_file = "tasks.json"
        self.current_user = None
        
        # Cargar datos existentes
        self.users = self.load_users()
        self.tasks = self.load_tasks()
        
        # Iniciar limpieza automática de tareas completadas
        self.start_cleanup_thread()
    
    def load_users(self) -> Dict:
        """Cargar usuarios desde archivo"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
        return {}
    
    def save_users(self):
        """Guardar usuarios en archivo"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando usuarios: {e}")
    
    def load_tasks(self) -> Dict:
        """Cargar tareas desde archivo"""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error cargando tareas: {e}")
        return {}
    
    def save_tasks(self):
        """Guardar tareas en archivo"""
        try:
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando tareas: {e}")
    
    def register_user(self, username: str, email: str, password: str) -> bool:
        """Registrar nuevo usuario"""
        if username in self.users:
            return False
        
        self.users[username] = {
            "email": email,
            "password": password,  # En producción, usar hash
            "created_at": datetime.now().isoformat()
        }
        self.save_users()
        return True
    
    def login_user(self, username: str, password: str) -> bool:
        """Autenticar usuario"""
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            if username not in self.tasks:
                self.tasks[username] = []
            return True
        return False
    
    def get_user_tasks(self) -> List[Dict]:
        """Obtener tareas del usuario actual"""
        if self.current_user:
            return self.tasks.get(self.current_user, [])
        return []
    
    def add_task(self, task_data: Dict):
        """Agregar nueva tarea"""
        if self.current_user:
            task_data["id"] = len(self.get_user_tasks()) + 1
            task_data["created_at"] = datetime.now().isoformat()
            task_data["status"] = "todo"
            self.tasks[self.current_user].append(task_data)
            self.save_tasks()
    
    def update_task(self, task_id: int, task_data: Dict):
        """Actualizar tarea existente"""
        if self.current_user:
            for i, task in enumerate(self.tasks[self.current_user]):
                if task["id"] == task_id:
                    task_data["id"] = task_id
                    task_data["created_at"] = task.get("created_at", datetime.now().isoformat())
                    task_data["updated_at"] = datetime.now().isoformat()
                    self.tasks[self.current_user][i] = task_data
                    self.save_tasks()
                    break
    
    def delete_task(self, task_id: int):
        """Eliminar tarea"""
        if self.current_user:
            self.tasks[self.current_user] = [
                task for task in self.tasks[self.current_user] 
                if task["id"] != task_id
            ]
            self.save_tasks()
    
    def complete_task(self, task_id: int):
        """Marcar tarea como completada"""
        if self.current_user:
            for task in self.tasks[self.current_user]:
                if task["id"] == task_id:
                    task["status"] = "completed"
                    task["completed_at"] = datetime.now().isoformat()
                    self.save_tasks()
                    break
    
    def start_cleanup_thread(self):
        """Iniciar hilo para limpieza automática de tareas completadas"""
        def cleanup():
            while True:
                time.sleep(86400)  # Revisar cada 24 horas
                self.cleanup_completed_tasks()
        
        thread = threading.Thread(target=cleanup, daemon=True)
        thread.start()
    
    def cleanup_completed_tasks(self):
        """Eliminar tareas completadas después de 5 días"""
        if not self.current_user:
            return
            
        current_time = datetime.now()
        updated_tasks = []
        
        for task in self.tasks[self.current_user]:
            if task.get("status") == "completed":
                completed_at = datetime.fromisoformat(task.get("completed_at", ""))
                if (current_time - completed_at).days < 5:
                    updated_tasks.append(task)
            else:
                updated_tasks.append(task)
        
        self.tasks[self.current_user] = updated_tasks
        self.save_tasks()


class TaskManagementApp:
    """Aplicación principal de gestión de tareas"""
    
    def __init__(self):
        # Inicializar gestor de datos
        self.data_manager = TaskManager()
        
        # Configurar ventana principal
        self.root = ctk.CTk()
        self.root.title("Task Management System")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Variables de estado
        self.current_frame = None
        self.remember_me = False
        self.selected_start_date = None
        self.selected_end_date = None
        self.editing_task_id = None
        
        # Colores para prioridades
        self.priority_colors = {
            "Important": "#FF4444",    # Rojo
            "Normal": "#44AA44",       # Verde
            "Postponable": "#4444FF"   # Azul
        }
        
        # Iniciar con página de login
        self.show_login_page()
    
    def clear_frame(self):
        """Limpiar frame actual"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_login_page(self):
        """Mostrar página de login (Página 1)"""
        self.clear_frame()
        
        # Frame principal centrado
        self.current_frame = ctk.CTkFrame(self.root)
        self.current_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Título
        title_label = ctk.CTkLabel(
            self.current_frame,
            text="🔐 Task Manager - Login",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(50, 30))
        
        # Formulario de login
        form_frame = ctk.CTkFrame(self.current_frame)
        form_frame.pack(pady=20, padx=100, fill="x")
        
        # Campo username
        ctk.CTkLabel(form_frame, text="Username:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        self.login_username = ctk.CTkEntry(form_frame, placeholder_text="Enter username", height=40)
        self.login_username.pack(pady=(0, 15), padx=20, fill="x")
        
        # Campo password
        ctk.CTkLabel(form_frame, text="Password:", font=ctk.CTkFont(size=14)).pack(pady=(0, 5))
        self.login_password = ctk.CTkEntry(form_frame, placeholder_text="Enter password", show="*", height=40)
        self.login_password.pack(pady=(0, 15), padx=20, fill="x")
        
        # Remember Me checkbox
        self.remember_checkbox = ctk.CTkCheckBox(form_frame, text="Remember Me")
        self.remember_checkbox.pack(pady=10)
        
        # Botones
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(pady=20, padx=20, fill="x")
        
        login_btn = ctk.CTkButton(
            button_frame, text="🔑 Login", command=self.handle_login,
            height=45, font=ctk.CTkFont(size=16, weight="bold")
        )
        login_btn.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        register_btn = ctk.CTkButton(
            button_frame, text="📝 Register", command=self.show_register_page,
            height=45, font=ctk.CTkFont(size=16, weight="bold"), fg_color="gray"
        )
        register_btn.pack(side="right", padx=(10, 0), fill="x", expand=True)
        
        # Forgot Password link
        forgot_btn = ctk.CTkButton(
            form_frame, text="Forgot Password?", command=self.show_forgot_password,
            fg_color="transparent", text_color="gray", hover_color="darkgray"
        )
        forgot_btn.pack(pady=10)
        
        # Bind Enter key
        self.login_password.bind("<Return>", lambda e: self.handle_login())
    
    def show_register_page(self):
        """Mostrar página de registro (Página 2)"""
        self.clear_frame()
        
        # Frame principal centrado
        self.current_frame = ctk.CTkFrame(self.root)
        self.current_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Título
        title_label = ctk.CTkLabel(
            self.current_frame,
            text="📝 Create New Account",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(50, 30))
        
        # Formulario de registro
        form_frame = ctk.CTkFrame(self.current_frame)
        form_frame.pack(pady=20, padx=100, fill="x")
        
        # Campos del formulario
        fields = [
            ("Username:", "register_username", "Enter username"),
            ("Email:", "register_email", "Enter email address"),
            ("Password:", "register_password", "Enter password"),
            ("Confirm Password:", "register_confirm", "Confirm password")
        ]
        
        self.register_fields = {}
        for label_text, field_name, placeholder in fields:
            ctk.CTkLabel(form_frame, text=label_text, font=ctk.CTkFont(size=14)).pack(pady=(15, 5))
            
            if "password" in field_name:
                entry = ctk.CTkEntry(form_frame, placeholder_text=placeholder, show="*", height=40)
            else:
                entry = ctk.CTkEntry(form_frame, placeholder_text=placeholder, height=40)
            
            entry.pack(pady=(0, 10), padx=20, fill="x")
            self.register_fields[field_name] = entry
        
        # Remember Me checkbox
        remember_checkbox = ctk.CTkCheckBox(form_frame, text="Remember Me")
        remember_checkbox.pack(pady=10)
        
        # Botones
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(pady=20, padx=20, fill="x")
        
        register_btn = ctk.CTkButton(
            button_frame, text="✅ Register", command=self.handle_register,
            height=45, font=ctk.CTkFont(size=16, weight="bold")
        )
        register_btn.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        back_btn = ctk.CTkButton(
            button_frame, text="⬅️ Back to Login", command=self.show_login_page,
            height=45, font=ctk.CTkFont(size=16, weight="bold"), fg_color="gray"
        )
        back_btn.pack(side="right", padx=(10, 0), fill="x", expand=True)
        
        # Forgot Password link
        forgot_btn = ctk.CTkButton(
            form_frame, text="Forgot Password?", command=self.show_forgot_password,
            fg_color="transparent", text_color="gray", hover_color="darkgray"
        )
        forgot_btn.pack(pady=10)
    
    def show_dashboard(self):
        """Mostrar dashboard principal (Página 3)"""
        self.clear_frame()
        
        # Frame principal con sidebar
        self.current_frame = ctk.CTkFrame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sidebar
        sidebar = ctk.CTkFrame(self.current_frame, width=250)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Logo/Título del sidebar
        ctk.CTkLabel(
            sidebar, text="📋 Task Manager",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Usuario actual
        ctk.CTkLabel(
            sidebar, text=f"👤 {self.data_manager.current_user}",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 20))
        
        # Botones de navegación
        nav_buttons = [
            ("➕ Add Task", self.show_add_task_page),
            ("📋 View Tasks", self.show_view_tasks_page),
            ("📅 Calendar", self.show_calendar_page),
            ("⭐ Set Priority", self.show_priority_page),
            ("✏️ Edit Task", self.show_edit_tasks_page),
            ("🚪 Logout", self.handle_logout)
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                sidebar, text=text, command=command,
                height=45, font=ctk.CTkFont(size=14)
            )
            btn.pack(pady=5, padx=20, fill="x")
        
        # Área principal del dashboard
        main_area = ctk.CTkFrame(self.current_frame)
        main_area.pack(side="right", fill="both", expand=True)
        
        # Título del dashboard
        ctk.CTkLabel(
            main_area, text="📊 Task Overview",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # Estadísticas rápidas
        stats_frame = ctk.CTkFrame(main_area)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        tasks = self.data_manager.get_user_tasks()
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.get("status") == "completed"])
        pending_tasks = total_tasks - completed_tasks
        
        stats_text = f"📊 Total: {total_tasks} | ✅ Completed: {completed_tasks} | ⏳ Pending: {pending_tasks}"
        ctk.CTkLabel(stats_frame, text=stats_text, font=ctk.CTkFont(size=16)).pack(pady=15)
        
        # Vista de tareas agrupadas
        self.create_task_overview(main_area)
    
    def create_task_overview(self, parent):
        """Crear vista general de tareas agrupadas"""
        # Frame scrollable para tareas
        tasks_frame = ctk.CTkScrollableFrame(parent, label_text="📋 Recent Tasks")
        tasks_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        tasks = self.data_manager.get_user_tasks()
        
        # Agrupar tareas por estado
        development_tasks = [t for t in tasks if t.get("status") == "todo" and t.get("priority") == "Important"]
        pending_tasks = [t for t in tasks if t.get("status") == "todo" and t.get("priority") != "Important"]
        
        # Mostrar tareas de desarrollo
        if development_tasks:
            dev_label = ctk.CTkLabel(
                tasks_frame, text="🔴 Development (High Priority)",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            dev_label.pack(anchor="w", padx=10, pady=(10, 5))
            
            for task in development_tasks[:5]:  # Mostrar solo las primeras 5
                self.create_task_preview(tasks_frame, task)
        
        # Mostrar tareas pendientes
        if pending_tasks:
            pending_label = ctk.CTkLabel(
                tasks_frame, text="🟡 Pending Tasks",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            pending_label.pack(anchor="w", padx=10, pady=(20, 5))
            
            for task in pending_tasks[:5]:  # Mostrar solo las primeras 5
                self.create_task_preview(tasks_frame, task)
    
    def create_task_preview(self, parent, task):
        """Crear vista previa de una tarea"""
        task_frame = ctk.CTkFrame(parent)
        task_frame.pack(fill="x", padx=10, pady=5)
        
        # Indicador de prioridad
        priority_color = self.priority_colors.get(task.get("priority", "Normal"), "#44AA44")
        priority_indicator = ctk.CTkFrame(task_frame, width=5, fg_color=priority_color)
        priority_indicator.pack(side="left", fill="y", padx=(5, 10))
        
        # Contenido de la tarea
        content_frame = ctk.CTkFrame(task_frame)
        content_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Título
        title_label = ctk.CTkLabel(
            content_frame, text=task.get("name", "Untitled"),
            font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
        )
        title_label.pack(anchor="w", padx=10, pady=(5, 0))
        
        # Descripción (truncada)
        desc = task.get("description", "")
        if len(desc) > 50:
            desc = desc[:50] + "..."
        
        desc_label = ctk.CTkLabel(
            content_frame, text=desc,
            font=ctk.CTkFont(size=12), text_color="gray", anchor="w"
        )
        desc_label.pack(anchor="w", padx=10, pady=(0, 5))
    
    def show_add_task_page(self):
        """Mostrar página de agregar tarea (Página 4)"""
        self.clear_frame()
        
        # Frame principal
        self.current_frame = ctk.CTkFrame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header con botón de regreso
        header_frame = ctk.CTkFrame(self.current_frame)
        header_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        back_btn = ctk.CTkButton(
            header_frame, text="⬅️ Back", command=self.show_dashboard,
            width=100, height=35
        )
        back_btn.pack(side="left", pady=15)
        
        title_label = ctk.CTkLabel(
            header_frame, text="➕ Add New Task",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Formulario de tarea
        form_frame = ctk.CTkScrollableFrame(self.current_frame, label_text="Task Details")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos del formulario
        self.task_fields = {}
        
        # Nombre de la tarea
        ctk.CTkLabel(form_frame, text="Task Name:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        self.task_fields["name"] = ctk.CTkEntry(form_frame, placeholder_text="Enter task name", height=40)
        self.task_fields["name"].pack(fill="x", padx=20, pady=(0, 15))
        
        # Descripción
        ctk.CTkLabel(form_frame, text="Description:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(0, 5))
        self.task_fields["description"] = ctk.CTkTextbox(form_frame, height=100)
        self.task_fields["description"].pack(fill="x", padx=20, pady=(0, 15))
        
        # Fechas
        dates_frame = ctk.CTkFrame(form_frame)
        dates_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Fecha de inicio
        start_frame = ctk.CTkFrame(dates_frame)
        start_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(start_frame, text="Start Date:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        self.start_date_btn = ctk.CTkButton(
            start_frame, text="📅 Select Start Date",
            command=lambda: self.show_date_selector("start"),
            height=40
        )
        self.start_date_btn.pack(fill="x", padx=15, pady=(0, 15))
        
        # Fecha de fin
        end_frame = ctk.CTkFrame(dates_frame)
        end_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(end_frame, text="End Date:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        self.end_date_btn = ctk.CTkButton(
            end_frame, text="📅 Select End Date",
            command=lambda: self.show_date_selector("end"),
            height=40
        )
        self.end_date_btn.pack(fill="x", padx=15, pady=(0, 15))
        
        # Duración calculada
        self.duration_label = ctk.CTkLabel(
            form_frame, text="Duration: Not calculated",
            font=ctk.CTkFont(size=14), text_color="gray"
        )
        self.duration_label.pack(pady=10)
        
        # Prioridad
        ctk.CTkLabel(form_frame, text="Priority:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        self.task_fields["priority"] = ctk.CTkOptionMenu(
            form_frame, values=["Important", "Normal", "Postponable"],
            height=40
        )
        self.task_fields["priority"].pack(fill="x", padx=20, pady=(0, 20))
        
        # Botón de guardar
        save_btn = ctk.CTkButton(
            form_frame, text="💾 Save Task", command=self.save_new_task,
            height=50, font=ctk.CTkFont(size=16, weight="bold")
        )
        save_btn.pack(pady=20, padx=20, fill="x")
    
    def show_date_selector(self, date_type):
        """Mostrar selector de fecha (Página 5)"""
        # Crear ventana modal para selección de fecha
        date_window = ctk.CTkToplevel(self.root)
        date_window.title(f"Select {date_type.title()} Date")
        date_window.geometry("400x500")
        date_window.transient(self.root)
        date_window.grab_set()
        
        # Centrar la ventana
        date_window.update_idletasks()
        x = (date_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (date_window.winfo_screenheight() // 2) - (500 // 2)
        date_window.geometry(f"400x500+{x}+{y}")
        
        # Título
        ctk.CTkLabel(
            date_window, text=f"📅 Select {date_type.title()} Date",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Calendar widget simplificado
        cal_frame = ctk.CTkFrame(date_window)
        cal_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mes y año actual
        current_date = datetime.now()
        self.cal_month = current_date.month
        self.cal_year = current_date.year
        
        # Header del calendario
        header_frame = ctk.CTkFrame(cal_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        prev_btn = ctk.CTkButton(header_frame, text="◀", width=40, command=lambda: self.change_month(-1, cal_frame, date_window, date_type))
        prev_btn.pack(side="left")
        
        self.month_label = ctk.CTkLabel(
            header_frame, text=f"{calendar.month_name[self.cal_month]} {self.cal_year}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.month_label.pack(side="left", expand=True)
        
        next_btn = ctk.CTkButton(header_frame, text="▶", width=40, command=lambda: self.change_month(1, cal_frame, date_window, date_type))
        next_btn.pack(side="right")
        
        # Grid del calendario
        self.create_calendar_grid(cal_frame, date_window, date_type)
        
        # Botón de cancelar
        cancel_btn = ctk.CTkButton(
            date_window, text="Cancel", command=date_window.destroy,
            height=40, fg_color="gray"
        )
        cancel_btn.pack(pady=10)
    
    def change_month(self, delta, cal_frame, date_window, date_type):
        """Cambiar mes en el calendario"""
        self.cal_month += delta
        if self.cal_month > 12:
            self.cal_month = 1
            self.cal_year += 1
        elif self.cal_month < 1:
            self.cal_month = 12
            self.cal_year -= 1
        
        self.month_label.configure(text=f"{calendar.month_name[self.cal_month]} {self.cal_year}")
        
        # Recrear grid del calendario
        for widget in cal_frame.winfo_children():
            if widget != cal_frame.winfo_children()[0]:  # No destruir el header
                widget.destroy()
        
        self.create_calendar_grid(cal_frame, date_window, date_type)
    
    def create_calendar_grid(self, parent, date_window, date_type):
        """Crear grid del calendario"""
        # Días de la semana
        days_frame = ctk.CTkFrame(parent)
        days_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            ctk.CTkLabel(days_frame, text=day, width=50).pack(side="left", padx=2)
        
        # Grid de días
        cal = calendar.monthcalendar(self.cal_year, self.cal_month)
        
        for week in cal:
            week_frame = ctk.CTkFrame(parent)
            week_frame.pack(fill="x", padx=10, pady=2)
            
            for day in week:
                if day == 0:
                    # Día vacío
                    ctk.CTkLabel(week_frame, text="", width=50, height=35).pack(side="left", padx=2)
                else:
                    # Día del mes
                    day_btn = ctk.CTkButton(
                        week_frame, text=str(day), width=50, height=35,
                        command=lambda d=day: self.select_date(d, date_type, date_window)
                    )
                    day_btn.pack(side="left", padx=2)
    
    def select_date(self, day, date_type, date_window):
        """Seleccionar fecha específica"""
        selected_date
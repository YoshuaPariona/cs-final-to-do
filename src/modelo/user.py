"""
Este módulo define la clase User, que representa un usuario en el sistema.
La clase incluye métodos para validar datos de usuario y convertir usuarios a/desde diccionarios.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

@dataclass
class User:
    """
    Modelo de usuario con validación de datos.
    Representa un usuario con atributos como nombre de usuario, correo electrónico, contraseña, etc.
    """

    username: str
    email: str
    password: str  # En producción usar hash
    created_at: datetime = datetime.now()
    remember_me: bool = False
    last_login: Optional[datetime] = None
    dark_mode: bool = False  # Campo para el modo oscuro

    def __init__(self, username=None, email=None, password=None, nombre=None, contraseña=None, modoOscuro=False):
        """
        Inicializa una instancia de User.
        Soporta nombres de parámetros tanto en inglés como en español para compatibilidad.

        Parámetros:
        username (str): Nombre de usuario.
        email (str): Correo electrónico del usuario.
        password (str): Contraseña del usuario.
        nombre (str): Nombre de usuario en español.
        contraseña (str): Contraseña del usuario en español.
        modoOscuro (bool): Indica si el usuario prefiere el modo oscuro.
        """
        # Soporta nombres de parámetros tanto en inglés como en español
        self.username = username or nombre
        self.email = email
        self.password = password or contraseña
        self.dark_mode = modoOscuro

    def validate(self) -> Tuple[bool, str]:
        """
        Valida los datos del usuario.

        Retorna:
        Tuple[bool, str]: Una tupla que indica si el usuario es válido y un mensaje de error en caso contrario.
        """
        if not self.username or len(self.username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"

        if not self.email or '@' not in self.email:
            return False, "Email inválido"

        if not self.password or len(self.password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"

        return True, "Usuario válido"

    def to_dict(self) -> dict:
        """
        Convierte el usuario a un diccionario para almacenamiento.

        Retorna:
        dict: Un diccionario que representa al usuario.
        """
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at.isoformat(),
            "remember_me": self.remember_me,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "dark_mode": self.dark_mode  # Incluir el nuevo campo
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Crea un usuario desde un diccionario.

        Parámetros:
        data (dict): Un diccionario que contiene los datos del usuario.

        Retorna:
        User: Una instancia de User creada a partir del diccionario.
        """
        return cls(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            created_at=datetime.fromisoformat(data["created_at"]),
            remember_me=data.get("remember_me", False),
            last_login=datetime.fromisoformat(data["last_login"]) if data.get("last_login") else None,
            modoOscuro=data.get("dark_mode", False)  # Obtener el valor de modo oscuro
        )

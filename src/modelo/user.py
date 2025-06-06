from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

@dataclass
class User:
    """Modelo de usuario con validación de datos"""
    username: str
    email: str
    password: str  # En producción usar hash
    created_at: datetime = datetime.now()
    remember_me: bool = False
    last_login: Optional[datetime] = None
    dark_mode: bool = False  # Nuevo campo para el modo oscuro

    def __init__(self, username=None, email=None, password=None, nombre=None, contraseña=None, modoOscuro=False):
        # Support both English and Spanish parameter names
        self.username = username or nombre
        self.email = email
        self.password = password or contraseña
        self.dark_mode = modoOscuro
        
    def validate(self) -> Tuple[bool, str]:
        """Validar datos del usuario
        Returns:
            tuple[bool, str]: (es_valido, mensaje_error)
        """
        if not self.username or len(self.username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"
        
        if not self.email or '@' not in self.email:
            return False, "Email inválido"
            
        if not self.password or len(self.password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
            
        return True, "Usuario válido"

    def to_dict(self) -> dict:
        """Convertir usuario a diccionario para almacenamiento"""
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
        """Crear usuario desde diccionario"""
        return cls(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            created_at=datetime.fromisoformat(data["created_at"]),
            remember_me=data.get("remember_me", False),
            last_login=datetime.fromisoformat(data["last_login"]) if data.get("last_login") else None,
            modoOscuro=data.get("dark_mode", False)  # Obtener el valor de modo oscuro
        )
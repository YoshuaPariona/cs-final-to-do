from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Tuple


@dataclass
class User:
    """
    Modelo de datos para representar un usuario del sistema.

    Atributos:
        username (str): Nombre de usuario.
        email (str): Dirección de correo electrónico.
        password (str): Contraseña del usuario (en producción, usar hash).
        created_at (datetime): Fecha de creación del usuario.
        remember_me (bool): Indica si el usuario eligió recordar sesión.
        last_login (Optional[datetime]): Último inicio de sesión.
        dark_mode (bool): Preferencia de modo oscuro.
    """
    username: str = ""
    email: str = ""
    password: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    remember_me: bool = False
    last_login: Optional[datetime] = None
    dark_mode: bool = False

    def __init__(
        self,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        nombre: Optional[str] = None,
        contraseña: Optional[str] = None,
        modoOscuro: bool = False,
        created_at: Optional[datetime] = None,
        remember_me: bool = False,
        last_login: Optional[datetime] = None
    ):
        """
        Inicializa un usuario permitiendo parámetros en inglés o español.

        Args:
            username (str): Nombre de usuario.
            email (str): Correo electrónico.
            password (str): Contraseña.
            nombre (str): Alias para username.
            contraseña (str): Alias para password.
            modoOscuro (bool): Preferencia de modo oscuro.
            created_at (datetime): Fecha de creación.
            remember_me (bool): Recordar sesión.
            last_login (datetime): Último inicio de sesión.
        """
        self.username = username or nombre or ""
        self.email = email or ""
        self.password = password or contraseña or ""
        self.dark_mode = modoOscuro
        self.created_at = created_at or datetime.now()
        self.remember_me = remember_me
        self.last_login = last_login

    def validate(self) -> Tuple[bool, str]:
        """
        Valida los datos del usuario.

        Returns:
            tuple[bool, str]: Tupla con el resultado de la validación
                              y un mensaje asociado.
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
        Convierte el usuario a un diccionario serializable.

        Returns:
            dict: Representación en formato diccionario del usuario.
        """
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at.isoformat(),
            "remember_me": self.remember_me,
            "last_login": (
                self.last_login.isoformat() if self.last_login else None
            ),
            "dark_mode": self.dark_mode
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Crea una instancia de User desde un diccionario.

        Args:
            data (dict): Diccionario con datos del usuario.

        Returns:
            User: Instancia de usuario.
        """
        return cls(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            created_at=datetime.fromisoformat(data["created_at"]),
            remember_me=data.get("remember_me", False),
            last_login=datetime.fromisoformat(data["last_login"])
            if data.get("last_login") else None,
            modoOscuro=data.get("dark_mode", False)
        )

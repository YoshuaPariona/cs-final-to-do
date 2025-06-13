"""
Configura la conexión a una base de datos SQLite usando SQLAlchemy.
Proporciona herramientas para crear el motor de la base de datos, la sesión y la clase base para los modelos.
Incluye una función para inicializar la base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "sqlite:///todo_app.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(my_base):
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.

    Parámetros:
    my_base: La clase base de los modelos de SQLAlchemy que contiene los metadatos de las tablas.

    Lanza:
    SQLAlchemyError: Si ocurre un error durante la creación de las tablas
    en la base de datos.
    """
    try:
        my_base.metadata.create_all(bind=engine)
        print("Base de datos inicializada correctamente.")
    except SQLAlchemyError as e:
        print(f"Error al inicializar la base de datos: {e}")

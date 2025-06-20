from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "sqlite:///todo_app.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def init_db(my_base):
    """
    Inicializa la base de datos creando todas las tablas definidas en el modelo.

    Args:
        my_base: La base declarativa de SQLAlchemy que contiene los modelos.

    Prints:
        Mensaje de éxito o error al inicializar la base de datos.
    """
    try:
        my_base.metadata.create_all(bind=engine)
        print("Base de datos inicializada correctamente.")
    except SQLAlchemyError as e:
        print(f"Error al inicializar la base de datos: {e}")

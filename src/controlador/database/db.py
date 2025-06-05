from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "sqlite:///todo_app.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(my_base):
    try:
        my_base.metadata.create_all(bind=engine)
        print("Base de datos inicializada correctamente.")
    except SQLAlchemyError as e:
        print(f"Error al inicializar la base de datos: {e}")

import src.logica.handlers                  # Logic
from src.modelos import Base                # Tables model
from src.database.db import engine          # DB Connexion
from src.vista.ui import menu_principal     # UI

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)  # Inicializar DB

    menu_principal()

from src.database.db import init_db
from src.vista.ui import menu_principal

if __name__ == "__main__":
    init_db()
    menu_principal()
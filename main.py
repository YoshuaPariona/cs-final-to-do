from src.controlador.database.db import init_db
from src.vista.ui import load_interface

if __name__ == "__main__":
    init_db()
    load_interface()

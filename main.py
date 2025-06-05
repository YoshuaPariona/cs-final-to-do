from src.controlador.database.db import init_db
from src.controlador.logica.models import Base # Inicializar base de datos
from src.vista.ui_minimal import ui_minimal
# from src.vista.ui import menu_principal

if __name__ == "__main__":
    init_db(Base)
    ui_minimal()
    # menu_principal()
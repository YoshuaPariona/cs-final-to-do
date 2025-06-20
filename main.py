from src.database.db import init_db
from src.models.models import Base # Inicializar base de datos
# from view.console_ui import ui_console
from src.views.ui import load_interface

if __name__ == "__main__":
    init_db(Base)
    # ui_console()
    load_interface()
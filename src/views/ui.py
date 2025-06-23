import os
import webview
from src.controllers.task_controller import TaskController as tc

"""
Este archivo define una pequeña aplicación tipo TODO usando PyWebView,
que actúa como interfaz gráfica local sin necesidad de un servidor web.
Incluye una clase API con métodos que pueden ser llamados desde JavaScript.
"""

class Api:
    """
    Clase API que define los métodos expuestos a JavaScript
    desde la interfaz de usuario.
    """
    def __init__(self):
        self.controller = tc()

    def get_item(self, action: str, data: dict) -> dict:
        """
        Obtiene items.

        Args:
            title (str): Título del ítem.
        """
        if action == 'get_user' :
            email = data.get("email")
            password = data.get("password")
            success, message, *data = self.controller.login(email, password)

            if len(data) == 0:
                return {"success": success, "message": message}
            else:
                return {"success": success, "message": message, "data": data[0]}


    def add_item(self, action: str, data: dict) -> dict:
        """
        Agrega un nuevo ítem.

        Args:
            title (str): Título del ítem.
        """
        if action == 'create_user' :
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            success, message = self.controller.register_user(name, email, password)
            return {"success": success, "message": message}
        

    def remove_item(self, item: str) -> None:
        """
        Elimina un ítem existente.

        Args:
            item (str): Ítem a eliminar.
        """
        print(f'Removed item {item}')

    def edit_item(self, item: str) -> None:
        """
        Edita un ítem existente.

        Args:
            item (str): Ítem a editar.
        """
        print(f'Edited item {item}')

    def toggle_item(self, item: str) -> None:
        """
        Alterna el estado de un ítem (ej. completado/no completado).

        Args:
            item (str): Ítem a alternar.
        """
        print(f'Toggled item {item}')

    def toggle_fullscreen(self) -> None:
        """
        Alterna el modo pantalla completa de la ventana principal.
        """
        webview.windows[0].toggle_fullscreen()


def load_interface() -> None:
    """
    Carga la interfaz de usuario de la aplicación utilizando PyWebView.
    """
    api = Api()
    webview.create_window(
        'TODO APP',
        './src/views/static/index.html',
        js_api=api,
        min_size=(1280, 720)
    )
    webview.start(debug=True, gui='qt')


# if __name__ == '__main__':
#     load_interface()

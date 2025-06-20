import os
import webview

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

    def add_item(self, title: str) -> None:
        """
        Agrega un nuevo ítem.

        Args:
            title (str): Título del ítem.
        """
        print(f'Added item {title}')

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

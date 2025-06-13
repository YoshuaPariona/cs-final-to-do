"""
Este módulo proporciona una arquitectura de aplicación sin servidor utilizando webview.
Define una clase Api que actúa como interfaz entre la lógica de la aplicación y la interfaz de usuario.
"""
import os
import webview


class Api:
    """
    Clase que define la interfaz para interactuar con la aplicación a través de la interfaz de usuario.
    Proporciona métodos para añadir, eliminar, editar, alternar elementos y alternar el modo de pantalla completa.
    """

    def addItem(self, title):
        """
        Añade un elemento a la aplicación.

        Parámetros:
        title (str): El título del elemento a añadir.
        """
        print('Added item %s' % title)

    def removeItem(self, item):
        """
        Elimina un elemento de la aplicación.

        Parámetros:
        item (str): El elemento a eliminar.
        """
        print('Removed item %s' % item)

    def editItem(self, item):
        """
        Edita un elemento en la aplicación.

        Parámetros:
        item (str): El elemento a editar.
        """
        print('Edited item %s' % item)

    def toggleItem(self, item):
        """
        Alterna el estado de un elemento en la aplicación.

        Parámetros:
        item (str): El elemento cuyo estado se va a alternar.
        """
        print('Toggled item %s' % item)

    def toggleFullscreen(self):
        """
        Alterna el modo de pantalla completa de la ventana de la aplicación.
        """
        webview.windows[0].toggle_fullscreen()


# if __name__ == '__main__':
def load_interface():
    """
    Carga la interfaz de usuario de la aplicación.
    Crea una ventana webview con la interfaz de usuario y configura la API para interactuar con ella.
    """
    api = Api()
    webview.create_window('TODO APP', './src/vista/static/index.html', js_api=api, min_size=(1280, 720))
    webview.start(debug=True, gui='qt')

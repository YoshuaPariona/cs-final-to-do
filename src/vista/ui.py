import os
import webview

"""
An example of serverless app architecture
"""

class Api:
    def addItem(self, title):
        print('Added item %s' % title)

    def removeItem(self, item):
        print('Removed item %s' % item)

    def editItem(self, item):
        print('Edited item %s' % item)

    def toggleItem(self, item):
        print('Toggled item %s' % item)

    def toggleFullscreen(self):
        webview.windows[0].toggle_fullscreen()


# if __name__ == '__main__':
def load_interface():
    api = Api()
    webview.create_window('TODO APP', './src/vista/static/index.html', js_api=api, min_size=(1280, 720))
    webview.start()

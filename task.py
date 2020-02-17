import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.k = 0
        self.getImage(list(map(float, input().split())))
        self.initUI()

    def getImage(self, data):
        self.k += 1
        a, b, delta = data
        self.a = a
        self.b = b
        self.delta = delta
        self.delta = str(self.delta).split('.')[0]
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={a},{b}&z={self.delta}&l=map"
        self.delta = int(self.delta)
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        if self.k != 1:
            self.image.clear()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.delta -= 1
            if self.delta <= 0:
                self.delta = 1
            self.getImage([self.a, self.b, self.delta])
        if event.key() == Qt.Key_PageUp:
            self.delta += 1
            if self.delta >= 17:
                self.delta = 17
            self.getImage([self.a, self.b, self.delta])

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

import sys
import requests

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class MyWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('timeLimited.ui', self)
        self.move(0,0)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.dolgota = float(self.textEdit_3.toPlainText())
        self.shirota = float(self.textEdit_2.toPlainText())
        self.masch1 = float(self.textEdit_5.toPlainText())
        self.masch2 = float(self.textEdit_4.toPlainText())
        self.setImage()


    def setImage(self):

        self.ex = MapViewer(self.dolgota, self.shirota, self.masch1, self.masch2 )
        self.ex.show()

class MapViewer(QWidget):
    def __init__(self, dolgota, shirota, masch1, masch2):
        self.dolgota = dolgota
        self.shirota = shirota
        self.masch1 = masch1
        self.masch2 = masch2
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = f'https://static-maps.yandex.ru/1.x/?ll={self.dolgota},' \
                      f'{self.shirota}&spn={self.masch1},{self.masch2}&l=map'
        response = requests.get(map_request)
        print(map_request)
        if not response:
            sys.exit(1)


        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)



    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
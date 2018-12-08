import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('yandex.ui', self)
        self.initUi()

    def initUi(self):
        #Настройки для кнопки по яркости.
        self.bright.setCheckable(True)
        self.bright.clicked.connect(self.brightness)

    def brightness(self): #функция для изменения яркости изображения



app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PIL import Image
import numpy

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('yandex.ui', self)
        self.initUi()

    def initUi(self):
        # сброс настроек
        self.everything()

        # Настройки окон открытия и сохранения
        self.openbut.clicked.connect(self.openimage)
        self.savebut.clicked.connect(self.saveimage)

        # Настройки для кнопки по яркости.
        self.bright.clicked.connect(self.brightness)

        # Настройки для кнопки по контрастности
        self.contrast.clicked.connect(self.contrasting)

        self.path = ""
        self.pathsave = ""

    def openimage(self):
        # функция для того, чтобы открыть изображение
        # Показ изображения на экране пользователя
        try:
            self.path = str(self.boxopen.text())
            if self.path == "":
                raise FileNotFoundError
            else:
                self.kartinka.setPixmap(QtGui.QPixmap(self.path))

                self.boxopen.setText("")

                self.savebut.setEnabled(True)
                self.boxsave.setEnabled(True)
        except FileNotFoundError:
            self.kartinka.setText("Изображение не найдено!")

            self.boxopen.setText("")

    def saveimage(self):
        # функция для сохранения изображения
        self.pathsave = self.boxsave.text()
        source = Image.open(self.path)
        source = numpy.array(source)
        source = Image.fromarray(source)
        source.save(self.pathsave)

        self.everything()

    def brightness(self):
        # функция для изменения яркости изображения
        self.param1label.setText("Яркость...")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)

        self.everything23()

    def contrasting(self):
        # функция для изменения яркости изображения
        self.param1label.setText("Контрастность...")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)

        self.everything23()

    def everything23(self):
        # функция для отключения 2-го и 3-го ползунков
        self.param2label.setText("-")
        self.param2.setSliderPosition(0)
        self.param2.setEnabled(False)

        self.param3label.setText("-")
        self.param3.setSliderPosition(0)
        self.param3.setEnabled(False)

    def everything13(self):
        # функция для отключения 1-го и 3-го ползунков
        self.param1label.setText("-")
        self.param1.setSliderPosition(0)
        self.param1.setEnabled(False)

        self.param3label.setText("-")
        self.param3.setSliderPosition(0)
        self.param3.setEnabled(False)

    def everything21(self):
        # функция для отключения 2-го и 1-го ползунков
        self.param2label.setText("-")
        self.param2.setSliderPosition(0)
        self.param2.setEnabled(False)

        self.param1label.setText("-")
        self.param1.setSliderPosition(0)
        self.param1.setEnabled(False)

    def everything(self):
        # функция для полного сброса настроек
        self.param2label.setText("-")
        self.param2.setSliderPosition(0)
        self.param2.setEnabled(False)

        self.param3label.setText("-")
        self.param3.setSliderPosition(0)
        self.param3.setEnabled(False)

        self.param1label.setText("-")
        self.param1.setSliderPosition(0)
        self.param1.setEnabled(False)

        self.savebut.setEnabled(False)
        self.boxsave.setEnabled(False)

        self.openbut.setEnabled(True)
        self.boxopen.setEnabled(True)

        self.path = ""
        self.pathsave = ""

        self.boxopen.setText("")
        self.boxsave.setText("")

        self.kartinka.setPixmap(QtGui.QPixmap(self.path))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
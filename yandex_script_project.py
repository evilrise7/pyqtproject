import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PIL import Image, ImageEnhance
import numpy
import os


class MyWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('yandex.ui', self)
        self.initUi()

    def initUi(self):
        # для чернового листа
        self.flag = False
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
        if self.flag:
            source = Image.open("working_sheet.png")  # открываю
            source = numpy.array(source)  # для подстраховки
            source = Image.fromarray(source)  # для подстраховки
            source.save(self.pathsave)  # спаси-сохрани!
            os.remove("working_sheet.png")
        else:
            source = Image.open(self.path)  #открываю
            source = numpy.array(source)  # для подстраховки
            source = Image.fromarray(source)  # для подстраховки
            source.save(self.pathsave)  # спаси-сохрани!

        self.everything()

    def brightness(self):
        # функция для изменения яркости изображения
        self.param1label.setText("Яркость: 50%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)  # базовое значение яркости

        self.everything23()

        # когда ползунок дергается, то происходит вызов функции для изменения яркости
        self.param1.valueChanged.connect(self.brightnessediting)

    def brightnessediting(self):
        self.param1label.setText("Яркость: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Brightness(source)  # модуль изменения яркости
        source = enhancer.enhance(float(float(self.param1.value()) / 10))  # значение яркости
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True  # флаг, чтобы учесть при сохранении, были ли какие-либо изменения в файле.
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))  # отображение

    def contrasting(self):
        # функция для изменения контраста изображения
        self.param1label.setText("Контрастность: 50%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)  # базовое значение контраста

        self.everything23()
        # когда ползунок дергается, то происходит вызов функции для изменения контраста
        self.param1.valueChanged.connect(self.contrastingediting)

    def contrastingediting(self):
        self.param1label.setText("Контрастность: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Contrast(source)  # модуль изменения контраста
        source = enhancer.enhance(float(float(self.param1.value()) / 10))  # значение контраста
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True  # флаг, чтобы учесть при сохранении, были ли какие-либо изменения в файле.
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))  # отображение

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
        self.param2.setSliderPosition(0)
        self.param2.setEnabled(False)

        self.param3.setSliderPosition(0)
        self.param3.setEnabled(False)

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

        self.flag = False

        self.param1label.setText("-")
        self.param2label.setText("-")
        self.param3label.setText("-")


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
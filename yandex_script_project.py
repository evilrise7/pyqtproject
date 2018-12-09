import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PIL import Image, ImageEnhance, ImageFilter
import numpy
import os


class MyWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('yandex.ui', self)
        app.setStyleSheet('QMainWindow{background-color: #000000;}')
        self.initUi()

    def initUi(self):
        self.setWindowTitle('Фитон')
        # для чернового листа
        self.flag = False
        # сброс настроек
        self.everything()

        # цвет буковок
        self.kartinka.setStyleSheet("color: white;")
        self.param1label.setStyleSheet("color: white;")
        self.param2label.setStyleSheet("color: white;")
        self.param3label.setStyleSheet("color: white;")

        self.param1label.setEnabled(True)
        self.param2label.setEnabled(True)
        self.param3label.setEnabled(True)

        # Настройки окон открытия и сохранения
        self.openbut.clicked.connect(self.openimage)
        self.savebut.clicked.connect(self.saveimage)

        # Настройки для кнопки по яркости.
        self.bright.clicked.connect(self.brightness)

        # Настройки для кнопки по контрастности
        self.contrast.clicked.connect(self.contrasting)

        # Настройки для кнопки по резкости
        self.reskost.clicked.connect(self.sharpe)

        # Настройки для кнопки по резкости
        self.colorbalance.clicked.connect(self.colorbalancing)

        # Настройки для кнопки по резкости
        self.gaussblur.clicked.connect(self.gaussbluring)

        # Настройки для кнопки по резкости
        self.poster.clicked.connect(self.posterize)

        self.path = ""
        self.pathsave = ""

    def openimage(self):
        # функция для того, чтобы открыть изображение
        # Показ изображения на экране пользователя
        try:
            self.path = str(self.boxopen.text())
            if self.path == "":
                # отключение кнопок
                self.everything()
                raise FileNotFoundError
            elif os.path.isfile(str(self.path)) is False:
                raise FileNotFoundError
            else:
                # включение кнопок
                self.bright.setEnabled(True)
                self.contrast.setEnabled(True)
                self.reskost.setEnabled(True)
                self.colorbalance.setEnabled(True)
                self.gaussblur.setEnabled(True)
                self.poster.setEnabled(True)

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
        self.everything23()
        # функция для изменения яркости изображения
        self.param1label.setText("Яркость: 50%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)  # базовое значение яркости

        # когда ползунок дергается, то происходит вызов функции для изменения яркости
        self.param1.valueChanged.connect(self.brightnessediting)

    def brightnessediting(self):
        self.param1label.setText("Яркость: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Brightness(source)  # модуль изменения контраста
        source = enhancer.enhance(float(float(self.param1.value()) / 50))  # значение контраста
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True  # флаг, чтобы учесть при сохранении, были ли какие-либо изменения в файле.
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))  # отображение

    def contrasting(self):
        # функция для изменения контраста изображения
        self.everything23()
        self.param1label.setText("Контрастность: 50%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)  # базовое значение контраста
        QApplication.processEvents()

        # когда ползунок дергается, то происходит вызов функции для изменения контраста
        self.param1.valueChanged.connect(self.contrastingediting)

    def contrastingediting(self):
        self.param1label.setText("Контрастность: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Contrast(source)  # модуль изменения контраста
        source = enhancer.enhance(float(float(self.param1.value()) / 50))  # значение контраста
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True  # флаг, чтобы учесть при сохранении, были ли какие-либо изменения в файле.
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))  # отображение

    def sharpe(self):
        self.everything23()
        self.param1label.setText("Резкость: 50%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)  # базовое значение яркости
        QApplication.processEvents()

        # когда ползунок дергается, то происходит вызов функции для изменения яркости
        self.param1.valueChanged.connect(self.sharpemaking)

    def sharpemaking(self):
        self.param1label.setText("Резкость: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Sharpness(source)  # модуль изменения резкости
        source = enhancer.enhance(float(float(self.param1.value()) / 25))  # значение резкости
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True  # флаг, чтобы учесть при сохранении, были ли какие-либо изменения в файле.
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))  # отображение

    def colorbalancing(self):
        self.everything23()
        self.param1label.setText("Цветобаланс: 50%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)  # базовое значение яркости
        QApplication.processEvents()

        # когда ползунок дергается, то происходит вызов функции для изменения яркости
        self.param1.valueChanged.connect(self.docolorbalance)

    def docolorbalance(self):
        self.param1label.setText("Цветобаланс: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Color(source)  # модуль изменения баланса
        source = enhancer.enhance(float(float(self.param1.value()) / 30))  # значение баланса
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True  # флаг, чтобы учесть при сохранении, были ли какие-либо изменения в файле.
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))  # отображение

    def gaussbluring(self):
        self.everything23()
        self.param1label.setText("Гауссовое Размытие: 0%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(0)  # базовое значение размытия

        # когда ползунок дергается, то происходит вызов функции для изменения размытия
        self.param1.valueChanged.connect(self.dogaussblur)

    def dogaussblur(self):
        self.param1label.setText(" Гауссовое Размытие: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        source = source.filter(ImageFilter.GaussianBlur(float(float(self.param1.value()) / 25)))  # значение баланса
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True  # флаг, чтобы учесть при сохранении, были ли какие-либо изменения в файле.
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))  # отображение

    def posterize(self):
        self.param1label.setText("Red: -%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(64)  # базовое значение red
        self.param2label.setText("Green: -%")
        self.param2.setEnabled(True)
        self.param2.setSliderPosition(64)  # базовое значение green
        self.param3label.setText("Blue: -%")
        self.param3.setEnabled(True)
        self.param3.setSliderPosition(64)  # базовое значение blue
        QApplication.processEvents()


        # когда ползунок дергается, то происходит вызов функции для изменения каналов
        self.param1.valueChanged.connect(self.doposterizered)
        self.param2.valueChanged.connect(self.doposterizegreen)
        self.param3.valueChanged.connect(self.doposterizeblue)

    def doposterizered(self):
        red = float(self.param1.value()) * 255 / 1000

        self.param1label.setText("Red: " + str(self.param1.value()) + "%")
        self.param2label.setText("Green: -%")
        self.param2.setSliderPosition(64)  # базовое значение green
        self.param3label.setText("Blue: -%")
        self.param3.setSliderPosition(64)  # базовое значение blue

        source = Image.open(self.path)
        source = numpy.array(source)
        source[:, :, 0] = red
        source = Image.fromarray(source)
        source.save("working_sheet.png")
        self.flag = True  # флаг, чтобы учесть при сохранении, были ли какие-либо изменения в файле.
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))  # отображение

    def doposterizegreen(self):
        green = float(self.param2.value()) * 255 / 1000

        self.param1label.setText("Red: -%")
        self.param1.setSliderPosition(64)  # базовое значение red
        self.param2label.setText("Green: " + str(self.param2.value()) + "%")
        self.param3label.setText("Blue: -%")
        self.param3.setSliderPosition(64)  # базовое значение blue

        source2 = Image.open(self.path)
        source2 = numpy.array(source2)
        source2[:, :, 1] = green
        source2 = Image.fromarray(source2)
        source2.save("working_sheet.png")
        self.flag = True  # флаг, чтобы учесть при сохранении, были ли какие-либо изменения в файле.
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))  # отображение

    def doposterizeblue(self):
        blue = float(self.param3.value()) * 255 / 1000

        self.param1label.setText("Red: -%")
        self.param1.setSliderPosition(64)  # базовое значение red
        self.param2label.setText("Green: -%")
        self.param2.setSliderPosition(64)  # базовое значение green
        self.param3label.setText("Blue: " + str(self.param3.value()) + "%")

        source3 = Image.open(self.path)
        source3 = numpy.array(source3)
        source3[:, :, 2] = blue
        source3 = Image.fromarray(source3)
        source3.save("working_sheet.png")

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

        self.reskost.setEnabled(False)
        self.bright.setEnabled(False)
        self.contrast.setEnabled(False)
        self.colorbalance.setEnabled(False)
        self.gaussblur.setEnabled(False)
        self.poster.setEnabled(False)

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
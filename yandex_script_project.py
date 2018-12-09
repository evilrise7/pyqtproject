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
        app.setStyleSheet('QMainWindow{background-color: #161616;}')
        self.initUi()

    def initUi(self):
        self.setWindowTitle('Фитон')
        # для чернового листа
        self.flag = False
        # сброс настроек
        self.everything()

        # цвет буковок там прикольчики
        self.kartinka.setStyleSheet("color: white;")
        self.param1label.setStyleSheet("color: white;")
        self.param2label.setStyleSheet("color: white;")
        self.param3label.setStyleSheet("color: white;")
        self.savelabel.setStyleSheet("color: white;")
        self.boxopen.setStyleSheet(
            "background: #161616; border: 3px solid white; color: white;")

        self.param1label.setEnabled(True)
        self.param2label.setEnabled(True)
        self.param3label.setEnabled(True)

        # Настройки окон открытия и сохранения
        self.openbut.clicked.connect(self.openimage)
        self.savebut.clicked.connect(self.saveimage)
        self.resetbut.clicked.connect(self.resetimage)

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

        # Чтобы кнопки могли быть зажаты
        self.bright.setCheckable(True)
        self.poster.setCheckable(True)
        self.gaussblur.setCheckable(True)
        self.colorbalance.setCheckable(True)
        self.contrast.setCheckable(True)
        self.reskost.setCheckable(True)

        self.path = ""

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
                self.resetbut.setEnabled(True)

                self.savebut.setVisible(True)
                self.resetbut.setVisible(True)
                self.savelabel.setVisible(True)

                self.openbut.setEnabled(False)
                self.boxopen.setEnabled(False)
        except FileNotFoundError:
            self.kartinka.setText("Изображение не найдено!")

            self.boxopen.setText("")

    def saveimage(self):
        # функция для сохранения изображения
        if self.flag:
            source = Image.open("working_sheet.png")  # открываю
            source = numpy.array(source)  # для подстраховки
            source = Image.fromarray(source)  # для подстраховки
            source.save(self.path)  # спаси-сохрани!
            os.remove("working_sheet.png")
        else:
            source = Image.open(self.path)  # открываю
            source = numpy.array(source)  # для подстраховки
            source = Image.fromarray(source)  # для подстраховки
            source.save(self.path)  # спаси-сохрани!

        self.resetimage()

    def brightness(self):
        self.everything23()
        # функция для изменения яркости изображения

        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.bright.setVisible(True)

        self.param1label.setText("Яркость: 50%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)  # базовое значение яркости

        # когда ползунок дергается, то
        # происходит вызов функции для изменения яркости
        self.param1.valueChanged.connect(self.brightnessediting)

    def brightnessediting(self):
        self.param1label.setText("Яркость: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Brightness(source)  # модуль контраста
        source = enhancer.enhance(float(float(self.param1.value()) / 50))
        # значение контраста
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

    def contrasting(self):
        # функция для изменения контраста изображения
        self.everything23()

        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.contrast.setVisible(True)

        self.param1label.setText("Контрастность: 50%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)  # базовое значение контраста
        QApplication.processEvents()

        # когда ползунок дергается, происходит вызов функции контраста
        self.param1.valueChanged.connect(self.contrastingediting)

    def contrastingediting(self):
        self.param1label.setText("Контрастность: " + str(
            self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Contrast(source)  # модуль изменения контраста
        source = enhancer.enhance(
            float(float(self.param1.value()) / 50))  # значение контраста
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

    def sharpe(self):
        self.everything23()
        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.reskost.setVisible(True)

        self.param1label.setText("Резкость: 50%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)  # базовое значение яркости
        QApplication.processEvents()

        # когда ползунок дергается, то происходит вызов функции яркости
        self.param1.valueChanged.connect(self.sharpemaking)

    def sharpemaking(self):
        self.param1label.setText("Резкость: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Sharpness(source)  # модуль изменения резкости
        source = enhancer.enhance(float(float(self.param1.value()) / 25))
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

    def colorbalancing(self):
        self.everything23()
        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.colorbalance.setVisible(True)

        self.param1label.setText("Цветобаланс: 50%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(50)  # базовое значение яркости
        QApplication.processEvents()

        # когда ползунок дергается, то происходит вызов функции яркости
        self.param1.valueChanged.connect(self.docolorbalance)

    def docolorbalance(self):
        self.param1label.setText(
            "Цветобаланс: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Color(source)  # модуль изменения баланса
        source = enhancer.enhance(
            float(float(self.param1.value()) / 30))  # значение баланса
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

    def gaussbluring(self):
        self.everything23()
        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.gaussblur.setVisible(True)

        self.param1label.setText("Гауссовое Размытие: 0%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(0)  # базовое значение размытия

        # когда ползунок дергается, то происходит вызов функции размытия
        self.param1.valueChanged.connect(self.dogaussblur)

    def dogaussblur(self):
        self.param1label.setText(
            "Гауссовое Размытие: " + str(self.param1.value()) + "%")
        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        source = source.filter(
            ImageFilter.GaussianBlur(float(float(self.param1.value()) / 25)))
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

    def posterize(self):
        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.poster.setVisible(True)

        self.param1label.setText("Red: -%")
        self.param1.setEnabled(True)
        self.param1.setSliderPosition(64)  # базовое значение red
        self.param2label.setText("Green: -%")
        self.param2.setEnabled(True)
        self.param2.setSliderPosition(64)  # базовое значение green
        self.param3label.setText("Blue: -%")
        self.param3.setEnabled(True)
        self.param3.setSliderPosition(64)  # базовое значение blue

        # когда ползунок дергается, то происходит вызов функции каналов
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
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

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
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

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

        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

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
        # Обнуляю ползунки
        self.param2.setSliderPosition(0)
        self.param2.setEnabled(False)

        self.param3.setSliderPosition(0)
        self.param3.setEnabled(False)

        self.param1.setSliderPosition(0)
        self.param1.setEnabled(False)

        self.savebut.setEnabled(False)
        self.resetbut.setEnabled(False)

        self.savebut.setVisible(False)
        self.resetbut.setVisible(False)

        self.savebut.setStyleSheet("border-image: url(./YES_OFF.png);")
        self.resetbut.setStyleSheet("border-image: url(./NO_OFF.png);")

        self.savelabel.setVisible(False)

        self.openbut.setEnabled(True)
        self.boxopen.setEnabled(True)

        self.reskost.setEnabled(False)
        self.bright.setEnabled(False)
        self.contrast.setEnabled(False)
        self.colorbalance.setEnabled(False)
        self.gaussblur.setEnabled(False)
        self.poster.setEnabled(False)

        self.path = ""

        self.boxopen.setText("")
        self.openbut.setEnabled(True)
        self.boxopen.setEnabled(True)

        self.kartinka.setPixmap(QtGui.QPixmap(self.path))

        self.flag = False

        self.param1label.setText("-")
        self.param2label.setText("-")
        self.param3label.setText("-")

    def resetbuttons(self):
        self.bright.setEnabled(False)
        self.contrast.setEnabled(False)
        self.poster.setEnabled(False)
        self.gaussblur.setEnabled(False)
        self.colorbalance.setEnabled(False)
        self.reskost.setEnabled(False)

        self.bright.setVisible(False)
        self.contrast.setVisible(False)
        self.poster.setVisible(False)
        self.gaussblur.setVisible(False)
        self.colorbalance.setVisible(False)
        self.reskost.setVisible(False)

        self.savebut.setEnabled(True)
        self.resetbut.setEnabled(True)

        self.savebut.setVisible(True)
        self.resetbut.setVisible(True)

        self.savebut.setStyleSheet("border-image: url(./YES.png);")
        self.resetbut.setStyleSheet("border-image: url(./NO.png);")

    def resetimage(self):
        # Делаю кнопки рабочими
        self.bright.setEnabled(True)
        self.contrast.setEnabled(True)
        self.poster.setEnabled(True)
        self.gaussblur.setEnabled(True)
        self.colorbalance.setEnabled(True)
        self.reskost.setEnabled(True)

        # Делаю кнопки видимыми
        self.bright.setVisible(True)
        self.contrast.setVisible(True)
        self.poster.setVisible(True)
        self.gaussblur.setVisible(True)
        self.colorbalance.setVisible(True)
        self.reskost.setVisible(True)

        # Обнуляю ползунки
        self.param2.setSliderPosition(0)
        self.param2.setEnabled(False)

        self.param3.setSliderPosition(0)
        self.param3.setEnabled(False)

        self.param1.setSliderPosition(0)
        self.param1.setEnabled(False)

        self.savebut.setEnabled(False)
        self.resetbut.setEnabled(False)

        self.savebut.setStyleSheet("border-image: url(./YES_OFF.png);")
        self.resetbut.setStyleSheet("border-image: url(./NO_OFF.png);")

        self.savelabel.setVisible(True)

        self.openbut.setEnabled(True)
        self.boxopen.setEnabled(True)

        self.flag = False

        self.param1label.setText("-")
        self.param2label.setText("-")
        self.param3label.setText("-")

        self.boxopen.setText("")

        self.kartinka.setPixmap(QtGui.QPixmap(self.path))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
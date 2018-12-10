import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import numpy
import os
import random


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
        self.filenamelabel.setStyleSheet("color: white;")
        self.filesizelabel.setStyleSheet("color: white;")
        self.infolabel.setStyleSheet("color: white;")

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

        # Фильтры: Ч/Б, Сепия, Негатив
        self.blackwhite.clicked.connect(self.blackwhitefunc)
        self.sepia.clicked.connect(self.sepiafunc)
        self.negative.clicked.connect(self.negativize)
        self.noise.clicked.connect(self.noisefunc)

        # Чтобы кнопки могли быть зажаты
        self.bright.setCheckable(True)
        self.poster.setCheckable(True)
        self.gaussblur.setCheckable(True)
        self.colorbalance.setCheckable(True)
        self.contrast.setCheckable(True)
        self.reskost.setCheckable(True)
        self.blackwhite.setCheckable(True)
        self.sepia.setCheckable(True)
        self.negative.setCheckable(True)
        self.noise.setCheckable(True)

        self.path = ""

    def openimage(self):
        # функция для того, чтобы открыть изображение
        # Показ изображения на экране пользователя
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
            self.path = fname
            if self.path == "":
                # отключение кнопок
                self.everything()
                raise FileNotFoundError
            elif os.path.isfile(str(self.path)) is False:
                raise FileNotFoundError
            else:
                # включение кнопок
                self.allbuttonTrue()

                self.kartinka.setPixmap(QtGui.QPixmap(self.path))

                self.savebut.setEnabled(True)
                self.resetbut.setEnabled(True)

                self.saveresetlabelVisibleTrue()

                self.filenamelabel.setText(self.path)

                source = Image.open(self.path)
                width = source.size[0]
                height = source.size[1]
                self.filesizelabel.setText("Д: {} ; Ш: {} ;".format(
                    width, height))

        except FileNotFoundError:
            self.kartinka.setText(
                "Изображение не найдено!\nПопробуйте еще раз.")
            self.filenamelabel.setText("имя.png")
            self.filesizelabel.setText("Д: - ; Ш: - ;")

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

        # когда ползунок дергается, то
        # происходит вызов функции для изменения яркости
        self.param1.valueChanged.connect(self.brightnessediting)
        self.param1.setSliderPosition(50)  # базовое значение яркости
        self.everything23()

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
        self.everything23()

    def contrasting(self):
        # функция для изменения контраста изображения
        self.everything23()
        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.contrast.setVisible(True)

        self.param1label.setText("Контрастность: 50%")
        self.param1.setEnabled(True)

        # когда ползунок дергается, происходит вызов функции контраста
        self.param1.valueChanged.connect(self.contrastingediting)
        self.param1.setSliderPosition(50)  # базовое значение контраста

        self.everything23()

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
        self.everything23()

    def sharpe(self):
        self.everything23()
        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.reskost.setVisible(True)

        self.param1label.setText("Резкость: 50%")
        self.param1.setEnabled(True)

        # когда ползунок дергается, то происходит вызов функции яркости
        self.param1.valueChanged.connect(self.sharpemaking)
        self.param1.setSliderPosition(50)  # базовое значение яркости
        self.everything23()

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
        self.everything23()

    def colorbalancing(self):
        self.everything23()
        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.colorbalance.setVisible(True)

        self.param1label.setText("Цветобаланс: 50%")
        self.param1.setEnabled(True)

        # когда ползунок дергается, то происходит вызов функции яркости
        self.param1.valueChanged.connect(self.docolorbalance)
        self.param1.setSliderPosition(50)  # базовое значение яркости
        self.everything23()

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
        self.everything23()

    def gaussbluring(self):
        self.everything23()
        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.gaussblur.setVisible(True)

        self.param1label.setText("Гауссовое Размытие: 0%")
        self.param1.setEnabled(True)

        # когда ползунок дергается, то происходит вызов функции размытия
        self.param1.valueChanged.connect(self.dogaussblur)
        self.param1.setSliderPosition(0)  # базовое значение размытия
        self.everything23()

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
        self.everything23()

    def posterize(self):
        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.poster.setVisible(True)

        self.param1label.setText("Red: 64%")
        self.param1.setEnabled(True)

        self.param2label.setText("Green: -%")
        self.param2.setEnabled(True)

        self.param3label.setText("Blue: -%")
        self.param3.setEnabled(True)

        # когда ползунок дергается, то происходит вызов функции каналов
        self.param1.valueChanged.connect(self.doposterizered)
        self.param1.setSliderPosition(64)  # базовое значение red

        self.param2.valueChanged.connect(self.doposterizegreen)
        self.param2.setSliderPosition(64)  # базовое значение green

        self.param3.valueChanged.connect(self.doposterizeblue)
        self.param3.setSliderPosition(64)  # базовое значение blue

    def doposterizered(self):
        red = float(self.param1.value()) * 255 / 1000

        self.param1label.setText("Red: " + str(self.param1.value()) + "%")
        self.param2label.setText("Green: -%")
        self.param3label.setText("Blue: -%")

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
        self.param2label.setText("Green: " + str(self.param2.value()) + "%")
        self.param3label.setText("Blue: -%")

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
        self.param2label.setText("Green: -%")
        self.param3label.setText("Blue: " + str(self.param3.value()) + "%")

        source3 = Image.open(self.path)
        source3 = numpy.array(source3)
        source3[:, :, 2] = blue
        source3 = Image.fromarray(source3)
        source3.save("working_sheet.png")

        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

    def blackwhitefunc(self):
        self.everything123()
        # Выключаем доступ ко всем кнопкам кроме данной
        self.resetbuttons()
        self.blackwhite.setVisible(True)

        source = Image.open(self.path)  # открываю
        source = numpy.array(source)  # для подстраховки
        source = Image.fromarray(source)  # для подстраховки
        enhancer = ImageEnhance.Color(source)  # модуль изменения баланса
        source = enhancer.enhance(0.0)  # значение баланса
        source.save("working_sheet.png")  # спаси-сохрани!
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

    def sepiafunc(self):
        self.everything123()
        self.resetbuttons()
        self.sepia.setVisible(True)

        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)
        width = source.size[0]  # ширина.
        height = source.size[1]  # высота.s
        pix = source.load()

        for i in range(width):
            for j in range(height):
                # разбиваем на каналы
                red = pix[i, j][0]
                green = pix[i, j][1]
                blue = pix[i, j][2]
                # нахожу среднее значение всех пикселей
                avg = (red + green + blue) // 3
                red = avg + 10 * 2  # 10 - глубина
                green = avg + 10  # если: 100 - суперярко; 0 - пещера
                blue = avg

                # приводим к адекватным показателям(0 - 255)
                if red > 255:
                    red = 255
                if green > 255:
                    green = 255
                if blue > 255:
                    blue = 255
                # прорисовываем
                draw.point((i, j), (red, green, blue))

        source.save("working_sheet.png")
        del draw
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

    def negativize(self):
        self.everything123()
        self.resetbuttons()
        self.negative.setVisible(True)

        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)
        width = source.size[0]  # ширина.
        height = source.size[1]  # высота
        pix = source.load()  # загрузка пикселей

        for i in range(width):
            for j in range(height):
                red = pix[i, j][0]
                green = pix[i, j][1]
                blue = pix[i, j][2]
                draw.point((i, j), (255 - red, 255 - green, 255 - blue))

        source.save("working_sheet.png")
        del draw
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))

    def noisefunc(self):
        # Выключаем доступ ко всем кнопкам кроме данной
        self.everything23()
        self.resetbuttons()

        self.param1label.setText("Степень щелчка: 0%")
        self.param1.setEnabled(True)
        self.noise.setVisible(True)

        # когда ползунок дергается, то происходит вызов функции размытия
        self.param1.valueChanged.connect(self.donoise)
        self.param1.setSliderPosition(0)  # базовое значение размытия
        self.everything23()

    def donoise(self):
        self.everything23()
        self.resetbuttons1()
        self.noise.setVisible(True)

        self.param1label.setText(
            "Степень щелчка: " + str(self.param1.value()) + "%")

        source = Image.open(self.path)
        draw = ImageDraw.Draw(source)
        width = source.size[0]  # ширина.
        height = source.size[1]  # высота
        pix = source.load()  # загрузка пикселей

        stepen = int(self.param1.value())
        for i in range(width):
            for j in range(height):
                rand = random.randint(-stepen, stepen)
                red = pix[i, j][0] + rand
                green = pix[i, j][1] + rand
                blue = pix[i, j][2] + rand
                if red < 0:
                    red = 0
                if green < 0:
                    green = 0
                if blue < 0:
                    blue = 0
                if red > 255:
                    red = 255
                if green > 255:
                    green = 255
                if blue > 255:
                    blue = 255
                draw.point((i, j), (red, green, blue))

        source.save("working_sheet.png")
        del draw
        self.flag = True
        self.kartinka.setPixmap(QtGui.QPixmap("working_sheet.png"))
        self.everything23()

    def resetbuttons(self):  # Сброс кнопок
        self.allbuttonsFalse()
        self.everything123()

        self.bright.setVisible(False)
        self.contrast.setVisible(False)
        self.poster.setVisible(False)
        self.gaussblur.setVisible(False)
        self.colorbalance.setVisible(False)
        self.reskost.setVisible(False)
        self.blackwhite.setVisible(False)
        self.sepia.setVisible(False)
        self.negative.setVisible(False)
        self.noise.setVisible(False)

        self.savebut.setEnabled(True)
        self.resetbut.setEnabled(True)

        self.saveresetlabelVisibleTrue()
        self.savebut.setStyleSheet("border-image: url(./YES.png);")
        self.resetbut.setStyleSheet("border-image: url(./NO.png);")

    def resetimage(self):
        # Делаю кнопки рабочими и обнуляю ползунки
        self.allbuttonTrue()
        self.everything123()

        self.savebut.setEnabled(False)
        self.resetbut.setEnabled(False)

        self.saveresetbuttonOff()

        self.savelabel.setVisible(True)

        self.openbut.setEnabled(True)

        self.flag = False

        self.kartinka.setPixmap(QtGui.QPixmap(self.path))

    def saveresetlabelVisibleTrue(self):
        self.savebut.setVisible(True)
        self.resetbut.setVisible(True)
        self.savelabel.setVisible(True)

    def saveresetbuttonOff(self):
        self.savebut.setStyleSheet("border-image: url(./YES_OFF.png);")
        self.resetbut.setStyleSheet("border-image: url(./NO_OFF.png);")

    def butresetsaveFalse(self):
        self.savebut.setEnabled(False)
        self.resetbut.setEnabled(False)

    def allbuttonsFalse(self):
        self.reskost.setEnabled(False)
        self.bright.setEnabled(False)
        self.contrast.setEnabled(False)
        self.colorbalance.setEnabled(False)
        self.gaussblur.setEnabled(False)
        self.poster.setEnabled(False)
        self.blackwhite.setEnabled(False)
        self.sepia.setEnabled(False)
        self.negative.setEnabled(False)
        self.noise.setEnabled(False)

    def allbuttonTrue(self):
        self.bright.setEnabled(True)
        self.contrast.setEnabled(True)
        self.poster.setEnabled(True)
        self.gaussblur.setEnabled(True)
        self.colorbalance.setEnabled(True)
        self.reskost.setEnabled(True)
        self.blackwhite.setEnabled(True)
        self.sepia.setEnabled(True)
        self.negative.setEnabled(True)
        self.noise.setEnabled(True)

        self.bright.setVisible(True)
        self.contrast.setVisible(True)
        self.poster.setVisible(True)
        self.gaussblur.setVisible(True)
        self.colorbalance.setVisible(True)
        self.reskost.setVisible(True)
        self.blackwhite.setVisible(True)
        self.sepia.setVisible(True)
        self.negative.setVisible(True)
        self.noise.setVisible(True)

    def everything123(self):
        # сброс всех ползунков
        self.param2.setSliderPosition(0)
        self.param3.setSliderPosition(0)
        self.param1.setSliderPosition(0)
        self.param3.setEnabled(False)
        self.param2.setEnabled(False)
        self.param1.setEnabled(False)
        self.param2label.setText("-")
        self.param3label.setText("-")
        self.param1label.setText("-")

    def everything23(self):
        # функция для отключения 2-го и 3-го ползунков
        self.param2.setSliderPosition(0)
        self.param2.setEnabled(False)

        self.param3.setSliderPosition(0)
        self.param3.setEnabled(False)

        self.param2label.setText("-")
        self.param3label.setText("-")

    def everything13(self):
        # функция для отключения 1-го и 3-го ползунков
        self.param1.setSliderPosition(0)
        self.param1.setEnabled(False)

        self.param3.setSliderPosition(0)
        self.param3.setEnabled(False)

        self.param1label.setText("-")
        self.param3label.setText("-")

    def everything21(self):
        # функция для отключения 2-го и 1-го ползунков
        self.param2.setSliderPosition(0)
        self.param2.setEnabled(False)

        self.param1.setSliderPosition(0)
        self.param1.setEnabled(False)

        self.param2label.setText("-")
        self.param1label.setText("-")

    def everything(self):
        # функция для полного сброса настроек
        self.everything123()

        self.butresetsaveFalse()

        self.savebut.setVisible(False)
        self.resetbut.setVisible(False)

        self.saveresetbuttonOff()

        self.savelabel.setVisible(False)

        self.openbut.setEnabled(True)

        self.allbuttonsFalse()

        self.path = ""

        self.openbut.setEnabled(True)

        self.kartinka.setPixmap(QtGui.QPixmap(self.path))

        self.flag = False


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
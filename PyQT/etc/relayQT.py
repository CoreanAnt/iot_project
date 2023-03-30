import RPi.GPIO as GPIO
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RELAY_PIN_1 = 17
RELAY_PIN_2 = 18
RELAY_PIN_3 = 27

GPIO.setup(RELAY_PIN_1, GPIO.OUT)
GPIO.setup(RELAY_PIN_2, GPIO.OUT)
GPIO.setup(RELAY_PIN_3, GPIO.OUT)

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Relay Control'
        self.left = 200
        self.top = 200
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 릴레이 1 제어 버튼
        self.relay1_button = QPushButton('red', self)
        self.relay1_button.setCheckable(True)
        self.relay1_button.move(20, 20)
        self.relay1_button.clicked.connect(self.relay_1_toggle)

        # 릴레이 2 제어 버튼
        self.relay2_button = QPushButton('green', self)
        self.relay2_button.setCheckable(True)
        self.relay2_button.move(20, 70)
        self.relay2_button.clicked.connect(self.relay_2_toggle)

        # 릴레이 3 제어 버튼
        self.relay3_button = QPushButton('blue', self)
        self.relay3_button.setCheckable(True)
        self.relay3_button.move(20, 120)
        self.relay3_button.clicked.connect(self.relay_3_toggle)

        self.show()

    def relay_1_toggle(self, checked):
        if checked:
            GPIO.output(RELAY_PIN_1, GPIO.HIGH)
        else:
            GPIO.output(RELAY_PIN_1, GPIO.LOW)

    def relay_2_toggle(self, checked):
        if checked:
            GPIO.output(RELAY_PIN_2, GPIO.HIGH)
        else:
            GPIO.output(RELAY_PIN_2, GPIO.LOW)

    def relay_3_toggle(self, checked):
        if checked:
            GPIO.output(RELAY_PIN_3, GPIO.HIGH)
        else:
            GPIO.output(RELAY_PIN_3, GPIO.LOW)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

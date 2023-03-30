import time
import serial

import dbConn as dC

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont


import RPi.GPIO as GPIO

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

# Set up GPIO pins for relay control
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT) # Relay channel 1
    GPIO.setup(18, GPIO.OUT) # Relay channel 2
    GPIO.setup(24, GPIO.OUT) # Relay channel 3
except:
    print("Error setting up GPIO pins. Please check connection.")


def toggle_relay1():
    # Toggle state of relay 1
    if GPIO.input(17):
        GPIO.output(17, GPIO.LOW)
    else:
        GPIO.output(17, GPIO.HIGH)


def toggle_relay2():
    # Toggle state of relay 2
    if GPIO.input(18):
        GPIO.output(18, GPIO.LOW)
    else:
        GPIO.output(18, GPIO.HIGH)


def toggle_relay3():
    # Toggle state of relay 3
    if GPIO.input(27):
        GPIO.output(27, GPIO.LOW)
    else:
        GPIO.output(27, GPIO.HIGH)


app = QApplication(sys.argv)

window = QMainWindow()
layout = QVBoxLayout()

temperature_label = QLabel("Temperature")
humidity_label = QLabel("Humidity")
light_label = QLabel("Light")
soil_label = QLabel("Soil moisture")
water_label = QLabel("물통의 물이 있는지 체크합니다.")
mpu_label = QLabel("수평을 체크합니다.")

font = QFont("Arial", 20)
temperature_label.setFont(font)
humidity_label.setFont(font)
light_label.setFont(font)
soil_label.setFont(font)
water_label.setFont(font)
mpu_label.setFont(font)

# Add a button to control the relays
relay_button1 = QPushButton('red')
relay_button2 = QPushButton('green')
relay_button3 = QPushButton('blue')

relay_button1.clicked.connect(toggle_relay1)
relay_button2.clicked.connect(toggle_relay2)
relay_button3.clicked.connect(toggle_relay3)

layout.addWidget(temperature_label)
layout.addWidget(humidity_label)
layout.addWidget(light_label)
layout.addWidget(soil_label)
layout.addWidget(water_label)
layout.addWidget(mpu_label)
layout.addWidget(relay_button1)
layout.addWidget(relay_button2)
layout.addWidget(relay_button3)


widget = QWidget()
widget.setLayout(layout)

window.setCentralWidget(widget)
window.setWindowTitle("smartFarm")
window.setStyleSheet("background-color: white;")
window.show()

sys.exit(app.exec_())

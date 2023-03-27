import time
import serial
import datetime
import dbConn as dC

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer,Qt


import RPi.GPIO as GPIO



relay_button_pressed = False

class SmartFarm(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up GUI layout
        self.layout = QVBoxLayout()
        self.temperature_label = QLabel("Temperature")
        self.humidity_label = QLabel("Humidity")
        self.light_label = QLabel("Light")
        self.soil_label = QLabel("Soil moisture")
        self.fire_label = QLabel("화재를 감시 합니다.")

        font = QFont("Arial", 20)
        self.temperature_label.setFont(font)
        self.humidity_label.setFont(font)
        self.light_label.setFont(font)
        self.soil_label.setFont(font)
        self.fire_label.setFont(font)

        # Add a button to control the relays
        self.relay_button1 = QPushButton('red')
        self.relay_button2 = QPushButton('green')
        self.relay_button3 = QPushButton('blue')
        self.relay_button4 = QPushButton('fan')

        self.relay_button1.clicked.connect(self.toggle_relay1)
        self.relay_button1.clicked.connect(self.buttonClicked)
        self.relay_button2.clicked.connect(self.toggle_relay2)
        self.relay_button2.clicked.connect(self.buttonClicked)
        self.relay_button3.clicked.connect(self.toggle_relay3)
        self.relay_button3.clicked.connect(self.buttonClicked)
        self.relay_button4.clicked.connect(self.toggle_relay4)
        self.relay_button4.clicked.connect(self.buttonClicked)

        self.layout.addWidget(self.temperature_label)
        self.layout.addWidget(self.humidity_label)
        self.layout.addWidget(self.light_label)
        self.layout.addWidget(self.soil_label)
        self.layout.addWidget(self.fire_label)
        self.layout.addWidget(self.relay_button1)
        self.layout.addWidget(self.relay_button2)
        self.layout.addWidget(self.relay_button3)
        self.layout.addWidget(self.relay_button4)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("smartFarm")
        self.setWindowState(self.windowState() | Qt.WindowMaximized | Qt.WindowTitleHint)
        self.setStyleSheet("background-color: white;")

        # # Set up serial connection
        self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

        # Set up GPIO pins for relay control
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT) # Relay channel 1
            GPIO.setup(18, GPIO.OUT) # Relay channel 2
            GPIO.setup(24, GPIO.OUT) # Relay channel 3
            GPIO.setup(27, GPIO.OUT) # Relay channel 4(Fan)
        except:
            print("Error setting up GPIO pins. Please check connection.")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update data every 1000 milliseconds (1 second)

        self.show()

    
        
    def buttonClicked(self):
        global relay_button_pressed
        sender = self.sender()  # Get the button that was clicked
        
        # Check which button was clicked and toggle the corresponding variable
        if sender == self.relay_button1:
            relay_button_pressed = not relay_button_pressed
            print("Relay1 Button Clicked: ", relay_button_pressed)

            # 릴레이 제어
            if relay_button_pressed ==True:
                print("Relay ON")
        
            elif relay_button_pressed ==False:
                print("Relay OFF")
                
                
        elif sender == self.relay_button2:
            print("Relay2 Button Clicked")

        elif sender == self.relay_button3:
            print("Relay3 Button Clicked")

        elif sender == self.relay_button4:
            print("Relay4 Button Clicked")

    def toggle_relay1(self):
        # Toggle state of relay 1
        if GPIO.input(17):
            GPIO.output(17, GPIO.LOW)
        else:
            GPIO.output(17, GPIO.HIGH)


    def toggle_relay2(self):
        # Toggle state of relay 2
        if GPIO.input(18):
            GPIO.output(18, GPIO.LOW)
        else:
            GPIO.output(18, GPIO.HIGH)


    def toggle_relay3(self):
        # Toggle state of relay 3
        if GPIO.input(24):
            GPIO.output(24, GPIO.LOW)
        else:
            GPIO.output(24, GPIO.HIGH)

    def toggle_relay4(self):
        # Toggle state of relay 3
        if GPIO.input(27):
            GPIO.output(27, GPIO.LOW)
        else:
            GPIO.output(27, GPIO.HIGH)

    def update_data(self):
        
        data = self.ser.readline().decode()
        now = datetime.datetime.now()

        
        

        if "temperature:" in data:
            temperature = int(data.split(":")[1])
            temperatureValue = temperature
            self.temperature_label.setText("Temperature : " + str(temperatureValue))
            self.temperature_label.setStyleSheet("color: blue;"
                    "background-color: #87CEFA;"
                    "border-style: dashed;"
                    "border-width: 3px;"
                    "border-color: #1E90FF")
            self.temperature_label.adjustSize()

            if now.minute == 0 and now.second < 10:
                dC.insertSensor1(temperatureValue)
            elif now.minute == 30 and now.second < 10:
                dC.insertSensor1(temperatureValue)
           
        


        if "humidity:" in data:
            humidity = int(data.split(":")[1])
            humidityValue = humidity
            self.humidity_label.setText("Humidity(%) : " + str(humidityValue))
            self.humidity_label.setStyleSheet("color: blue;"
                    "background-color: #87CEFA;"
                    "border-style: dashed;"
                    "border-width: 3px;"
                    "border-color: #1E90FF")
            self.humidity_label.adjustSize()

            if now.minute == 0 and now.second < 10:
                dC.insertSensor2(humidityValue)
            elif now.minute == 30 and now.second < 10:
                dC.insertSensor2(humidityValue)
           


            if humidityValue > 20:
                GPIO.output(27, GPIO.HIGH)

            elif humidityValue <= 20:
                GPIO.output(27, GPIO.LOW)


        

        if "light :" in data:
            light = int(data.split(":")[1])
            lightValue = light
            self.light_label.setText("Light : " + str(lightValue))
            self.light_label.setStyleSheet("color: blue;"
                    "background-color: #87CEFA;"
                    "border-style: dashed;"
                    "border-width: 3px;"
                    "border-color: #1E90FF")
            self.light_label.adjustSize()
            
            if now.minute == 0 and now.second < 10:
                dC.insertSensor3(lightValue)
            


            if(lightValue < 300 and relay_button_pressed ==False):
                GPIO.output(17, GPIO.LOW)
                GPIO.output(18, GPIO.LOW)
                GPIO.output(24, GPIO.LOW)
            elif(lightValue >= 300 and relay_button_pressed ==False):
                GPIO.output(17, GPIO.HIGH)
                GPIO.output(18, GPIO.HIGH)
                GPIO.output(24, GPIO.HIGH)
                
        
                

        if "soil :" in data:
            soil = int(data.split(":")[1])
            soilValue = soil
            self.soil_label.setText("Soil moisture: " + str(soilValue))
            self.soil_label.setStyleSheet("color: blue;"
                    "background-color: #87CEFA;"
                    "border-style: dashed;"
                    "border-width: 3px;"
                    "border-color: #1E90FF")
            self.soil_label.adjustSize()
           
            if now.minute == 0 and now.second < 10:
                dC.insertSensor4(soilValue)
            elif now.minute == 30 and now.second < 10:
                dC.insertSensor4(soilValue)
           
        


         
        


        if "fire :" in data:
            fire = int(data.split(":")[1])
            
        
            if (fire == 0):
        
                self.fire_label.setText("화재 감시중")
                self.fire_label.setStyleSheet("color: green;"
                            "border-style: dashed;"
                            "border-width: 3px;"
                            "border-color: #7FFFD4;;"
                            "background-color: white;"
                            "border-radius: 3px")
            elif(fire == 1):
                self.fire_label.setText("화재 발생!!")
                self.fire_label.setStyleSheet("color: red;"
                            "border-style: dashed;"
                            "border-width: 3px;"
                            "border-color: #FA8072;"
                            "background-color: white;"
                            "border-radius: 3px")

        

        time.sleep(0.1)








if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartFarm()
    while True:
        window.update_data()

        sys.exit(app.exec_())
    

        

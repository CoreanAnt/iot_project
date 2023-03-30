import time
import serial

import dbConn as dC

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont


import RPi.GPIO as GPIO

relay_button_pressed = False

# import smbus         #import SMBus module of I2C
# from time import sleep          #import

# #some MPU6050 Registers and their Address
# PWR_MGMT_1   = 0x6B
# SMPLRT_DIV   = 0x19
# CONFIG       = 0x1A
# GYRO_CONFIG  = 0x1B
# INT_ENABLE   = 0x38
# ACCEL_XOUT_H = 0x3B
# ACCEL_YOUT_H = 0x3D
# ACCEL_ZOUT_H = 0x3F
# GYRO_XOUT_H  = 0x43
# GYRO_YOUT_H  = 0x45
# GYRO_ZOUT_H  = 0x47

# Q_angle = 0.001
# Q_gyro = 0.003
# R_angle = 0.03

# angle = 0
# bias = 0
# P = [[1, 0], [0, 1]]

# def KalmanFilterGYRO(angle, gyro, dt):
#     global Q_angle
#     global Q_gyro
#     global R_angle
#     global bias
#     global P
    
#     rate = gyro - bias
#     angle += rate * dt
    
#     P[0][0] += dt * (2*P[1][1] - Q_angle)
#     P[0][1] -= dt * P[1][1]
#     P[1][0] -= dt * P[1][1]
#     P[1][1] += Q_gyro * dt
    
#     S = P[0][0] + R_angle
#     K = [P[0][0]/S, P[1][0]/S]
    
#     y = angle - angle
#     angle += K[0] * y
#     bias += K[1] * y
#     P00_temp = P[0][0]
#     P[0][0] -= K[0] * P00_temp
#     P[0][1] -= K[0] * P[0][1]
#     P[1][0] -= K[1] * P00_temp
#     P[1][1] -= K[1] * P[0][1]
    
#     return angle, bias



# def MPU_Init():
#    #write to sample rate register
#    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
   
#    #Write to power management register
#    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
   
#    #Write to Configuration register
#    bus.write_byte_data(Device_Address, CONFIG, 0)
   
#    #Write to Gyro configuration register
#    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
   
#    #Write to interrupt enable register
#    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

# def read_raw_data(addr):
#    #Accelero and Gyro value are 16-bit
#         high = bus.read_byte_data(Device_Address, addr)
#         low = bus.read_byte_data(Device_Address, addr+1)
    
#         #concatenate higher and lower value
#         value = ((high << 8) | low)
        
#         #to get signed value from mpu6050
#         if(value > 32768):
#                 value = value - 65536
#         return value


# bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
# Device_Address = 0x68   # MPU6050 device address

# MPU_Init()










# 센서 핀 설정

#자이로센서 SDA=2,SCL=3

#수위감지 센서
# sensor_pin = 27



# 부저 
# buzzer_pin = 18


#불꽃감지 센서
# inputPin = 17


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
    if GPIO.input(18):
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
    if GPIO.input(24):
        GPIO.output(24, GPIO.LOW)
    else:
        GPIO.output(24, GPIO.HIGH)













app = QApplication(sys.argv)

window = QMainWindow()
layout = QVBoxLayout()

temperature_label = QLabel("Temperature")
humidity_label = QLabel("Humidity")
light_label = QLabel("Light")
soil_label = QLabel("Soil moisture")
water_label = QLabel("물통의 물이 있는지 체크합니다.")
# mpu_label = QLabel("수평을 체크합니다.")

font = QFont("Arial", 20)
temperature_label.setFont(font)
humidity_label.setFont(font)
light_label.setFont(font)
soil_label.setFont(font)
water_label.setFont(font)
# mpu_label.setFont(font)


# Add a button to control the relays
relay_button1 = QPushButton('red')
relay_button2 = QPushButton('green')
relay_button3 = QPushButton('blue')

# relay_button1.clicked.connect(toggle_relay1)
# relay_button2.clicked.connect(toggle_relay2)
# relay_button3.clicked.connect(toggle_relay3)
relay_button1.clicked.connect(lambda: toggle_relay1() if not relay_button1.isChecked() else None)
relay_button2.clicked.connect(lambda: toggle_relay2() if not relay_button2.isChecked() else None)
relay_button3.clicked.connect(lambda: toggle_relay3() if not relay_button3.isChecked() else None)


layout.addWidget(temperature_label)
layout.addWidget(humidity_label)
layout.addWidget(light_label)
layout.addWidget(soil_label)
layout.addWidget(water_label)
# layout.addWidget(mpu_label)
layout.addWidget(relay_button1)
layout.addWidget(relay_button2)
layout.addWidget(relay_button3)



widget = QWidget()
widget.setLayout(layout)

window.setCentralWidget(widget)
window.setWindowTitle("smartFarm")
window.setStyleSheet("background-color: white;")
window.show()



def buttonClicked(self):
        global relay_button_pressed
        sender = self.sender() 
    
        
        # Check which button was clicked and toggle the corresponding variable
        if sender == relay_button1:
            relay_button_pressed = not relay_button_pressed
            print("Relay1 Button Clicked: ", relay_button_pressed)

            # 릴레이 제어
            if relay_button_pressed ==True:
                print("Relay ON")
        
            elif relay_button_pressed ==False:
                print("Relay OFF")
                
        elif sender == relay_button2:
            print("Relay2 Button Clicked")
        elif sender == relay_button3:
            print("Relay2 Button Clicked")








while True:
    data = ser.readline().decode()

    if "temperature:" in data:
        temperature = int(data.split(":")[1])
        temperatureValue = temperature
        dC.insertSensor1(temperatureValue)
        temperature_label.setText("Temperature(°C) : " + str(temperatureValue))
        app.processEvents()
        temperature_label.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: dashed;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")
        

    if "humidity:" in data:
        humidity = int(data.split(":")[1])
        humidityValue = humidity
        dC.insertSensor2(humidityValue)
        humidity_label.setText("Humidity(%) : " + str(humidityValue))
        app.processEvents()
        humidity_label.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: dashed;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")
     

    if "light :" in data:
        adc1 = int(data.split(":")[1])
        adc1Value = adc1
        dC.insertSensor3(adc1Value)
        light_label.setText("Light : " + str(adc1Value))
        app.processEvents()
        light_label.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: dashed;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")
        print(relay_button1.setChecked)
        if(relay_button1.setChecked(False) and adc1Value < 1000):
            GPIO.output(17, GPIO.HIGH)
        # elif(relay_button1.setChecked(False) and adc1Value >= 600):
        #     GPIO.output(17, GPIO.LOW)


        
        

    if "soil :" in data:
        adc2 = int(data.split(":")[1])
        adc2Value = adc2
        dC.insertSensor4(adc2Value)
        soil_label.setText("Soil moisture : " + str(adc2Value))
        app.processEvents()
        soil_label.setStyleSheet("color: blue;"
                       "background-color: #87CEFA;"
                       "border-style: dashed;"
                       "border-width: 3px;"
                       "border-color: #1E90FF")
    

      




# 수위센서 관련 동작
   

    if "water :" in data:
        water = int(data.split(":")[1])
        
    
        if (water == 1):
    
            water_label.setText("물통에 물이 충분합니다.")
            app.processEvents()
            water_label.setStyleSheet("color: green;"
                        "border-style: dashed;"
                        "border-width: 3px;"
                        "border-color: #7FFFD4;;"
                        "background-color: white;"
                        "border-radius: 3px")
        elif(water == 0):
            water_label.setText("경고 : 물통에 물이 부족합니다!!")
            app.processEvents()
            water_label.setStyleSheet("color: red;"
                        "border-style: dashed;"
                        "border-width: 3px;"
                        "border-color: #FA8072;"
                        "background-color: white;"
                        "border-radius: 3px")

       









    # # #자이로센서 관련동작

    #  #Read Accelerometer raw value
    # acc_x = read_raw_data(ACCEL_XOUT_H)
    # acc_y = read_raw_data(ACCEL_YOUT_H)
    # acc_z = read_raw_data(ACCEL_ZOUT_H)
    
    # #Read Gyroscope raw value
    # gyro_x = read_raw_data(GYRO_XOUT_H)
    # gyro_y = read_raw_data(GYRO_YOUT_H)
    # gyro_z = read_raw_data(GYRO_ZOUT_H)
    
    # #Full scale range +/- 250 degree/C as per sensitivity scale factor
    # Ax = acc_x/16384.0
    # Ay = acc_y/16384.0
    # Az = acc_z/16384.0
    
    # Gx = gyro_x/131.0
    # Gy = gyro_y/131.0
    # Gz = gyro_z/131.0
    
    # angle = KalmanFilterGYRO(angle, Gy, 0.01)[0]

    # # print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az, "\tAngle=%.2f" %angle, u'\u00b0')
    # sleep(1)


    # if Ax>0.35 or Ax<-0.35:
    #     mpu_label.setText("경고!! 수평이 맞지 않습니다!!")
    #     mpu_label.setStyleSheet("color: red;"
    #                   "border-style: dashed;"
    #                   "border-width: 3px;"
    #                   "border-color: #FA8072;"
    #                   "background-color: white;"
    #                   "border-radius: 3px")

    # elif Ay>0.2 or Ay<-0.2:
    #     mpu_label.setText("경고!! 수평이 맞지 않습니다!!")
    #     mpu_label.setStyleSheet("color: red;"
    #                   "border-style: dashed;"
    #                   "border-width: 3px;"
    #                   "border-color: #FA8072;"
    #                   "background-color: white;"
    #                   "border-radius: 3px")
        

    # elif Az>1.05:
    #     mpu_label.setText("경고!! 수평이 맞지 않습니다!!")
    #     mpu_label.setStyleSheet("color: red;"
    #                   "border-style: dashed;"
    #                   "border-width: 3px;"
    #                   "border-color: #FA8072;"
    #                   "background-color: white;"
    #                   "border-radius: 3px")
    

    # else:
    #     mpu_label.setText("수평 이상 없습니다.")
    #     mpu_label.setStyleSheet("color: green;"
    #                   "border-style: dashed;"
    #                   "border-width: 3px;"
    #                   "border-color:#7FFFD4;"
    #                   "background-color: white;"
    #                   "border-radius: 3px")


# GPIO 정리
GPIO.cleanup()


   
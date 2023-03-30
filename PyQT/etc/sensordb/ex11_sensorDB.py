# import spidevRead as sr

import time
import serial

import dbConn as dC




ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)





while True:   
    data = ser.readline().decode()  # read the data from the serial port and decode it
     
        
    if "temperature:" in data:
        temperature = int(data.split(":")[1])  # extract the temperature value
        temperatureValue=temperature 
        dC.insertSensor1(temperatureValue)

        print("Temperature:",temperatureValue)

        time.sleep(1) 
        

    if "humidity:" in data:
        humidity = int(data.split(":")[1])  # extract the humidity value
        humidityValue = humidity #습도
    
        dC.insertSensor2(humidityValue)

        print("Humidity:",humidityValue)

        time.sleep(1)
        

    if "light :" in data:
        adc1 = int(data.split(":")[1])  # extract the ADC1 value
        adc1Value = adc1 #조도
    
        dC.insertSensor3(adc1Value)

        print("light:",adc1Value)

        time.sleep(1)
        

    if "soil :" in data:
        adc2 = int(data.split(":")[1])  # extract the ADC2 value
        adc2Value= adc2 #토양습도
    
        dC.insertSensor4(adc2Value)

        print("soil:",adc2Value)

        time.sleep(1)
    
    

    


   
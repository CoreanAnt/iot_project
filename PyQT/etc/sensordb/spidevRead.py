import spidev
import serial




 

spi = spidev.SpiDev()

 

spi.open(0,0)

 

spi.max_speed_hz = 16000000 

 

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)


while True:
    data = ser.readline().decode()  # read the data from the serial port and decode it
    if "temperature:" in data:
        temperature = int(data.split(":")[1])  # extract the temperature value
        print("Temperature:", temperature)
    if "humidity:" in data:
        humidity = int(data.split(":")[1])  # extract the humidity value
        print("Humidity:", humidity)
    if "light :" in data:
        adc1 = int(data.split(":")[1])  # extract the ADC1 value
        print("light:", adc1)
    if "soil :" in data:
        adc2 = int(data.split(":")[1])  # extract the ADC2 value
        print("soil:", adc2)

        













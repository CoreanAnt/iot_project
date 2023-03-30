import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # BCM 모드 설정
GPIO.setwarnings(False) # 경고 메시지 끄기

# 4채널 릴레이 모듈에 연결된 핀 번호 설정
RELAY_PIN_1 = 17
RELAY_PIN_2 = 18
RELAY_PIN_3 = 27


# 각 핀을 출력 모드로 설정
GPIO.setup(RELAY_PIN_1, GPIO.OUT)
GPIO.setup(RELAY_PIN_2, GPIO.OUT)
GPIO.setup(RELAY_PIN_3, GPIO.OUT)


# 모든 릴레이를 끄는 함수
def all_relays_off():
    GPIO.output(RELAY_PIN_1, GPIO.LOW)
    GPIO.output(RELAY_PIN_2, GPIO.LOW)
    GPIO.output(RELAY_PIN_3, GPIO.LOW)
 

# 릴레이 1을 켜는 함수
def relay_1_on():
    GPIO.output(RELAY_PIN_1, GPIO.HIGH)

# 릴레이 2를 켜는 함수
def relay_2_on():
    GPIO.output(RELAY_PIN_2, GPIO.HIGH)

# 릴레이 3을 켜는 함수
def relay_3_on():
    GPIO.output(RELAY_PIN_3, GPIO.HIGH)



# 릴레이 1을 끄는 함수
def relay_1_off():
    GPIO.output(RELAY_PIN_1, GPIO.LOW)

# 릴레이 2를 끄는 함수
def relay_2_off():
    GPIO.output(RELAY_PIN_2, GPIO.LOW)

# 릴레이 3을 끄는 함수
def relay_3_off():
    GPIO.output(RELAY_PIN_3, GPIO.LOW)



# 1초 간격으로 릴레이를 켜고 끄는 예제
while True:
    relay_1_on()
    time.sleep(1)
    relay_1_off()
    time.sleep(1)
    relay_2_on()
    time.sleep(1)
    relay_2_off()
    time.sleep(1)
    relay_3_on()
    time.sleep(1)
    relay_3_off()
    time.sleep(1)
   

# # 모든 릴레이를 끄기
# all_relays_off()

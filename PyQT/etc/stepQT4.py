import serial
import time
import keyboard

# 시리얼 포트 설정
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

# 초기값 설정
forward = True
pulse_width = 0

# 무한 루프
while True:
    cmd = input('a:정방향 회전 /b:역방향 회전 /q:종료')

    # 키보드 입력 감지
    if cmd == "a":
        pulse_width = 1000
        forward = True
    elif cmd == "s":
        pulse_width = 1000
        forward = False
    elif cmd == "q":
        break  # q 키를 누르면 프로그램 종료

    # 시리얼 통신으로 pulse_width와 forward 전송
    pulse_width_str = str(pulse_width)
    forward_str = str(int(forward))
    message = pulse_width_str + ',' + forward_str
    ser.write(message.encode())

    # 0.5초 대기
    time.sleep(0.5)

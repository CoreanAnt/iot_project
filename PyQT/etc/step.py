import serial
import time

# 시리얼 포트와 baud rate 지정
ser = serial.Serial('/dev/ttyS0', 9600)
time.sleep(2)  # 접속 대기


def flash():

    while(True):
        cmd = input('a:정방향 회전 /b:역방향 회전 /q:종료')

        if cmd == "a":
            print("정방향")
            ser.write(b'a')
        elif cmd == "s":
            print("역방향")
            ser.write(b's')
        elif cmd == "q":
            print("프로그램 종료")
            break
        


flash()
ser.close()
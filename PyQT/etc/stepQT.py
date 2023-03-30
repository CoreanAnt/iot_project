import serial
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

# 시리얼 포트와 baud rate 지정
ser = serial.Serial('/dev/ttyS0', 9600)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        # 버튼 생성
        btn_forward = QPushButton('정방향', self)
        btn_forward.move(50, 50)
        btn_forward.clicked.connect(self.forward)

        btn_reverse = QPushButton('역방향', self)
        btn_reverse.move(50, 100)
        btn_reverse.clicked.connect(self.reverse)

        btn_quit = QPushButton('종료', self)
        btn_quit.move(50, 150)
        btn_quit.clicked.connect(self.quit)

        # 윈도우 크기와 제목 설정
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle('제어')

    def forward(self):
        print("정방향")
        ser.write(b'a')

    def reverse(self):
        print("역방향")
        ser.write(b's')

    def quit(self):
        print("프로그램 종료")
        ser.close()
        qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

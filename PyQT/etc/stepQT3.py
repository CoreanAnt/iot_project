import serial
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout

ser = serial.Serial('/dev/ttyS0', 9600)

pulse_width = 50
forward = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 버튼 생성
        btn_forward = QPushButton(QIcon.fromTheme("media-skip-backward"), "", self)
        btn_forward.clicked.connect(self.forward)

        btn_reverse = QPushButton(QIcon.fromTheme("media-skip-forward"), "", self)
        btn_reverse.clicked.connect(self.reverse)

        btn_quit = QPushButton(QIcon.fromTheme("application-exit"), "", self)
        btn_quit.clicked.connect(self.quit)

        # 수평 박스 레이아웃 생성
        hbox = QHBoxLayout()
        hbox.addWidget(btn_forward)
        hbox.addWidget(btn_reverse)
        hbox.addWidget(btn_quit)

        # 윈도우 설정
        window = QWidget()
        window.setLayout(hbox)
        self.setCentralWidget(window)
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle('제어')

    def forward(self):
        print("정방향")
        ser.write(b'a')
        condition = pulse_width > 0 and forward == True

    def reverse(self):
        print("역방향")
        ser.write(b's')
        condition = pulse_width > 0 and forward == False

    def quit(self):
        print("프로그램 종료")
        ser.close()
        qApp.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


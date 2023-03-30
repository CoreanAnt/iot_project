import serial
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QCoreApplication, QEventLoop, QEvent

# 시리얼 포트와 baud rate 지정
ser = serial.Serial('/dev/ttyS0', 9600)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 버튼 생성
        btn_forward = QPushButton(QIcon("forward.png"), "<", self)
        btn_forward.setIconSize(btn_forward.size())
        btn_forward.setStyleSheet("QPushButton {"
                                  "background-color: #f5f5f5;"
                                  "border-style: outset;"
                                  "border-width: 1px;"
                                  "border-radius: 3px;"
                                  "border-color: beige;"
                                  "font: bold 14px;"
                                  "padding: 6px;"
                                  "}")
        btn_forward.clicked.connect(self.forward)

        btn_reverse = QPushButton(QIcon("reverse.png"), ">", self)
        btn_reverse.setIconSize(btn_reverse.size())
        btn_reverse.setStyleSheet("QPushButton {"
                                  "background-color: #f5f5f5;"
                                  "border-style: outset;"
                                  "border-width: 1px;"
                                  "border-radius: 3px;"
                                  "border-color: beige;"
                                  "font: bold 14px;"
                                  "padding: 6px;"
                                  "}")
        btn_reverse.clicked.connect(self.reverse)

        btn_quit = QPushButton(QIcon("quit.png"), "종료", self)
        btn_quit.setIconSize(btn_quit.size())
        btn_quit.setStyleSheet("QPushButton {"
                                "background-color: #f5f5f5;"
                                "border-style: outset;"
                                "border-width: 1px;"
                                "border-radius: 3px;"
                                "border-color: beige;"
                                "font: bold 14px;"
                                "padding: 6px;"
                                "}")
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

    def reverse(self):
        print("역방향")
        ser.write(b's')

    def quit(self):
        print("프로그램 종료")
        ser.close()
        qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set QAudio style
    app.setStyle('QAudioStyle')

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())

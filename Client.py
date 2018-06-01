import socket
import threading
from PyQt5.QtWidgets import QMainWindow,QApplication
import client_ui
import sys


class Client:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect((host, port))
        self.sock.send(b'1')

class  ClientUI(QMainWindow,client_ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)
        self.c = Client('140.138.145.59', 5550)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.changep)
        self.pushButton_3.clicked.connect(self.send)


    def sendThreadFunc(self):

        try:
            myword=self.lineEdit_4.text()
            self.c.sock.send(myword.encode())
        except ConnectionAbortedError:
            print('Server closed this connection!')

        except ConnectionResetError:
            print('Server is closed!')

    def recvThreadFunc(self):
        while True:
            try:
                otherword = self.c.sock.recv(1024) # socket.recv(recv_size)
                self.textBrowser.append(otherword.decode())
                self.textBrowser.update()
            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')

    def login(self):
        text="Welcome to chat room !" + self.lineEdit.text() + "\nNow let\'s chat !"  +  self.lineEdit.text()
        self.textBrowser.append(text)
        self.textBrowser.update()
        self.pushButton.setDisabled(True)
        self.lineEdit.setDisabled(True)
        self.lineEdit_2.setDisabled(True)
        self.pushButton_3.setDisabled(False)

    def send(self):
        mes = " \n                                         " + self.lineEdit_4.text() + ": You"
        self.textBrowser.append(mes)
        self.textBrowser.update()
        th1 = threading.Thread(target=self.sendThreadFunc)
        th1.setDaemon(True)
        th1.start()

    def changep(self):
        mes = " \n                                         " + self.lineEdit.text() + ": You"
        self.textBrowser.append(mes)
        self.textBrowser.update()

def main():
    app=QApplication(sys.argv)
    MainWindow=ClientUI()
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

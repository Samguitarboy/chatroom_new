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
    def sendThreadFunc(self):
        while True:
            try:
                word = self.sock.recv(1024) # socket.recv(recv_size)
                print(word.decode())
            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')

    def recvThreadFunc(self):
        while True:
            try:
                otherword = self.sock.recv(1024) # socket.recv(recv_size)
                print(otherword.decode())
            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')

class Main(QMainWindow,client_ui.Ui_MainWindow,Client):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)
        self.pushButton_2.setText("Send")
        self.pushButton_2.clicked.connect(self.login)
        self.pushButton.clicked.connect(self.send)
    def login(self):
        text="Welcome to chat room !" + self.textEdit.toPlainText() + "\nNow let\'s chat !"  +  self.textEdit.toPlainText()
        self.textBrowser.append(text)
        self.textBrowser.update()
        self.lineEdit.setText("")
        self.pushButton_2.setDisabled(True)
        self.textEdit.setDisabled(True)
        self.pushButton.setDisabled(False)
        self.nickname=self.textEdit.toPlainText()
        #self.sock.send(self.nickname.encode())

    def send(self):
        #self.sock.send(self.lineEdit.text().encode(()))
        mes = " \n                                         " + self.lineEdit.text() + ": You"
        self.textBrowser.append(mes)
        self.textBrowser.update()

def main():
    app=QApplication(sys.argv)
    MainWindow=Main()
    MainWindow.show()
    sys.exit(app.exec_())
    c = Client('140.138.145.59', 5550)
    th1 = threading.Thread(target=c.sendThreadFunc)
    th2 = threading.Thread(target=c.recvThreadFunc)
    threads = [th1, th2]

    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()


if __name__ == "__main__":
    main()

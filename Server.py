# -*- encoding: utf-8 -*-
import socket
import threading
from PyQt5.QtWidgets import QMainWindow,QApplication
import server_ui
import sys
from time import gmtime, strftime


class Server:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.bind((host, port))
        self.sock.listen(5)
        print('Server', socket.gethostbyname(host), 'listening ...')
        self.mylist = list()
        self.people=0
    def checkConnection(self):
        connection, addr = self.sock.accept()
        print('Accept a new connection', connection.getsockname(), connection.fileno())

        try:
            buf = connection.recv(1024).decode()
            if buf == '1':
                # start a thread for new connection
                mythread = threading.Thread(target=self.subThreadIn, args=(connection, connection.fileno()))
                mythread.setDaemon(True)
                mythread.start()
                connection.send(b'Welcome to Chat room!')
                connection.send(b'Input your nickname: ' )

            else:
                connection.send(b'please go out!')
                connection.close()
        except:
            pass

    # send whatToSay to every except people in exceptNum
    def tellOthers(self, exceptNum, whatToSay):
        for c in self.mylist:
            if c.fileno() != exceptNum:
                try:
                    c.send((whatToSay+'                 ['+strftime("%T",gmtime())+']').encode())
                except:
                    pass

    def subThreadIn(self, myconnection, connNumber):

        self.mylist.append(myconnection)
        nickname=(myconnection.recv(1024).decode())
        recv =  'SYSTEM: '+nickname+' in the chat room'
        self.tellOthers(connNumber, recv)
        self.people+=1
        self.tellOthers(connNumber, 'Now we have '+str(self.people)+' people!')
        while True:
            try:
                recvedMsg = myconnection.recv(1024).decode()
                if recvedMsg:
                    self.tellOthers(connNumber, recvedMsg)
                else:
                    pass

            except (OSError, ConnectionResetError):
                try:
                    self.mylist.remove(myconnection)
                    leave = nickname + ' is leaving!'
                    self.people-=1
                    self.tellOthers(connNumber, leave)
                    self.tellOthers(connNumber, 'Now we have '+str(self.people)+' people!')
                except:
                    pass

                myconnection.close()
                return


class ServerUI(QMainWindow,server_ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)



def main():
    app=QApplication(sys.argv)
    MainWindow=ServerUI()
    MainWindow.show()
    sys.exit(app.exec_())
    s = Server('140.138.145.59', 5550)
    while True:
        s.checkConnection()


if __name__ == "__main__":
    main()

# -*- encoding: utf-8 -*-
import socket
import threading
from PyQt5.QtWidgets import QMainWindow,QApplication, QLineEdit
import server_ui
import sys
from time import gmtime, strftime
from pymongo import MongoClient

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
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.dbChatRoom = DataBaseChatRoom()
        self.dbChatRoom.collection.delete_many({})
        self.dbChatRoom.Initdatabase()
        self.dbChatRoom.colseClient()
        self.update_textBrowser()
        self.pushButton.clicked.connect(self.add)
    def add(self):
        uname =  self.lineEdit.displayText()
        upwd = self.lineEdit_2.displayText()
        s = {'uname': uname, 'upwd': upwd}
        self.dbChatRoom.collection.insert_one(s)
        self.update_textBrowser()

    def update_textBrowser(self):
        cursor = self.dbChatRoom.collection.find()
        data = [d for d in cursor]
        u = ""
        for i in data:
            u += str(i["uname"]) + ","
        self.textBrowser.setText(u)
class DataBaseChatRoom:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)  # 比较常用
        self.database = self.client["ChatRoom"]  # SQL: Database Name
        self.collection = self.database["user"]  # SQL: Table Name

    def loadData(self):
        pass
        return None

    # delete user by uname
    # dbChatRoom.deleteUser(['A'])
    def deleteUser(self, unameList=None):
        pass
        return 'successful'

    # insert user
    # dbChatRoom.insertUser(uname='A', upwd='A')
    def insertUser(self, uname=None, upwd=None):
        pass
        return 'successful'

    def updataUser(self, uname=None, upwd=None):
        pass
        return 'successful'

    # check checkUserExist
    def checkUserExist(self, uname='A'):
        pass
        return False

    # query user bu uname
    # dbChatRoom.queryByuname(uname='A', upwd='A')
    def queryByuname(self, uname='A', upwd='A'):
        pass
        return False

    # Init database
    # dbChatRoom.Initdatabase()
    def Initdatabase(self):

        userList = []
        userList.append({'uname': 'A', 'upwd': 'A'})
        userList.append({'uname': 'B', 'upwd': 'B'})
        userList.append({'uname': 'C', 'upwd': 'C'})
        userList.append({'uname': 'D', 'upwd': 'D'})
        userList.append({'uname': 'E', 'upwd': 'E'})
        self.collection.insert_many(userList)

    def colseClient(self):
        self.client.close()


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


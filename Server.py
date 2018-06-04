# -*- encoding: utf-8 -*-
import sys
import socket
import threading
from PyQt5.QtWidgets import QMainWindow,QApplication, QLineEdit,QCheckBox
import server_ui
from pymongo import MongoClient

host = 'localhost'
class Server:
    def __init__(self, host, port):
        self.mylist = list()
        self.people = 0
        # 建立socket連線
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.bind((host, 5550))
        self.sock.listen(5)
        print('Server', socket.gethostbyname(host), 'listening ...')

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
                    c.send(whatToSay.encode())
                except:
                    pass

    def subThreadIn(self, myconnection, connNumber):
        self.mylist.append(myconnection)
        nickname = (myconnection.recv(1024).decode())
        self.people += 1
        recv = str(self.people) + 'SYSTEM: ' + nickname + ' in the chat room'
        self.tellOthers(connNumber, recv)

        while True:
            try:
                recvedMsg = str(self.people) + nickname + ': ' + myconnection.recv(1024).decode()
                if recvedMsg:
                    self.tellOthers(connNumber, recvedMsg)
                else:
                    pass

            except (OSError, ConnectionResetError):
                try:
                    self.mylist.remove(myconnection)

                except:
                    pass

                self.people -= 1
                leave = str(self.people) + '[SYSTEM: ' + nickname + ' leave the chat room]'
                self.tellOthers(connNumber, leave)

                myconnection.close()
                return

class ServerUI(QMainWindow,server_ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__,self).__init__()
        # GUI設定好
        self.setupUi(self)
        self.checkboxs = []
        self.checkboxs.append(self.checkBox_2)
        self.checkboxs.append(self.checkBox_3)
        self.checkboxs.append(self.checkBox_4)
        self.checkboxs.append(self.checkBox_5)
        self.checkboxs.append(self.checkBox_6)

        self.dbChatRoom = DataBaseChatRoom()
        self.dbChatRoom.collection.delete_many({})
        self.dbChatRoom.Initdatabase()

        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)
        self.dbChatRoom.closeClient()
        self.setWindowTitle("Chat Application")

    def add(self):
        uname = self.lineEdit.displayText()
        upwd = self.lineEdit_2.text()
        self.dbChatRoom.insertUser(uname,upwd)

        self.checkBox_7 = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_7.setCheckable(True)
        self.vertical.addWidget(self.checkBox_7)
        self.checkBox_7.setText(uname)
        self.checkboxs.append(self.checkBox_7)

    def delete(self):
        deleteList = []
        for bye in self.checkboxs:
            if bye.isChecked():
                self.checkboxs.remove(bye)
                deleteList.append(bye.text())
                self.vertical.removeWidget(bye)
                bye.deleteLater()
                bye = None
        self.dbChatRoom.deleteUser(deleteList)


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
        self.collection.remove(unameList)
        return 'successful'

    # insert user
    # dbChatRoom.insertUser(uname='A', upwd='A')
    def insertUser(self, uname=None, upwd=None):
        self.collection.insert_one({'uname': uname, 'upwd': upwd})
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

    def closeClient(self):
        self.client.close()

def main():
    app=QApplication(sys.argv)
    serverWindow=ServerUI()
    serverWindow.show()
    #s = Server(host, 5550)
    #while True:
        #s.checkConnection()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


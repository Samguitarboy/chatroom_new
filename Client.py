import socket
import threading
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton
from time import strftime
import client_ui
import sys
from pymongo import MongoClient

class  ClientUI(QMainWindow,client_ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__,self).__init__()

        self.dbChatRoom = DataBaseChatRoom()

        #建立socket連線
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect(('localhost', 5550))
        self.sock.send(b'1')
        #GUI設定好
        self.setupUi(self)
        self.setWindowTitle("Chat Application")
        #按按鈕做相應的事件
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.changep)
        self.pushButton_3.clicked.connect(self.send)

        self.dbChatRoom.closeClient()

        #起一個thread做接受訊息
        th2 = threading.Thread(target=self.recvThreadFunc)
        th2.setDaemon(True)
        th2.start()

    #將進入聊天室的名子傳給ser
    def system_notice(self):
       self.sock.send(self.lineEdit.text().encode())


    #client傳訊息給server
    def sendThreadFunc(self):
        try:
            sendtext =  self.lineEdit_4.text()  +'                  ['+strftime("%T")+']'
            self.sock.send(sendtext.encode())

        except ConnectionAbortedError:
            print('Server closed this connection!')
        except ConnectionResetError:
            print('Server is closed!')

    # client接收sevrver傳來的訊息
    def recvThreadFunc(self):
        while True:
            try:
                otherword = self.sock.recv(1024) # socket.recv(recv_size)
                print(otherword.decode())
                self.label_4.setText(otherword.decode()[0:1])
                self.textBrowser.append(otherword.decode()[1:])
                self.textBrowser.update()

            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')

    #login鈕按下去，檢查資料是否存在，並打招呼(login那排鎖起來，send鈕變正常)
    def login(self):
        text="Welcome to chat room !" + self.lineEdit.text() + "\nNow let\'s chat !"  +  self.lineEdit.text()
        self.textBrowser.append(text)
        self.textBrowser.update()

        name = self.dbChatRoom.collection.find_one({'uname' : self.lineEdit.text()})
        print(name['upwd'])
        if name['upwd'] == self.lineEdit_2.text():
            #傳給server名子
            th2 = threading.Thread(target=self.system_notice)
            th2.setDaemon(True)
            th2.start()

            self.label_4.setText('1')
            self.pushButton.setDisabled(True)
            self.lineEdit.setDisabled(True)
            self.lineEdit_2.setDisabled(True)
            self.pushButton_3.setDisabled(False)

        else:
            warning = "Wrong Password!"
            self.textBrowser.append(warning)
            self.textBrowser.update()
            self.pushButton.setDisabled(True)
            self.lineEdit.setDisabled(True)
            self.lineEdit_2.setDisabled(True)
            self.lineEdit_3.setDisabled(True)
            self.pushButton_2.setDisabled(True)

    # send鈕按下去，在自己視窗顯示mes，而另起一個thread傳我傳的訊息給server
    def send(self):
        mes = " \n                                             " + self.lineEdit_4.text() + ": You"
        self.textBrowser.append(mes)
        self.textBrowser.update()

        th1 = threading.Thread(target=self.sendThreadFunc)
        th1.setDaemon(True)
        th1.start()

    def changep(self):
        new_pwd = self.lineEdit_3.text()
        self.dbChatRoom.updataUser(self.lineEdit.text(),new_pwd)

class DataBaseChatRoom:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)  # 比较常用
        self.database = self.client["ChatRoom"]  # SQL: Database Name
        self.collection = self.database["user"]  # SQL: Table Name

    def updataUser(self, uname=None, upwd=None):
        self.collection.update_one({"uname": uname}, {"$set": {"upwd": upwd}})
        return 'successful'

    def closeClient(self):
        self.client.close()

def main():
    app=QApplication(sys.argv)
    clientWindow=ClientUI()
    clientWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

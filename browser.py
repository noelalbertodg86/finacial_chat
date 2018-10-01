import sys
import threading
import traceback

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QListView, QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextItem

from client import Client

class App(QMainWindow):

        def __init__(self, user_, userId_):
            try:
                super().__init__()
                self.client_ = Client(user_, userId_)
                self.user = user_
                self.title = user_ + ': welcome to financial chat room'
                self.userId = userId_
                self.left = 0
                self.top = 0
                self.width = 440
                self.height = 650
                self.initUI()
                self.count_messages = 0
                ithread = threading.Thread(target=self.reciveMessage)
                ithread.daemon = True
                ithread.start()
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
                print('Error starting Browers: %s' % (error))

        def initUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            self.view = QListView(self)
            self.view.move(15, 15)
            self.view.resize(400, 580)
            self.model = QStandardItemModel()


            self.user_message = QLineEdit(self)
            self.user_message.move(30, 610)
            self.user_message.resize(280, 30)
            self.user_message.setPlaceholderText('write a message')

            self.button =QPushButton('Send', self)
            self.button.move(320, 610)
            self.button.resize(40,30)
            self.button.clicked.connect(self.on_click)
            self.show()

        def on_click(self):
            try:
                self.show_in_chatbox(self.user_message.text())
                self.client_.sendMessage_to_chatroom(self.user_message.text())
                self.user_message.clear()
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
                print('**** ERROR %s' % error)

        def reciveMessage(self):
            while True:
                try:
                    print('Browers reciveMessage start...')
                    resul = self.client_.reciveMessage_from_chatroom()
                    print('Browers reciveMessage got something...')

                    if resul is not None:
                        self.show_in_chatbox(str(resul))
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
                    print('** ERROR: %s' % error)

        def show_in_chatbox(self, message):
            self.count_messages += 1
            if self.count_messages > 50:
                self.model.removeRow(0)
            self.model.appendRow(QStandardItem(message))
            self.model.appendRow(QStandardItem('--------------'))
            self.view.setModel(self.model)

# if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # ex = App('noel', 1)
    # sys.exit(app.exec_())
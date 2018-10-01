import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QMessageBox
from PyQt5 import QtGui

from utilities import userdb
from Model.userModel import user

class Login(QMainWindow):
        def __init__(self):
            super().__init__()
            self.title = 'Welcome to financial Chat'
            self.left = 0
            self.top = 0
            self.width = 400
            self.height = 140
            self.userObject = user()
            self.initUI()

        def initUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left,self.top,self.width,self.height)

            self.user = QLineEdit(self)
            self.user.move(30, 30)
            self.user.resize(280, 20)
            self.user.setPlaceholderText('user')

            self.password=QLineEdit(self)
            self.password.move(30, 55)
            self.password.resize(280, 20)
            self.password.setPlaceholderText('pass')
            self.password.setEchoMode(QLineEdit.Password)



            self.button=QPushButton('Login',self)
            self.button.move(30, 85)
            self.button.clicked.connect(self.on_click)
            self.show()

        def on_click(self):
            try:
                login_ok = False
                userData = self.userObject.userLogin({'user': self.user.text(), 'pass': self.password.text()})
                if userData:
                    login_ok = True
                    from browser import App
                    app = App(self.user.text(),userData[0][2])
                if login_ok:
                    self.hide()
                else:
                    QMessageBox.question(self, 'Error', "Incorrect user or password ", QMessageBox.Ok, QMessageBox.Ok)

            except Exception as e:
                print('Error: %s' % e.args[0])

login = QApplication(sys.argv)
ex = Login()
sys.exit(login.exec_())
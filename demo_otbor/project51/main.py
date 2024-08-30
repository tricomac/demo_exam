from PyQt5 import QtWidgets, QtCore
import sys



class AuthorisationForm(QtWidgets.QMainWindow):
	
    def __init__(self):
        super().__init__()
        self.setObjectName("self")
        self.resize(800, 600)
        self.setStyleSheet("background-color:rgb(210,210,210);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 60, 121, 61))
        self.label.setStyleSheet("color:rgb(0,0,0);font:16pt \"Arial\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 130, 121, 61))
        self.label_2.setStyleSheet("color:rgb(0,0,0);font:16pt \"Arial\";")
        self.label_2.setObjectName("label_2")
        self.button_quit = QtWidgets.QPushButton(self.centralwidget)
        self.button_quit.setGeometry(QtCore.QRect(10, 500, 120, 80))
        self.button_quit.setStyleSheet("background-color:rgb(255,255,255);color:rgb(0,0,0);font:16pt \"Arial\";")
        self.button_quit.setObjectName("button_quit")
        self.button_enter = QtWidgets.QPushButton(self.centralwidget)
        self.button_enter.setGeometry(QtCore.QRect(340, 350, 120, 80))
        self.button_enter.setStyleSheet("background-color:rgb(255,255,255);color:rgb(0,0,0);font:16pt \"Arial\";")
        self.button_enter.setObjectName("button_enter")
        self.lineEdit_login = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_login.setGeometry(QtCore.QRect(230, 70, 401, 41))
        self.lineEdit_login.setStyleSheet("background-color:rgb(255,255,255);color:rgb(0,0,0);font:16pt \"Arial\";")
        self.lineEdit_login.setObjectName("lineEdit_login")
        self.lineEdit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_password.setGeometry(QtCore.QRect(230, 140, 401, 41))
        self.lineEdit_password.setStyleSheet("background-color:rgb(255,255,255);color:rgb(0,0,0);font:16pt \"Arial\";")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Окно авторизации"))
        self.label.setText(_translate("self", "Логин:"))
        self.label_2.setText(_translate("self", "Пароль:"))
        self.button_quit.setText(_translate("self", "ВЫХОД"))
        self.button_enter.setText(_translate("self", "Войти"))
        self.label.adjustSize()
        self.label_2.adjustSize()
        self.button_enter.clicked.connect(lambda: self.authorise())
        self.button_quit.clicked.connect(lambda: self.closeEvent(None))
        self.show()

    def authorise(self):
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        if login == "Usr" and password == "123":
            self.destroy()
            self = NextWindow(self)

    def closeEvent(self, event):
        sys.exit()

class NextWindow(QtWidgets.QMainWindow):
    def __init__(self, other: AuthorisationForm):
        super().__init__()
        self.other = other
        self.setObjectName("self")
        self.resize(800, 600)
        self.setStyleSheet("background-color: rgb(210,210,210);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.button_quit = QtWidgets.QPushButton(self.centralwidget)
        self.button_quit.setGeometry(QtCore.QRect(10, 582, 43, 24))
        self.button_quit.setText("")
        self.button_quit.setObjectName("button_quit")
        self.setCentralWidget(self.centralwidget)

        self.button_quit.hide()
        self.button_quit.clicked.connect(lambda: self.closeEvent(None))
        self.show()
    def closeEvent(self, event):
        sys.exit()

if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    window = AuthorisationForm()
    sys.exit(application.exec_())
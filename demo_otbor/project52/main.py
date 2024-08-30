from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os


class User:
    def __init__(self, arga : list):
            self.name = (arga[0])
            self.login = (arga[1])
            self.password = (arga[2])

    def convert_to_CSVstring(self):
        return f"{self.name};{self.login};{self.password}\n"

def writeLastUser(user : User):
    with open(os.path.join(os.path.abspath(os.getcwd()),"last_user.txt"), 'w', encoding = "utf8") as file:
        file.write(user.convert_to_CSVstring())
        
def get_authData():
    users = dict()
    with open(os.path.join(os.path.abspath(os.getcwd()),"data.csv"), 'r', encoding="utf8") as file:

        last_char = ''
        file.readline()
        for line in file:
            current_line = line.strip().split(';')
            current_user = User(current_line)
            users[current_user.login] = current_user
            last_char = line[-1]
    if last_char != '\n':
        with open(os.path.join(os.path.abspath(os.getcwd()),"data.csv"), 'a', encoding="utf8") as file:
            file.write('\n')
    return users

def change_user_data(login : str, data : str):
    file_data = str()
    with open(os.path.join(os.path.abspath(os.getcwd()),"data.csv"), 'r', encoding="utf8") as file:
        for line in file:
            if line.strip().split(';')[1] == login:
                line = line.replace(line, data)
            file_data += line
        if file_data[-1]!='\n':
            file_data += '\n'
    with open(os.path.join(os.path.abspath(os.getcwd()),"data.csv"), 'w', encoding="utf8") as file:
        file.write(file_data)

def new_user(data : str):
    with open(os.path.join(os.path.abspath(os.getcwd()),"data.csv"), 'a', encoding="utf8") as file:
        file.write(data)

def throw_error(description : str):
    msg = QtWidgets.QMessageBox()
    msg.setStyleSheet(
        "background-color: rgb(210, 0, 0);"+
        "color: rgb(0,0,0);"+
        "font: 18pt \"Arial\";"
    )
    msg.setText(description)
    msg.exec_()

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
        self.button_quit.setGeometry(QtCore.QRect(10, 512, 111, 71))
        self.button_quit.setStyleSheet("background-color:rgb(255,255,255);color:rgb(0,0,0);font:16pt \"Arial\";")
        self.button_quit.setObjectName("button_quit")
        self.button_enter = QtWidgets.QPushButton(self.centralwidget)
        self.button_enter.setGeometry(QtCore.QRect(300, 270, 161, 71))
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
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(270, 220, 241, 41))
        self.checkBox.setStyleSheet("font:16pt \"Arial\";")
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Окно авторизации"))
        self.label.setText(_translate("self", "Логин:"))
        self.label_2.setText(_translate("self", "Пароль:"))
        self.button_quit.setText(_translate("self", "ВЫХОД"))
        self.button_enter.setText(_translate("self", "Войти"))
        self.checkBox.setText(_translate("self", "Запомнить меня"))


        ##################################

        self.label.adjustSize()
        self.label_2.adjustSize()
        self.button_enter.clicked.connect(lambda: self.authorise())
        self.button_quit.clicked.connect(lambda: self.closeEvent(None))

        self.users = get_authData()
        with open(os.path.join(os.path.abspath(os.getcwd()),"last_user.txt"), 'r') as file:
            line = file.readline().strip()
            if (line != ''):
                log_pass = line.split(';')
                self.lineEdit_login.setText(log_pass[1])
                self.lineEdit_password.setText(log_pass[2])
        self.show()

    def authorise(self):
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        if login in self.users.keys():
            if password == self.users[login].password:
                if self.checkBox.isChecked():
                    writeLastUser(self.users[login])
                self.destroy()
                self = NextWindow(self)
            else:
                throw_error("НЕВЕРНЫЙ ПАРОЛЬ!")
        else:
            throw_error("НЕВЕРНЫЙ ЛОГИН!")

    def closeEvent(self, event):
        sys.exit()

class NextWindow(QtWidgets.QMainWindow):
    def __init__(self, other: AuthorisationForm):
        super().__init__()
        self.other = other
        self.setObjectName("self")
        self.resize(1000, 600)
        self.setStyleSheet("background-color:rgb(210,210,210);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 981, 431))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("background-color: rgb(255,255,255);")
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setItem(0, 2, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.button_quit = QtWidgets.QPushButton(self.centralwidget)
        self.button_quit.setGeometry(QtCore.QRect(20, 520, 141, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.button_quit.setFont(font)
        self.button_quit.setStyleSheet("background-color: rgb(255,255,255);color:rgb(0,0,0);")
        self.button_quit.setObjectName("button_quit")
        self.button_add = QtWidgets.QPushButton(self.centralwidget)
        self.button_add.setGeometry(QtCore.QRect(10, 450, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.button_add.setFont(font)
        self.button_add.setStyleSheet("background-color: rgb(255,255,255);color:rgb(0,0,0);")
        self.button_add.setObjectName("button_add")
        self.button_change = QtWidgets.QPushButton(self.centralwidget)
        self.button_change.setGeometry(QtCore.QRect(220, 450, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.button_change.setFont(font)
        self.button_change.setStyleSheet("background-color: rgb(255,255,255);color:rgb(0,0,0);")
        self.button_change.setObjectName("button_change")
        self.button_delete = QtWidgets.QPushButton(self.centralwidget)
        self.button_delete.setGeometry(QtCore.QRect(430, 450, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.button_delete.setFont(font)
        self.button_delete.setStyleSheet("background-color: rgb(255,255,255);color:rgb(0,0,0);")
        self.button_delete.setObjectName("button_delete")
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Второе окно"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("self", "Имя сотрудника"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("self", "Логин"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("self", "Пароль"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.button_quit.setText(_translate("self", "НАЗАД"))
        self.button_add.setText(_translate("self", "Добавить"))
        self.button_change.setText(_translate("self", "Изменить"))
        self.button_delete.setText(_translate("self", "Удалить"))

        self.fnt = QtGui.QFont("Arial")
        self.fnt.setPointSize(18)
        self.black = QtGui.QColor(0,0,0)
        self.old_logins = set()

        with open(os.path.join(os.path.abspath(os.getcwd()),"data.csv"), 'r', encoding="utf8") as file:
            i = 1
            file.readline()
            for line in file:
                self.tableWidget.setRowCount(i + 1)
                current = line.strip().split(';')
                for j in range(3):
                    item = QtWidgets.QTableWidgetItem()
                    item.setForeground(self.black)
                    item.setFont(self.fnt)
                    item.setText(current[j])
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableWidget.setItem(i, j, item)
                    if i == 1:
                        self.tableWidget.setColumnWidth(j, self.tableWidget.width() // 3 - 1)
                    elif j == 1:
                        self.old_logins.add(current[j])

                i += 1
        
        self.button_add.clicked.connect(lambda: self.click_button_add())
        self.button_change.clicked.connect(lambda: self.click_button_change())
        self.button_delete.clicked.connect(lambda: self.click_button_delete())
        self.button_quit.clicked.connect(lambda: self.closeEvent(None))

        self.show()

    def click_button_add(self):
        pass

    def click_button_change(self):
        pass

    def click_button_delete(self):
        pass
            
    def closeEvent(self, event):
        self.destroy()
        self = AuthorisationForm()

if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    window = AuthorisationForm()
    sys.exit(application.exec_())

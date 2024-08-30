from PyQt5 import QtWidgets, QtGui, QtCore, QtChart, QtMultimedia
from PyQt5.QtGui import QCloseEvent
from PyQt5.uic import loadUi
import sys
import time as tm
from random import randint
import os

class User:
    def __init__(self, arga : list):
        try:
            self.id = int(arga[0])
            self.login = (arga[1])
            self.password = (arga[2])
            self.role = (arga[3])
            self.name = (arga[4])
            self.results = int(arga[5])
            self.valid = True
        except ValueError:
            self.valid = False
    def convert_to_CSVstring(self):
        return f"{self.id},{self.login},{self.password},{self.role},{self.name},{self.results}\n"

def get_authData():
    users = dict()
    with open("users.csv", 'r') as file:
        last_char = ''
        file.readline()
        for line in file:
            current_line = line.strip().split(',')
            last_char = line[-1]
            current_user = User(current_line)
            users[current_user.login] = current_user
    if last_char != '\n':
        with open("users.csv", 'a') as file:
            file.write('\n')
    with open("orders.csv", 'r') as file:
        last_char = file.readlines()[-1][-1]
    if last_char != '\n':
        with open("orders.csv", 'a') as file:
            file.write('\n')
    return users

def renew_users_data(data : str, old_id : int):
    file_data = str()
    with open("users.csv", 'r') as file:
        for line in file:
            if line.strip().split(',')[0] == str(old_id):
                line = line.replace(line, data)
            file_data += line
    with open("users.csv", 'w') as file:
        file.write(file_data)

def new_user(data : str):
    with open("users.csv", 'a') as file:
        file.write(data)

class AuthorisationForm(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        loadUi("AuthorisationForm.ui", self)
        self.button_quit.clicked.connect(lambda: self.closeEvent())
        self.button_authorise.clicked.connect(lambda: self.authorise())
        self.button_register.clicked.connect(lambda: self.registration())
        self.users = get_authData()
        self.show()

    def throw_error(self, description : str):
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet(
            "background-color: rgb(210, 0, 0);"+
            "color: rgb(0,0,0);"+
            "font: 18pt \"Arial\";"
        )
        msg.setText(description)
        msg.exec_()

    def authorise(self):
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        if login in self.users.keys():
            if self.users[login].password == password: 
                self.user = self.users[login]
                self.destroy()
                if self.user.role.lower() == "директор":
                    self = DirectorWindow(self)
                elif self.user.role.lower() == "администратор":
                    self = AdminWindow(self)
                elif self.user.role.lower() == "работник":
                    self = WorkerWindow(self)
                else:
                    self.throw_error("У Вашей роли нет рабочего окна.")
                    self.closeEvent()
            else:
                self.throw_error("Неверный пароль!")
        else:
            self.throw_error("Неверный логин!")


    def registration(self):
        self = RegistrationForm()

    def closeEvent(self):
        sys.exit()

class RegistrationForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("RegistrationForm.ui", self)
        self.button_quit.clicked.connect(lambda: self.closeEvent())
        self.button_enter.clicked.connect(lambda: self.registration())
        self.users = get_authData()
        self.show()

    def throw_error(self, description : str):
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet(
            "background-color: rgb(210, 0, 0);"+
            "color: rgb(0,0,0);"+
            "font: 18pt \"Arial\";"
        )
        msg.setText(description)
        msg.exec_()

    def registration(self):
        with open("waiting for assignment.txt", "a") as file:
            file.write(
                self.lineEdit_name.text() + ' ' +
                self.comboBox.currentText().lower() + '\n'
            )
        self.closeEvent()

    def closeEvent(self):
        self.destroy()
        self = AuthorisationForm()

class DirectorWindow(QtWidgets.QMainWindow):
    def __init__(self, other : AuthorisationForm):
        super().__init__()
        loadUi("DirectorWindow.ui", self)
        self.button_quit.clicked.connect(lambda: self.closeEvent())
        self.button_openPlayer.clicked.connect(lambda: self.openPlayer())
        self.other = other
        self.users = other.users
        self.fnt = QtGui.QFont("Arial")
        self.fnt.setPointSize(18)
        self.color = QtGui.QColor(0,0,0)
        chart = QtChart.QChart()
        chart.setTheme(QtChart.QChart.ChartTheme.ChartThemeHighContrast)
        
        ids_list = list()
        min_res = 2 ** 63
        max_res = -(min_res)
        i = 1
        for k in self.users.keys():
            if self.users[k].role == "работник":
                self.tableWidget.setRowCount(i + 1)
                current_user = [self.users[k].id, self.users[k].name, self.users[k].results]
                for j in range(3):
                    if i == 1:
                        self.tableWidget.setColumnWidth(j,253)
                    item = QtWidgets.QTableWidgetItem()
                    item.setForeground(self.color)
                    item.setFont(self.fnt)
                    item.setText(str(current_user[j]))
                    self.tableWidget.setItem(i, j, item)
                i += 1
                ids_list.append(str(self.users[k].id))
                if self.users[k].results < min_res:
                    min_res = self.users[k].results
                elif self.users[k].results > max_res:
                    max_res = self.users[k].results
                set0 = QtChart.QBarSet(str(self.users[k].id))
                set0 << self.users[k].results
                series = QtChart.QBarSeries()
                series.append(set0)
                chart.addSeries(series)
        
        X = QtChart.QBarCategoryAxis()
        X.setCategories(ids_list)
        Y = QtChart.QValueAxis()
        Y.setRange(min_res, max_res)

        chart.createDefaultAxes()
        chart.setAxisX(X)
        chart.setAxisY(Y)
        chart.legend().hide()
        chart.setTitle("Результаты работников")

        self.chartView = QtChart.QChartView(self)
        self.chartView.setChart(chart)
        self.chartView.setGeometry(
            780, 10,
            620, 471
        )

        self.show()
    def openPlayer(self):
        self.destroy()
        self = Player(self)
    def closeEvent(self):
        self.destroy()
        self = self.other
        self.__init__()
        


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, other : AuthorisationForm):
        super().__init__()
        loadUi("AdminWindow.ui",self)
        self.other = other
        self.user = other.user
        self.old_ids = set()
        self.old_logins = set()
        self.fnt = QtGui.QFont("Arial")
        self.fnt.setPointSize(18)
        self.black = QtGui.QColor(0,0,0)

        loadUi("AdminWindow.ui", self)
        self.button_add.clicked.connect(lambda: self.click_button_add())
        self.button_renew.clicked.connect(lambda: self.click_button_renew())
        self.button_delete.clicked.connect(lambda: self.click_button_delete())
        self.button_quit.clicked.connect(lambda: self.closeEvent())
        with open("users.csv", 'r') as file:
            i = 0
            for line in file:
                self.tableWidget.setRowCount(i + 1)
                current = line.strip().split(',')
                for j in range(5):
                    if i == 0:
                        self.tableWidget.setColumnWidth(j, self.tableWidget.width() // 5 - 1)
                    elif j == 0:
                        self.old_ids.add(int(current[j]))
                    elif j == 1:
                        self.old_logins.add(str(current[j]))   
                    item = QtWidgets.QTableWidgetItem()
                    item.setForeground(self.black)
                    item.setFont(self.fnt)
                    item.setText(current[j])
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableWidget.setItem(i,j,item)
                i += 1
        self.show()
    def throw_error(self,description:str):
        msg = QtWidgets.QMessageBox()
        msg.styleSheet(
            "background-color: rgb(210,0,0);"
            "color: rgb(0,0,0);"
            "font: 18pt \"Arial\";"
        )
        msg.setText(description)
        msg.exec_()
    def click_button_delete(self):
        items = self.tableWidget.selectedItems()
        if len(items) == 0:
            self.throw_error("Вы не выбрали пользователя,\nданные которого хотите изменить!")
            return
        self.destroy()
        row = items[0].row()
        renew_users_data('',int(self.tableWidget.item(row,0).text()))
        self.__init__(self.other)
    def click_button_renew(self):
        items = self.tableWidget.selectedItems()
        if len(items) == 0:
            self.throw_error("Вы не выбрали пользователя,\nданные которого хотите изменить!")
            return
        row = items[0].row()
        self.destroy()
        self = ChangeForm(self, 
                          int(self.tableWidget.item(row,0).text()),
                          str(self.tableWidget.item(row,1).text())
                          )
    def click_button_add(self):
        self.destroy()
        self = AddForm(self)

    def closeEvent(self) -> None:
        self.destroy()
        self = self.other
        self.__init__()

class AddForm(QtWidgets.QMainWindow):
    def __init__(self, other : AdminWindow):
        super().__init__()
        self.other = other
        self.old_logins = other.old_logins
        self.old_ids = other.old_ids
        loadUi("TableForm.ui", self)
        self.button_enter.clicked.connect(lambda: self.click_button_enter())
        self.button_quit.clicked.connect(lambda: self.closeEvent())
        self.show()

    def throw_error(self,description:str):
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet(
            "background-color: rgb(210,0,0);"+
            "color: rgb(0,0,0);"+
            "font: 18pt \"Arial\";"
        )
        msg.setText(description)
        msg.exec_()

    def click_button_enter(self):
        try:
            new_id = int(self.lineEdit_id.text())
            # with open("./waiting for assignment.txt", 'r') as file:
            #     real_user = False
            #     for line in file:
            #         if line.strip() == new_name:
            #             real_user = True
            new_login = self.lineEdit_login.text()
            new_password = self.lineEdit_password.text()
            new_role = self.comboBox_role.currentText().lower()
            new_name = self.lineEdit_name.text()
            new_results = 0
            if new_id in self.old_ids or new_login in self.old_logins:
                raise ValueError()
            user = User([new_id,new_login,new_password,new_role,new_name,new_results])
            if not user.valid:
                raise ValueError()
        except ValueError:
            self.throw_error("Неверные данные пользователя!")
            return
        new_user(user.convert_to_CSVstring())
        self.closeEvent()

    def closeEvent(self):
        self.destroy()
        self = self.other
        self.__init__(self.other)

class ChangeForm(AddForm):
    def __init__(self, other: AdminWindow, old_id : int, old_login : str):
        super().__init__(other)
        self.old_id = old_id
        self.old_login = old_login

    def click_button_enter(self):
        try:
            new_id = int(self.lineEdit_id.text())
            new_login = self.lineEdit_login.text()
            new_password = self.lineEdit_password.text()
            new_role = self.comboBox_role.currentText().lower()
            new_name = self.lineEdit_name.text()
            new_results = 0
            if (new_id in self.old_ids and not new_id == self.old_id) or (
                new_login in self.old_logins and not new_login == self.old_login):
                raise ValueError()
            user = User([new_id,new_login,new_password,new_role,new_name,new_results])
            if not user.valid:
                raise ValueError()
        except ValueError:
            self.throw_error("Неверные данные пользователя!")
            return
        renew_users_data(user.convert_to_CSVstring(), self.old_id)
        self.closeEvent()


class WorkerWindow(QtWidgets.QMainWindow):
    
    def __init__(self, other: AuthorisationForm):
        super().__init__()
        self.other = other
        self.user = other.user
        self.directory = self.user.name
        loadUi("WorkerWindow.ui", self)
        self.show()
        self.button_enter.clicked.connect(lambda: self.save_file())
        self.button_quit.clicked.connect(lambda: self.closeEvent())
        self.button_openPlayer.clicked.connect(lambda: self.openPlayer())
        self.tasks = list()
        with open("tasks.txt",'r') as file:
            for line in file:
                self.tasks.append(line.strip())

        self.set_label_greetings()
        self.set_label_task()
        self.show()

    def set_label_task(self):
        self.label_task.setText(self.tasks[randint(0, len(self.tasks) - 1)])

    def set_label_greetings(self):
        self.label_greetings.setText(f"Добро пожаловать, {self.user.name}! Ваш результат: {self.user.results}")

    def save_file(self):
        self.user.results += 1
        try:
            open(f"./{self.directory}")
        except IsADirectoryError:
            pass
        except FileNotFoundError:
            self.directory = ('_').join(self.user.name.split(' '))
            os.system(f"mkdir . {self.directory}")
        with open(f"./{self.directory}/FILE {self.user.results}.txt", 'w') as file:
            file.write(f"{self.label_task.text()}\n{self.textEdit.toPlainText()}\n")
        self.set_label_greetings()
        self.set_label_task()
        self.textEdit.setText('')
        renew_users_data(self.user.convert_to_CSVstring(), self.user.id)
    
    def openPlayer(self):
        self.destroy()
        self = Player(self)


    def closeEvent(self) -> None:
        self.destroy()
        self = self.other
        self.__init__()

class Player(QtWidgets.QMainWindow):
    def __init__(self, other : WorkerWindow | DirectorWindow):
        super().__init__()
        self.other = other
        loadUi("Player.ui", self)
        self.player = QtMultimedia.QMediaPlayer()
        self.button_quit.clicked.connect(lambda: self.closeEvent())
        self.pushButton.clicked.connect(lambda:self.playAudio())
        self.button_up.clicked.connect(lambda:self.addVolume(10))
        self.button_down.clicked.connect(lambda:self.addVolume(-10))
        self.button_pause.clicked.connect(lambda:self.pauseAudio())
        self.button_play.clicked.connect(lambda:self.resumeAudio())

        self.show()

    def addVolume(self, delta : int):
        vol = self.player.volume() + delta
        if vol < 0:
            vol = 0
        elif vol > 100:
            vol = 100
        self.player.setVolume(vol)
    
    def pauseAudio(self):
        try:
            self.player.pause()
        except BaseException:
            pass
    
    def resumeAudio(self):
        try:
            self.player.play()
        except BaseException:
            pass    

    def playAudio(self):
        url = QtCore.QUrl.fromLocalFile(os.path.abspath("music/banger.wav"))
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def closeEvent(self):
        self.destroy()
        self = self.other
        self.__init__(self.other)


if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    window = AuthorisationForm()
    sys.exit(application.exec_())
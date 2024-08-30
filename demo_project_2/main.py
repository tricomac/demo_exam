import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QCloseEvent
from PyQt5.uic import loadUi
import time as tm
import datetime as dt
from math import ceil

class User:
    def __init__(self, arg_array):
        self.name = arg_array[0]
        self.login = arg_array[1]
        self.password = arg_array[2]
        self.role = arg_array[3]

    def convert_to_string(self):
        return f"{self.name},{self.login},{self.password},{self.role}"

def renew_client_in_table(data : str, old_id : str):
    file_data = str()
    with open("table_director.csv", 'r') as file:
        for line in file:
            current = line.strip().split(',')
            if old_id == current[0]:
                line = line.replace(line, data)
            file_data += line
    with open("table_director.csv", 'w') as file:
        file.write(file_data)
    

def add_client_to_table(data : str):
    with open("table_director.csv", 'r') as file:
        file_data = file.read()
    file_data += data
    with open("table_director.csv", 'w') as file:
        file.write(file_data)

def get_users_from_table():
    users = dict()
    last_char = str()

    with open("table_admin.csv", 'r') as file:
        file.readline()
        for line in file:
            current = line.strip().split(',')
            user = User(current)
            users[user.login] = user
            last_char = line[-1]
    if last_char[-1] != '\n':
        with open("table_admin.csv", 'a') as file:
            file.write('\n')

    return users

def get_clients_from_table():
    file_data = list()
    last_char = str()
    with open("table_director.csv", 'r') as file:
        for line in file:
            file_data.append(
                line.strip().split(',')
            )
            last_char = line[-1]
    if last_char[-1] != '\n':
        with open("table_director.csv", 'a') as file:
            file.write('\n')

    return file_data


class AuthorisationForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("authorisationForm.ui", self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.button_quit.clicked.connect(lambda: self.click_button_quit())
        self.button_enter.clicked.connect(lambda: self.click_button_enter())
        self.users = get_users_from_table()
        self.fnt = QtGui.QFont("Arial")
        self.fnt.setPixelSize(18)
        self.color = QtGui.QColor(0,0,0)
        self.show()

    def error(self, type : str):
        msg = QtWidgets.QMessageBox()
        msg.setText(type)
        msg.exec_()

    def click_button_enter(self):
        correct = False
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        try:
            i = 0
            for digit in login:
                int(digit)
                i += 1
            if i != 10:
                int('bruh')

        except ValueError:
            self.error("Неправильный формат логина!")

        if login in self.users.keys():
            user = self.users[login]
            if password == user.password:
                correct = True

        if not correct:
            self.error("Неправильный логин или пароль!")

        else:
            if user.role.lower() == "администратор":
                self.new_window = AdminWindow(self, user)
            elif user.role.lower() == "директор":
                self.new_window = DirectorWindow(self, user)
            else:
                self.error("У Вашей роли нет своего рабочего окна")
            self.destroy()

    def click_button_quit(self):
        sys.exit()

class AdminWindow(QtWidgets.QMainWindow):

    def __init__(self, other : AuthorisationForm, admin : User):
        super().__init__()
        loadUi("administratorWindow.ui", self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.fnt = other.fnt
        self.color = other.color
        self.other = other
        self.users = self.other.users
        self.admin = admin
        self.label.setText(f"Добро пожаловать, {self.admin.name}!")
        self.button_quit.clicked.connect(lambda: self.click_button_quit())

        for i in range(4):
            self.tableWidget.setColumnWidth(i, 195)
        i = 1
        for k in self.users.keys():
            current_user = self.users[k].convert_to_string().split(',')
            self.tableWidget.setRowCount(i + 1)
            for j in range(4):
                item = QtWidgets.QTableWidgetItem()
                item.setFont(self.fnt)
                item.setForeground(self.color)
                item.setText(current_user[j])
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.tableWidget.setItem(i, j, item)
            i += 1
        self.show()
        
    def works(self):
        return self.run
    
    def click_button_quit(self):
        self.run = False

class DirectorWindow(QtWidgets.QMainWindow):
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.click_button_quit()
    def __init__(self, other : AuthorisationForm, director : User):
        super().__init__()
        loadUi("directorWindow.ui", self)
        self.button_add.clicked.connect(lambda: self.click_button_add())
        self.button_renew.clicked.connect(lambda: self.click_button_renew())
        self.button_delete.clicked.connect(lambda: self.click_button_delete())
        self.button_quit.clicked.connect(lambda: self.click_button_quit())
        self.timer = QtCore.QBasicTimer()
        self.fnt = other.fnt
        self.color = other.color
        self.other = other
        self.director = director
        self.table_data = get_clients_from_table()
        self.label.setText(f"Добро пожаловать, {self.director.name}!")
        self.deadlines = list()
        self.used_ids = set()
        #table initing
        self.client_count = len(self.table_data)
        for j in range(5):
            self.tableWidget.setColumnWidth(j,200)
        for i in range(1, self.client_count):
            print('initing')
            self.tableWidget.setRowCount(i + 1)
            for j in range(5 - 1):
                if j == 0:
                    self.used_ids.add(int(self.table_data[i][j]))
                item = QtWidgets.QTableWidgetItem()
                item.setFont(self.fnt)
                item.setForeground(self.color)
                item.setText(self.table_data[i][j])
                self.tableWidget.setItem(i, j, item)                
            self.deadlines.append(self.table_data[i][4])   
        self.show()
        self.timer.start(300,self)

    def timerEvent(self, event):
        if (self.timer.timerId() == event.timerId()):                
            for i in range(self.client_count - 1):
                current_time = tm.time()
                deadline_time = dt.datetime.strptime(f"{self.deadlines[i]} 00:00:00",
                                                    f"%d.%m.%Y %H:%M:%S").timestamp()
                delta_time = ceil(deadline_time - current_time)
                d = 60 * 60 * 24
                
                days_left = delta_time // d
                delta_time -= days_left * d
                d //= 24
                
                hours_left = delta_time // d
                delta_time -= hours_left * d
                d //= 60
                
                minutes_left = delta_time // d
                delta_time -= minutes_left * d
                
                seconds_left = delta_time
                
                item = QtWidgets.QTableWidgetItem()
                item.setFont(self.fnt)
                item.setForeground(self.color)
                item.setText(f"{days_left} {hours_left}:{minutes_left}:{seconds_left}")
                self.tableWidget.setItem(i + 1, 4, item)
            self.update()

    def click_button_add(self):
        self.timer.stop()
        self.destroy()
        self.new_window = AddForm(self)


    def throw_error(self):
        msg = QtWidgets.QMessageBox()
        msg.setText("Неверные данные!")
        msg.exec_()

    def click_button_renew(self):
        self.timer.stop()
        self.destroy()
        items = self.tableWidget.selectedItems()
        if len(items) > 0:
            row = items[0].row()
        else:
            self.throw_error()
        old_id = self.tableWidget.item(row, 0).text()
        self.new_window = RenewForm(self, old_id)

    def click_button_delete(self):
        items = self.tableWidget.selectedItems()
        if len(items) > 0:
            row = items[0].row()
        else:
            self.throw_error()
        old_id = self.tableWidget.item(row, 0).text()
        renew_client_in_table("", old_id)
        self.timer.stop()
        self.destroy()
        self.__init__(self.other,self.director)

    def click_button_quit(self):
        self.timer.stop()
        self.destroy()
        self.other.__init__()

class AddForm(QtWidgets.QMainWindow):
    def __init__(self, other : DirectorWindow):
        super().__init__()
        loadUi("directorForm.ui", self)
        self.button_quit.clicked.connect(lambda: self.click_button_quit())
        self.button_enter.clicked.connect(lambda: self.click_button_enter())
        self.setWindowTitle("Окно добавления заказа")
        self.other = other
        self.show()

    def throw_error(self):
        msg = QtWidgets.QMessageBox()
        msg.setText("Неверные данные!")
        msg.exec_()

    def invalid(self, deadline : str):
        nums = deadline.split('.')
        if nums.__len__() != 3:
            return False
        try:
            day = int(nums[0])
            month = int(nums[1])
            year = int(nums[2])
        except ValueError:
            return False
        if (year < 2024 or day < 1 or month < 1 or month > 12) or (month in set([1,3,5,7,8,10,12]) and day > 31) or (month not in set([1,3,5,7,8,10,12]) and day > 30) or (month == 2 and ((day > 28 and year % 4 != 0) or (year % 4 == 0 and day > 29))):
            return False
        
    def click_button_enter(self):
        try:
            order_id = int(self.lineEdit_id.text())
            product_name = self.lineEdit_name.text()
            quantity = int(self.lineEdit_quantity.text())
            deadline = self.lineEdit_deadline.text()
            if (self.invalid(deadline) or order_id in self.other.used_ids): self.throw_error(); return
            client_name = self.lineEdit_client.text()
        except ValueError:
            self.throw_error()
            return
        order = f"{order_id},{client_name},{product_name},{quantity},{deadline}\n"
        add_client_to_table(order)
        self.click_button_quit()
    
    def click_button_quit(self):
        self.destroy()
        self.other.__init__(self.other.other, self.other.director)

class RenewForm(AddForm):
    def __init__(self, other : DirectorWindow, old_id : str):
        super().__init__(other)
        self.other = other
        self.old_id = old_id
        self.setWindowTitle("Окно изменения заказа")
        self.show()

    def click_button_enter(self):
        try:
            order_id = int(self.lineEdit_id.text())
            product_name = self.lineEdit_name.text()
            quantity = int(self.lineEdit_quantity.text())
            deadline = (self.lineEdit_deadline.text())
            if (self.invalid(deadline) or (order_id in self.other.used_ids and order_id != int(self.old_id))): self.throw_error(); return
            client_name = self.lineEdit_client.text()
        except ValueError:
            self.throw_error()
            return
        order = f"{order_id},{client_name},{product_name},{quantity},{deadline}\n"
        renew_client_in_table(order, self.old_id)
        self.click_button_quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    prog = AuthorisationForm()
    sys.exit(app.exec_())
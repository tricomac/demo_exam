import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtChart
from PyQt5.QtGui import QCloseEvent
from PyQt5.uic import loadUi

class User:
    def __init__(self, arga: list()):
        #  Данный метод принимает значения: self – объект User, arga - список с данными пользователя
        #  Выполняет следующие действия: инициализирует объект User
        #  В качестве результата ничего не возвращает.
        self.id = int(arga[0]) # id пользователя
        self.login = str(arga[1]) # login пользователя
        self.password = str(arga[2]) # password пользователя
        self.role = str(arga[3]) # role пользователя
        self.name = str(arga[4]) # name пользователя
        self.result = int(arga[5]) # result пользователя
    def to_str(self):
        return  f"{self.id},{self.login},{self.password},{self.role},{self.name},{self.result}\n"

def GetDictFromTable():
    users = dict() # dict с данными каждой строки из таблицы
    write_n = False
    with open("Company list.csv", 'r') as file: # Открывает файл для чтения
        file.readline() # читает 1 строку таблицы с заголовками
        for line in file: # Построчно читает файл
            current = line.strip().split(',')
            user = User(current)
            users[current[1]] = user
            if line[-1] != '\n':
                write_n = True
    if write_n:
        with open("Company list.csv", 'a') as file:
            file.write('\n')
    return users 

def RenewDataInTable(user : User):
    data = str()
    with open("Company list.csv", 'r') as file:
        data += file.readline()
        for line in file:
            current = line.strip().split(',')
            if (int(current[0]) == user.id):
                line = line.replace(
                    line, user.to_str()
                )
            data += line
    with open("Company list.csv", 'w') as file:
        file.write(data)

def DeleteUser(user : User):
    data = str()
    with open("Company list.csv", 'r') as file:
        data += file.readline()
        for line in file:
            current = line.strip().split(',')
            if (int(current[0]) == user.id):
                line = ''
            data += line
    with open("Company list.csv", 'w') as file:
        file.write(data)


class AuthorisationForm(QtWidgets.QMainWindow): # Данный класс реализует интерфейс и функционал окна авторизации
    def __init__(self):
        # Данный метод принимает значения: self – объект AuthorisationForm 
        #  Выполняет следующие действия: инициализирует объект AuthorisationForm. 
        #  В качестве результата ничего не возвращает.
        super().__init__() # Вызывание конструктора базового класса
        loadUi("AuthorisationForm.ui", self) # Загружаем интерфейс формы
        self.button_quit.clicked.connect(lambda: self.click_button_quit()) # Связываем нажатие кнопки button_quit с исполнением метода click_button_quit(self)
        self.button_enter.clicked.connect(lambda: self.click_button_enter())# Связываем нажатие кнопки button_enter с исполнением метода click_button_enter(self)
        self.users = GetDictFromTable() # Получает все данные из таблицы # Конвертирует данные в словарь по ключу логина пользователь
        self.main_font = QtGui.QFont("Arial")
        self.main_font.setPixelSize(18)
        self.show() # Показывает форму
        

    def click_button_enter(self):
        comrade = False
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()
        if login in self.users:
            if password == self.users[login].password:
                comrade = True
        
        if comrade:
            user = self.users[login]
            if user.role.lower() == "директор":
                self.next_window = DirectorForm(user, self.users, self)

            elif user.role.lower() == "администратор":
                self.next_window = AdminForm(user, self)

            elif user.role.lower() == "работник":
                self.next_window = WorkerForm(user, self)

            else: # у такой профессии нет своего окна
                error_message = QtWidgets.QMessageBox()
                error_message.setStyleSheet(
                    "background-color: rgb(255,255,255);"+
                    "color:rgb(0,0,0);"+
                    "font:18pt \"Arial\";"
                )
                error_message.setText("У вашей роли нет рабочего окна!")
                sys.exit(error_message.exec_())

            self.destroy()
        else:
            error_message = QtWidgets.QMessageBox()
            error_message.setStyleSheet(
                "background-color: rgb(255,255,255);"+
                "color:rgb(0,0,0);"+
                "font:18pt \"Arial\";"
            )
            error_message.setText("Неверный логин или пароль!")
            error_message.exec_()

    def click_button_quit(self):
        # Данный метод принимает значения: self – объект AuthorisationForm 
        #  Выполняет следующие действия: завершает выполнение программы. 
        #  В качестве результата ничего не возвращает.
        sys.exit()
    
class WorkerForm(QtWidgets.QMainWindow):
    def __init__(self, worker: User, other : AuthorisationForm):
        super().__init__()
        loadUi("WorkerForm.ui",self)
        self.other = other
        self.worker = worker
        self.button_quit.clicked.connect(lambda: self.click_button_quit())
        self.button_work.clicked.connect(lambda: self.click_button_work())
        self.label_greetings.setText(f"Добро пожаловать, {self.worker.name}!")
        self.renew_result()
        self.show()

    def renew_result(self):
        self.label_result.setText(f"Ваш результат: {self.worker.result}")

    def click_button_work(self):
        self.worker.result += 1
        self.renew_result()
        RenewDataInTable(self.worker)

    def click_button_quit(self):
        self.other.__init__()
        self.destroy()


class AdminForm(QtWidgets.QMainWindow):
    def __init__(self, admin: User, other: AuthorisationForm):
        super().__init__()
        loadUi("AdminForm.ui",self)
        self.other = other
        self.admin = admin
        self.users = self.other.users
        self.main_font = QtGui.QFont("Arial")
        self.main_font.setPixelSize(18)
        self.button_quit.clicked.connect(lambda: self.click_button_quit())
        self.button_add.clicked.connect(lambda: self.click_button_add())
        self.button_change.clicked.connect(lambda: self.click_button_change())
        self.button_delete.clicked.connect(lambda: self.click_button_delete())

        self.results = dict()
        with open("Company list.csv", 'r') as file: # Открывает файл для чтения
            y = 0
            for line in file:
                x = 0
                self.tableWidget.setRowCount(y + 1)
                current = line.strip().split(',')
                for x in range(current.__len__()):
                    field = current[x]
                    if y == 0:
                        self.tableWidget.setColumnWidth(x, 493)
                    elif x == 0:
                        last_index = int(field)
                    if x != 5:
                        item = QtWidgets.QTableWidgetItem()
                        item.setText(str(field))
                        item.setFont(self.main_font)
                        item.setBackground(QtGui.QBrush(QtGui.QColor(120,120,120)))
                        item.setForeground(QtGui.QBrush(QtGui.QColor(0,0,0)))
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                        self.tableWidget.setItem(y, x, item)
                    elif y != 0:
                        self.results[int(current[0])] = int(field)
                y += 1

            self.next_index = last_index + 1

        self.show()

    def click_button_add(self):
        self.next_window = AddForm(self)
        self.destroy()
    
    def click_button_change(self):
        item = self.tableWidget.selectedItems()[0]
        index = int(item.text())
        login = self.tableWidget.item(item.row(), 1).text()
        result = self.results[index]
        self.next_window = ChangeForm(self,index,result,login)
        self.destroy()

    def click_button_delete(self):
        item = self.tableWidget.selectedItems()[0]
        user= User(
            [int(item.text()),'','','','',0]
        )
        DeleteUser(user)
        self.destroy()
        self.__init__(self.admin, self.other)
    def click_button_quit(self):
        self.other.__init__()
        self.destroy()

class AddForm(QtWidgets.QMainWindow):
    def __init__(self, other: AdminForm):
        super().__init__()
        loadUi("Change_or_AddForm.ui",self)
        self.other = other
        self.users = other.users
        self.index = self.other.next_index
        self.button_quit.clicked.connect(lambda: self.click_button_quit())
        self.button_enter.clicked.connect(lambda: self.click_button_enter())
        self.show()
        
    def click_button_enter(self):
        with open("Company list.csv", 'a') as file: # Открывает файл для чтения
            arga = [
                self.index,
                self.lineEdit.text(),
                self.lineEdit_2.text(),
                self.lineEdit_5.text(),
                self.lineEdit_3.text()+self.lineEdit_4.text(),
                0
            ]
            error = False
            for a in range(len(arga)):
                if arga[a] == '' or (a == 3 and (arga[a].lower() != "директор" and
                    arga[a].lower() != "администратор" and 
                    arga[a].lower() != "работник"
                    ) or (a == 1 and arga[a] in self.users.keys())
                ):
                    error = True
                    break
            if error:
                error_message = QtWidgets.QMessageBox()
                error_message.setStyleSheet(
                    "background-color: rgb(255,255,255);"+
                    "color:rgb(0,0,0);"+
                    "font:18pt \"Arial\";"
                )
                error_message.setText("Неверные данные!")
                error_message.exec_()
            else:
                user = User(arga)
                file.write(user.to_str())
        self.click_button_quit()

    def click_button_quit(self):
        self.other.__init__(self.other.admin, self.other.other)
        self.destroy()

class ChangeForm(QtWidgets.QMainWindow):
    def __init__(self, other: AdminForm, index: int, result: int, login: str):
        super().__init__()
        loadUi("Change_or_AddForm.ui",self)
        self.setWindowTitle(f"Окно изменения данных пользователя {index}")
        self.index = index
        self.login = login
        self.other = other
        self.result = result
        self.users = other.users
        self.button_quit.clicked.connect(lambda: self.click_button_quit())
        self.button_enter.clicked.connect(lambda: self.click_button_enter())
        self.show()

    def click_button_enter(self):
        arga = [
                    self.index,
                    self.lineEdit.text(),
                    self.lineEdit_2.text(),
                    self.lineEdit_5.text(),
                    self.lineEdit_3.text()+self.lineEdit_4.text(),
                    self.result
                ]
        error = False
        for a in range(len(arga)):
            if arga[a] == '' or (a == 3 and (arga[a].lower() != "директор" and
                arga[a].lower() != "администратор" and 
                arga[a].lower() != "работник"
                ) or (a == 1 and arga[a] in self.users.keys() and not arga[a] == self.login)
            ):
                error = True
                break
        if error:
            error_message = QtWidgets.QMessageBox()
            error_message.setStyleSheet(
                "background-color: rgb(255,255,255);"+
                "color:rgb(0,0,0);"+
                "font:18pt \"Arial\";"
            )
            error_message.setText("Неверные данные!")
            error_message.exec_()
        else:
            user = User(arga)
            RenewDataInTable(user)
        self.click_button_quit()
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        return super().closeEvent(a0)
    def click_button_quit(self):
        self.other.__init__(self.other.admin, self.other.other)
        self.destroy()

class DirectorForm(QtWidgets.QMainWindow):
    def __init__(self, director : User, all_users : dict, other : AuthorisationForm):
        super().__init__() # Вызывание конструктора базового класса
        loadUi("DirectorForm.ui", self) # Загружаем интерфейс формы
        self.director = director
        self.all_users = all_users
        self.other = other
        self.main_font = other.main_font
        self.button_quit.clicked.connect(lambda: self.click_button_quit()) # Связываем нажатие кнопки button_quit с исполнением метода click_button_quit(self)

        chart = QtChart.QChart()
        chart.setTheme(QtChart.QChart.ChartTheme.ChartThemeHighContrast)
        chart.setFont(self.main_font)

        self.tableWidget.setFont(self.other.main_font)
        
        self.tableWidget.setColumnWidth(0,266)
        self.tableWidget.setColumnWidth(1,266)
        self.tableWidget.setColumnWidth(2,266)
        i = 1
        self.tableWidget.setRowCount(i + 1)

        ids_list = list()
        for key in all_users.keys():
            user=all_users[key]
            if user.role == "работник":
                self.tableWidget.setRowCount(i + 1)
                if ids_list.__len__() == 0:
                    minimum = user.result
                    maximum = minimum
                ids_list.append(str(user.id))
                series = QtChart.QBarSeries()
                bar_set = QtChart.QBarSet(str(user.id))
                bar_set << int(user.result)
                if user.result > maximum:
                    maximum = user.result
                if user.result < minimum:
                    minimum = user.result
                series.append(bar_set)
                chart.addSeries(series)
            
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(user.id))
                item.setFont(self.main_font)
                item.setBackground(QtGui.QBrush(QtGui.QColor(120,120,120)))
                item.setForeground(QtGui.QBrush(QtGui.QColor(0,0,0)))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.tableWidget.setItem(i,0,item)

                item = QtWidgets.QTableWidgetItem()
                item.setText(str(user.name))
                item.setFont(self.main_font)
                item.setBackground(QtGui.QBrush(QtGui.QColor(120,120,120)))
                item.setForeground(QtGui.QBrush(QtGui.QColor(0,0,0)))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.tableWidget.setItem(i,1,item)

                item = QtWidgets.QTableWidgetItem()
                item.setText(str(user.result))
                item.setFont(self.main_font)
                item.setBackground(QtGui.QBrush(QtGui.QColor(120,120,120)))
                item.setForeground(QtGui.QBrush(QtGui.QColor(0,0,0)))
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.tableWidget.setItem(i,2,item)
                
                i += 1
        axisX = QtChart.QBarCategoryAxis(self)
        axisX.setCategories(ids_list)
        axisY = QtChart.QValueAxis(self)
        axisY.setRange(minimum, maximum)

        chart.createDefaultAxes()
        chart.setAxisX(axisX)
        chart.setAxisY(axisY)
        chart.legend().hide()
        chartview = QtChart.QChartView(self)
        chartview.setChart(chart)
        chartview.resize(649,680)
        chartview.move(841,10)

        
        self.show() # Показывает форму
        
    def click_button_quit(self):
        self.other.__init__()
        self.destroy()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Данный объект - GUI программа
    window = AuthorisationForm() # Данный объект - наше главное окно, сначала запускает форму авторизации
    sys.exit(app.exec_()) # Данный метод запускает цикл программы, и гарантирует завершение после выхода из цикла

import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore

class User:
    def __init__(self, arga : list()):
        self.name = (arga[0])
        self.login = (arga[1])
        self.password = (arga[2])

    def convert_to_CSVstring(self):
        return f"{self.name},{self.login},{self.password}\n"

def get_authData():
    users = dict()
    with open(os.path.abspath("data.csv"), 'r') as file:
        last_char = ''
        file.readline()
        for line in file:
            current_line = line.strip().split(',')
            last_char = line[-1]
            current_user = User(current_line)
            users[current_user.login] = current_user
    if last_char != '\n':
        with open(os.path.abspath("data.csv"), 'a') as file:
            file.write('\n')
    return users


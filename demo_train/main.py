import sys
import os
import pandas as pd
from PyQt5 import QtWidgets, QtCore, QtGui, uic

# Смотреть с 19-ой минуты

class Window1(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.getcwd(), "untitled.ui"), self)
        self.show()
    
    def submit(self):
        self.button.setText("clicked")
        self.button.setDisabled(True)

    def closeEvent(self, a0: QtGui.QCloseEvent | None) -> None:
        sys.exit()


if __name__ == "__main__":
    process = QtWidgets.QApplication(sys.argv)
    programm = Window1()
    sys.exit(process.exec_())

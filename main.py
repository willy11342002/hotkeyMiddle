from PyQt5 import QtWidgets
from window.main import MainWindow
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

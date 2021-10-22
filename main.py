from PyQt5 import QtWidgets
from window.main import MainWindow
from pathlib import Path
import sys


if __name__ == '__main__':
    if not Path('data').exists():
        Path('data').mkdir()
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

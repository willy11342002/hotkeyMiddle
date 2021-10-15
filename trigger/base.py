from PyQt5 import QtWidgets
from utils.path import Dict


class BaseTrigger:
    def __init__(self):
        self._data = Dict()
        self.first = QtWidgets.QWidget()
        self.label = QtWidgets.QLabel()
        self.widget = QtWidgets.QWidget()

    def change_data(self, key, value):
        self._data[key] = value

    @property
    def data(self):
        return self._data

    @property
    def ui(self):
        return [self.first, self.label, self.widget]

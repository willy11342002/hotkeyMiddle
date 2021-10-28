from PyQt5 import QtWidgets
from PyQt5 import QtCore


class ComboBox(QtWidgets.QComboBox):
    sig_current_changed = QtCore.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currentIndexChanged.connect(self.sig_current_changed.emit)
    @classmethod
    def from_value(cls, value):
        obj = cls()
        obj.addItems(value.choices)
        obj.setCurrentIndex(value.fixed)
        return obj
    @property
    def current(self):
        return self.currentIndex()
    @current.setter
    def current(self, idx):
        self.setCurrentIndex(idx)

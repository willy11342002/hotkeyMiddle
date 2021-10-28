from PyQt5 import QtWidgets
from PyQt5 import QtCore


class SpinBox(QtWidgets.QSpinBox):
    sig_current_changed = QtCore.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valueChanged.connect(self.sig_current_changed.emit)
    @classmethod
    def from_value(cls, value):
        obj = cls()
        obj.setValue(value.fixed)
        return obj
    @property
    def current(self):
        return self.value()
    @current.setter
    def current(self, value):
        self.setValue(value)

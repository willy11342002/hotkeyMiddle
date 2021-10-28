from PyQt5 import QtWidgets
from PyQt5 import QtCore


class TextEdit(QtWidgets.QTextEdit):
    sig_current_changed = QtCore.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self.sig_current_changed.emit)
    @classmethod
    def from_value(cls, value):
        obj = cls()
        obj.setText(value.fixed)
        return obj
    @property
    def current(self):
        return self.toPlainText()
    @current.setter
    def current(self, txt):
        self.setText(txt)

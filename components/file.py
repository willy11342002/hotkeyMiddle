from PyQt5 import QtWidgets
from PyQt5 import QtCore
from pathlib import Path


class FileEdit(QtWidgets.QPushButton):
    sig_current_changed = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.choose_path)

    @classmethod
    def from_value(cls, value):
        obj = cls()
        obj.path = Path(value.fixed)
        obj.method = value.method
        obj.types = value.types
        return obj
    @property
    def current(self):
        return str(self.path.absolute())
    @current.setter
    def current(self, path):
        self.path = Path(path)

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, p):
        self._path = p
        self.setText(str(p.absolute()))
        self.sig_current_changed.emit()

    def choose_path(self):
        filename, ok = getattr(QtWidgets.QFileDialog, self.method)(
            self, '選擇檢查檔', str(self.path.parent), self.types)
        if not ok:
            return
        self.path = Path(filename)

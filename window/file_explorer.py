from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class FileLink(QtWidgets.QTreeWidgetItem):
    def __init__(self, script, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.script = script
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)

    @property
    def path(self) -> Path:
        return self.script.path
    @path.setter
    def path(self, path):
        self.script.path = path

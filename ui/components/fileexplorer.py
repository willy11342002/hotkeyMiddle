from PyQt5 import QtWidgets
from PyQt5 import QtCore


class FileLink(QtWidgets.QTreeWidgetItem):
    def __init__(self, script, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.script = script
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)

    @property
    def path(self):
        return self.script.path
    @path.setter
    def path(self, path):
        self.script.path = path


class FileExplorer(QtWidgets.QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 設定樣式
        style = QtWidgets.QApplication.style()
        self.icon_dir_open = style.standardIcon(QtWidgets.QStyle.SP_DirOpenIcon)
        self.icon_dir_close = style.standardIcon(QtWidgets.QStyle.SP_DirClosedIcon)
        self.icon_pause = style.standardIcon(QtWidgets.QStyle.SP_MediaPause)
        self.icon_run = style.standardIcon(QtWidgets.QStyle.SP_MediaPlay)
        # 綁定功能
        self.itemExpanded.connect(self.item_expanded)
        self.itemCollapsed.connect(self.item_collapsed)

    # 展開、收合類別
    def item_expanded(self, item):
        item.setIcon(0, self.icon_dir_open)
    def item_collapsed(self, item):
        item.setIcon(0, self.icon_dir_close)

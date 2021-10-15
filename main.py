from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from ui.main import Ui_MainWindow
from utils.path import Dict
from utils.path import walk
from pathlib import Path
import sys
import ui


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.dic_scripts = Dict()

        style = QtWidgets.QApplication.style()
        self.icon_checked = style.standardIcon(QtWidgets.QStyle.SP_DialogApplyButton)
        self.action_file_explorer.setIcon(self.icon_checked)

        # 選單 - 檔案
        self.action_add_category.triggered.connect(lambda e: self.create_category(None))
        self.action_add_script.triggered.connect(lambda e: self.create_script(None))
        self.action_save.triggered.connect(self.save_script)
        self.action_close.triggered.connect(self.closeEvent)
        # 選單 - 檢視
        self.action_file_explorer.triggered.connect(self.switch_file_explorer)
        # 選單 - 操作
        self.action_start_all.triggered.connect(self.start_all)
        self.action_stop_all.triggered.connect(self.stop_all)

        # 畫面修改功能
        self.tree_scripts.itemDoubleClicked.connect(lambda item: item.script.open_editor())
        self.tree_scripts.itemChanged.connect(lambda item: item.script.rename(item.text(0)))
        self.main_script.tabCloseRequested.connect(lambda idx: self.main_script.widget(idx).script.close_editor())
        self.main_script.currentChanged.connect(self.detect_savable)

        self.load_list()

    # 切換檔案總管是否顯示
    def switch_file_explorer(self):
        if self.file_explorer.isHidden():
            self.file_explorer.show()
            self.action_file_explorer.setIcon(self.icon_checked)
        else:
            self.file_explorer.hide()
            self.action_file_explorer.setIcon(QtGui.QIcon())

    # 讀取完整清單
    def load_list(self):
        for dirpath, dirnames, filenames in walk('data'):
            for dirname in dirnames:
                if dirname.parent != Path('data'):
                    continue
                self.create_category(path=dirname)
            for filename in filenames:
                if filename.parent.parent != Path('data'):
                    continue
                if not filename.name.endswith('.ini'):
                    continue
                self.create_script(path=filename)

    # 新增類別
    def create_category(self, path: Path=None):
        undefined = self.tree_scripts.findItems('新增類別', QtCore.Qt.MatchStartsWith, 0)
        if undefined:
            path = path or Path('data') / f'新增類別 ({len(undefined)})'
        else:
            path = path or Path('data') / f'新增類別'

        script = ui.Script(self, path)
        script.tree.setIcon(0, self.tree_scripts.icon_dir_close)
        self.tree_scripts.addTopLevelItem(script.tree)

        self.dic_scripts[id(script)] = script

    # 新增腳本
    def create_script(self, path: Path=None):
        if path is None:
            parent = self.tree_scripts.currentItem()
            if parent is None:
                return
            parent = parent.parent() or parent
        else:
            parent = self.tree_scripts.findItems(path.parent.name, QtCore.Qt.MatchExactly, 0)[0]
        undefined = self.tree_scripts.findItems('新增腳本', QtCore.Qt.MatchStartsWith|QtCore.Qt.MatchRecursive, 0)
        undefined = list(filter(lambda x: x.parent() == parent, undefined))
        if undefined:
            path = path or parent.path / f'新增腳本 ({len(undefined)}).ini'
        else:
            path = path or parent.path / f'新增腳本.ini'

        script = ui.Script(self, path)
        parent.addChild(script.tree)

        self.dic_scripts[id(script)] = script

    # 儲存檔案
    def save_script(self, path: Path=None):
        editor = self.main_script.currentWidget()
        editor.save_data(path)

    # 控制工具列是否可以保存
    def detect_savable(self):
        if self.main_script.currentIndex() != -1:
            self.action_save.setEnabled(True)
            self.action_save_as.setEnabled(True)
        else:
            self.action_save.setEnabled(False)
            self.action_save_as.setEnabled(False)

    def start_all(self):
        items = self.tree_scripts.findItems('', QtCore.Qt.MatchContains|QtCore.Qt.MatchRecursive, 0)
        for item in items:
            if not item.parent():
                continue
            item.script.editor.ccb_activate.setCurrentIndex(1)
            item.script.editor.save_data()
    def stop_all(self):
        items = self.tree_scripts.findItems('', QtCore.Qt.MatchContains|QtCore.Qt.MatchRecursive, 0)
        for item in items:
            if not item.parent():
                continue
            item.script.editor.ccb_activate.setCurrentIndex(0)
            item.script.editor.save_data()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

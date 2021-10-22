from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from ui.main import Ui_MainWindow
from window.script import Script
from utils.path import Dict
from utils.path import walk
from pathlib import Path


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.showMaximized()

        self.dic_scripts = Dict()

        # 選單 - 檔案
        self.action_add_category.triggered.connect(lambda e: self.create_category(None))
        self.action_add_script.triggered.connect(lambda e: self.create_script(None))
        self.action_save.triggered.connect(self.save_script)
        self.action_close.triggered.connect(self.closeEvent)
        # 選單 - 檢視
        self.action_file_explorer.triggered.connect(self.switch_file_explorer)
        self.action_script_explorer.triggered.connect(self.switch_script_explorer)
        # 選單 - 操作
        self.action_start_all.triggered.connect(self.start_all)
        self.action_stop_all.triggered.connect(self.stop_all)

        # 畫面修改功能
        self.tree_files.itemDoubleClicked.connect(lambda item: item.script.open_editor())
        self.tree_files.itemChanged.connect(lambda item: item.script.rename(item.text(0)))
        self.main_script.currentChanged.connect(self.detect_savable)

        self.tree_scripts.doubleClicked.connect(
            lambda: self.tree_scripts.currentItem().parent() and
                    self.main_script.currentWidget() and 
                    self.main_script.currentWidget().add_trigger(
                        class_name=self.tree_scripts.currentItem().whatsThis(0)
                    ))

        self.load_list()

    def switch_script_explorer(self):
        if self.script_explorer.isHidden():
            self.script_explorer.show()
        else:
            self.script_explorer.hide()

    # 切換檔案總管是否顯示
    def switch_file_explorer(self):
        if self.file_explorer.isHidden():
            self.file_explorer.show()
        else:
            self.file_explorer.hide()

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
        undefined = self.tree_files.findItems('新增類別', QtCore.Qt.MatchStartsWith, 0)
        if undefined:
            path = path or Path('data') / f'新增類別 ({len(undefined)})'
        else:
            path = path or Path('data') / f'新增類別'

        if not path.exists():
            path.mkdir()
        script = Script(self, path)
        self.tree_files.addTopLevelItem(script.tree)

    # 新增腳本
    def create_script(self, path: Path=None):
        if path is None:
            parent = self.tree_files.currentItem()
            if parent is None:
                return
            parent = parent.parent() or parent
        else:
            parent = self.tree_files.findItems(path.parent.name, QtCore.Qt.MatchExactly, 0)[0]
        undefined = self.tree_files.findItems('新增腳本', QtCore.Qt.MatchStartsWith|QtCore.Qt.MatchRecursive, 0)
        undefined = list(filter(lambda x: x.parent() == parent, undefined))
        if undefined:
            path = path or parent.path / f'新增腳本 ({len(undefined)}).ini'
        else:
            path = path or parent.path / f'新增腳本.ini'

        if not path.exists():
            path.touch()

        script = Script(self, path)
        parent.addChild(script.tree)

    # 儲存檔案
    def save_script(self, path: Path=None):
        editor = self.main_script.currentWidget()
        idx = self.main_script.indexOf(editor)

        editor.save_data(path)
        self.main_script.setTabText(idx, editor.script.tab_text)
        print(editor._data)
        print(editor.data)
        print(editor.data == editor._data)

    # 控制工具列是否可以保存
    def detect_savable(self):
        if self.main_script.currentIndex() != -1:
            self.action_save.setEnabled(True)
            self.action_save_as.setEnabled(True)
        else:
            self.action_save.setEnabled(False)
            self.action_save_as.setEnabled(False)

    def start_all(self):
        items = self.tree_files.findItems('', QtCore.Qt.MatchContains|QtCore.Qt.MatchRecursive, 0)
        for item in items:
            if not item.parent():
                continue
            item.script.editor.ccb_activate.setCurrentIndex(1)
            item.script.editor.save_data()
    def stop_all(self):
        items = self.tree_files.findItems('', QtCore.Qt.MatchContains|QtCore.Qt.MatchRecursive, 0)
        for item in items:
            if not item.parent():
                continue
            item.script.editor.ccb_activate.setCurrentIndex(0)
            item.script.editor.save_data()


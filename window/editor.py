from pathlib import Path
from PyQt5 import QtWidgets

from ui.editor import Ui_ScriptEditor
from utils.path import Dict
import trigger


class Editor(QtWidgets.QWidget, Ui_ScriptEditor):
    _data = Dict({
        'BASIC': {
            'activate': False,
            'start_hotkey': [121],
            'stop_hotkey': [123],
            'descript': '',
            'category': 'once'
        },
        'SCRIPT': {
            'content': []
        },
    })
    def __init__(self, script, path, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.script = script
        self.path = path
        self.read_data()
        

    @property
    def data(self) -> Dict:
        if self.path.is_dir():
            return self._data

        if self.rb_once.isChecked():
            category = 'once'
        if self.rb_while.isChecked():
            category = 'while'

        return Dict({
            'BASIC': {
                'activate': bool(self.ccb_activate.currentIndex()),
                'start_hotkey': self.le_start_hotkey.PRESSED_KEY_VK,
                'stop_hotkey': self.le_stop_hotkey.PRESSED_KEY_VK,
                'descript': self.te_descript.toPlainText(),
                'category': category
            },
            'SCRIPT': {
                'content': []
            },
        })
    @data.setter
    def data(self, data):
        self._data = data
        # 修改UI
        self.ccb_activate.setCurrentIndex(int(data.BASIC.activate))
        self.le_start_hotkey.PRESSED_KEY_VK = data.BASIC.start_hotkey
        self.le_stop_hotkey.PRESSED_KEY_VK = data.BASIC.stop_hotkey
        self.te_descript.setText(data.BASIC.descript)
        if data.BASIC.category == 'once':
            self.rb_once.click()
        else:
            self.rb_while.click()

    @property
    def path(self) -> Path:
        return self.script.path
    @path.setter
    def path(self, path):
        self.script.path = path

    # 腳本內容存讀
    def compare_data(self) -> bool:
        return self._data == self.data
    def reset_data(self):
        self.data = self._data
    def init_data(self):
        self.data.dump_json(self.path)
    def read_data(self):
        if self.path.is_dir():
            return
        if not self.path.read_text():
            self.init_data()
            return
        # 讀取資料
        self.data = Dict.load_json(self.path)
    def save_data(self, path=None):
        path = path or self.path
        self.data.dump_json(path)

    # 腳本設計
    def move_up_trigger(self, trigger):
        pass
    def move_down_trigger(self, trigger):
        pass
    def remove_trigger(self, trigger):
        pass
    def sort_trigger(self):
        pass
    def add_trigger(self, row=None, data=None):
        pass


class EditorTabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTabBar(QtWidgets.QTabBar())
        self.tabBar().setAutoHide(False)
        self.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, idx):
        editor = self.widget(idx)
        if editor.compare_data():
            self.removeTab(idx)
            return
        result = QtWidgets.QMessageBox.information(
            self, '關閉頁籤', '若未儲存，變更將會遺失，確認關閉頁籤嗎?',
            QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No
        )
        if result == QtWidgets.QMessageBox.No:
            return
        elif result == QtWidgets.QMessageBox.Yes:
            editor.reset_data()
            self.removeTab(idx)

from PyQt5 import QtWidgets
from ..editor import Ui_ScriptEditor
from trigger import ImgCheckTrigger
from trigger import ScreenShotTrigger
from trigger import FileLoadTrigger
from trigger import FileSaveTrigger
from trigger import KeyboardTrigger
from trigger import MouseTrigger
from utils.path import Dict
import copy

class Editor(QtWidgets.QWidget, Ui_ScriptEditor):
    DIC_TRIGGER = Dict({
        'pb_click_mouse': MouseTrigger,
        'pb_click_keyboard': KeyboardTrigger,
        'pb_file_load': FileLoadTrigger,
        'pb_file_save': FileSaveTrigger,
        'pb_img_check': ImgCheckTrigger,
        'pb_screen_shot': ScreenShotTrigger,
    })
    def __init__(self, script, *args, **kwargs):
        super().__init__()
        self.script = script
        self.unsave = False
        self.steps = []
        self.setupUi(self)
        self.read_data()

        self.ccb_activate.currentIndexChanged.connect(
            lambda idx: self.change_data('BASIC', 'activate', bool(idx)))
        self.le_start_hotkey.textChanged.connect(
            lambda txt: self.change_data('BASIC', 'start_hotkey', self.le_start_hotkey.PRESSED_KEY_VK))
        self.le_stop_hotkey.textChanged.connect(
            lambda txt: self.change_data('BASIC', 'stop_hotkey', self.le_stop_hotkey.PRESSED_KEY_VK))
        self.rb_once.toggled.connect(
            lambda: self.change_data('BASIC', 'category', 'once') and self.le_stop_hotkey.setEnabled(False))
        self.rb_while.toggled.connect(
            lambda: self.change_data('BASIC', 'category', 'while') and self.le_stop_hotkey.setEnabled(True))
        self.te_descript.textChanged.connect(
            lambda: self.change_data('BASIC', 'descript', self.te_descript.toPlainText()))
        self.te_record.textChanged.connect(
            lambda: self.change_data('RECORD', 'content', self.te_record.toPlainText()))

    @property
    def path(self):
        return self.script.path
    @path.setter
    def path(self, path):
        self.script.path = path

    @property
    def unsave(self):
        return self._unsave
    @unsave.setter
    def unsave(self, value):
        self._unsave = value
        idx = self.script.mainwindow.main_script.indexOf(self)
        if idx != -1:
            self.script.mainwindow.main_script.setTabText(idx, self.tab_text)
        self.script.tree.setText(0, self.tab_text)

    @property
    def tab_text(self):
        return f'{"* " if self._unsave else ""}{self.path.stem}'

    # 腳本內容存讀
    def change_data(self, section, key, value):
        self.data[section][key] = value
        self.unsave = self.data != self._data
        return True
    def read_data(self):
        if self.path.is_dir():
            self.data = Dict()
            return
        if not self.path.read_text():
            self.data = Dict({
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
                'RECORD': {
                    'content': ''
                },
            })
            self._data = copy.deepcopy(self.data)
            self.data.dump_json(self.path)
            return
        # 讀取資料
        self.data = Dict.load_json(self.path)
        self._data = copy.deepcopy(self.data)
        self.unsave = False
        # 調整畫面
        self.ccb_activate.setCurrentIndex(int(self.data.BASIC.activate))
        self.le_start_hotkey.PRESSED_KEY_VK = self.data.BASIC.start_hotkey
        self.le_stop_hotkey.PRESSED_KEY_VK = self.data.BASIC.stop_hotkey
        self.te_descript.setText(self.data.BASIC.descript)
        for i, data in enumerate(self.data.SCRIPT.content):
            self.add_trigger(row=i, data=data)
        return self.data
    def save_data(self, path=None):
        path = path or self.path
        self.data['SCRIPT']['content'] = [
            self.tb_script.cellWidget(row, 0).data
            for row in range(self.tb_script.rowCount())
        ]
        self.data.dump_json(path)
        self._data = copy.deepcopy(self.data)
        self.unsave = False

    # 腳本設計
    def move_up_trigger(self, trigger):
        for row in range(self.tb_script.rowCount()):
            first = self.tb_script.cellWidget(row, 0)
            if row != 0 and first == trigger.first:
                self.tb_script.removeRow(row)
                self.add_trigger(row=row-1, data=trigger.data)
                self.data.SCRIPT.content.insert(row-1, self.data.SCRIPT.content.pop(row))
                break
        self.unsave = self.data != self._data
    def move_down_trigger(self, trigger):
        for row in range(self.tb_script.rowCount()):
            first = self.tb_script.cellWidget(row, 0)
            if row != self.tb_script.rowCount()-1 and first == trigger.first:
                self.tb_script.removeRow(row)
                self.add_trigger(row=row+1, data=trigger.data)
                self.data.SCRIPT.content.insert(row+1, self.data.SCRIPT.content.pop(row))
                break
        self.unsave = self.data != self._data
    def remove_trigger(self, trigger):
        for row in range(self.tb_script.rowCount()):
            first = self.tb_script.cellWidget(row, 0)
            if first == trigger.first:
                self.tb_script.removeRow(row)
                self.data.SCRIPT.content.pop(row)
                break
        self.unsave = self.data != self._data
    def sort_trigger(self):
        for row in range(self.tb_script.rowCount()):
            item = self.tb_script.verticalHeaderItem(row)
            item.setText(str(row))
    def add_trigger(self, row=None, data=None):
        row = row or self.tb_script.currentRow()
        row = 0 if row == -1 else row

        if data:
            _class = globals()[data['class_name']]
            trigger = _class(self, data)
            first, label, widget = trigger.ui
        else:
            pb = self.sender()
            Trigger = self.DIC_TRIGGER[pb.objectName()]
            trigger = Trigger(self, data)
            first, label, widget = trigger.ui
            self.data.SCRIPT.content.insert(row, data)
            self.unsave = self.data != self._data

        self.tb_script.insertRow(row)
        item = QtWidgets.QTableWidgetItem(str(row))
        self.tb_script.setVerticalHeaderItem(row, item)
        self.tb_script.setCellWidget(row, 0, first)
        self.tb_script.setCellWidget(row, 1, label)
        self.tb_script.setCellWidget(row, 2, widget)
        self.tb_script.verticalHeader().resizeSection(row, 50)

        self.sort_trigger()


class EditorTabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTabBar(QtWidgets.QTabBar())
        self.tabBar().setAutoHide(False)

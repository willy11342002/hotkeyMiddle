from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from pathlib import Path

from trigger import KeyboardTrigger
from trigger import MouseTrigger
from ui.component import HotKeyEdit
from utils.path import Dict
from utils.vk import VK
import pynput
import copy


# 腳本功能視窗
class Script:
    mouse_controller = pynput.mouse.Controller()
    keyboard_controller = pynput.keyboard.Controller()
    def __init__(self, mainwindow, path):
        self.mainwindow = mainwindow
        self.path = path
        self.is_open = False
        # 創建資料夾(文件)
        if not self.path.exists():
            if not self.path.name.endswith('.ini'):
                self.path.mkdir()
            else:
                self.path.touch()
        self.tree = FileLink(self, [path.stem])
        self.editor = Editor(self)

        self.editor.ccb_activate.currentIndexChanged.connect(self.switch_status)
        self.switch_status(self.editor.ccb_activate.currentIndex())

        # 偵測快速鍵
        self.pressing_key = set()
        self.keyboard_listener = pynput.keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        )
        self.keyboard_listener.start()
        self.mouse_listener = pynput.mouse.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        )
        self.mouse_listener.start()

    # 修改檔案名撐、UI頁籤名稱
    def rename(self, new_name):
        if new_name == self.editor.tab_text:
            return
        # 修改檔案
        if self.path.is_dir():
            self.path.rename(f'data/{new_name}')
            self.path = Path(f'data/{new_name}')
            for i in range(self.tree.childCount()):
                self.tree.child(i).path = self.path / f'{self.tree.child(i).text(0)}.ini'
        else:
            self.path.rename(f'{self.path.parent}/{new_name}.ini')
            self.path = Path(f'{self.path.parent}/{new_name}.ini')
        # 修改UI
        self.tree.setText(0, self.editor.tab_text)
        idx = self.mainwindow.main_script.indexOf(self.editor)
        self.mainwindow.main_script.setTabText(idx, self.editor.tab_text)

    # 開啟腳本(建立頁簽)
    def activate_editor(self):
        self.mainwindow.main_script.setCurrentWidget(self.editor)
    def open_editor(self):
        if self.path.is_dir():
            return
        if not self.is_open:
            self.mainwindow.main_script.addTab(self.editor, self.editor.tab_text)
            self.is_open = True
        self.activate_editor()

    # 切換啟用/停用，同時修改左側圖示及右側各選項是否可修改
    def switch_status(self, idx):
        dic_icon = dict(enumerate([
            self.mainwindow.tree_scripts.icon_pause,
            self.mainwindow.tree_scripts.icon_run,
        ]))
        self.tree.setIcon(0, dic_icon[idx])
        self.editor.le_start_hotkey.setEnabled(not bool(idx))
        self.editor.le_stop_hotkey.setEnabled(
            not bool(idx) and self.editor.rb_while.isChecked())
        self.editor.te_descript.setEnabled(not bool(idx))
        self.editor.pb_click_mouse.setEnabled(not bool(idx))
        self.editor.pb_click_keyboard.setEnabled(not bool(idx))
        self.editor.tb_script.setEnabled(not bool(idx))
        self.editor.te_record.setEnabled(not bool(idx))

    # 關閉腳本(關閉頁簽)
    def close_editor(self):
        idx = self.mainwindow.main_script.indexOf(self.editor)
        self.mainwindow.main_script.removeTab(idx)
        self.is_open = False

    def run_script(self):
        for row in range(self.editor.tb_script.rowCount()):
            first = self.editor.tb_script.cellWidget(row, 0)
            first.activate()

    # 鍵盤偵測
    def on_press(self, key):
        '''按下按鈕後存入集合並逐一檢查是否滿足快速鍵'''
        # 加入集合
        if not self.editor.data:
            return
        # 啟動中，逐一檢查是否滿足快速鍵
        if self.editor.ccb_activate.currentIndex():
            vk = VK.get_vk_from_key(key)
            self.pressing_key.add(vk)
            if not (set(self.editor.le_start_hotkey.PRESSED_KEY_VK) - self.pressing_key):
                self.pressing_key.clear()
                self.run_script()
    def on_release(self, key):
        '''釋放按鈕後從集合中移出'''
        vk = VK.get_vk_from_key(key)
        self.pressing_key.discard(vk)

    # 滑鼠偵測
    def on_move(x, y):
        pass
    def on_click(x, y, button, is_press):
        pass
    def on_scroll(x, y, dx, dy):
        pass


# 左側檔案總管
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


#  右側編輯器
from .editor import Ui_ScriptEditor
class Editor(QtWidgets.QWidget, Ui_ScriptEditor):
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

        self.pb_click_mouse.clicked.connect(
            lambda: self.add_trigger())
        self.pb_click_keyboard.clicked.connect(
            lambda: self.add_trigger())

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
                    'content': ''
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
    def add_trigger(self, row=None, data=None):
        row = row or self.tb_script.currentRow()
        row = 0 if row == -1 else row

        if data:
            _class = globals()[data['class_name']]
            trigger = _class(self, data)
            first, label, widget = trigger.ui
        else:
            pb = self.sender()
            if pb == self.pb_click_mouse:
                trigger = MouseTrigger(self, data)
                first, label, widget = trigger.ui
            elif pb == self.pb_click_keyboard:
                trigger = KeyboardTrigger(self, data)
                first, label, widget = trigger.ui
            self.data.SCRIPT.content.insert(row, data)
            self.unsave = self.data != self._data

        self.tb_script.insertRow(row)
        self.tb_script.setCellWidget(row, 0, first)
        self.tb_script.setCellWidget(row, 1, label)
        self.tb_script.setCellWidget(row, 2, widget)
        self.tb_script.verticalHeader().resizeSection(row, 50)


class EditorTabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTabBar(QtWidgets.QTabBar())
        self.tabBar().setAutoHide(False)


from .main import Ui_MainWindow

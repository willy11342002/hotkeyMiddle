import pynput._util.win32_vks as VK
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from pathlib import Path

import werdsazxc
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
        dic_icon = dict(enumerate([
            self.mainwindow.tree_scripts.icon_pause,
            self.mainwindow.tree_scripts.icon_run,
        ]))
        self.tree.setIcon(0, dic_icon[self.editor.ccb_activate.currentIndex()])

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
            return
        self.activate_editor()

    def switch_status(self, idx):
        dic_icon = dict(enumerate([
            self.mainwindow.tree_scripts.icon_pause,
            self.mainwindow.tree_scripts.icon_run,
        ]))
        self.tree.setIcon(0, dic_icon[idx])

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
            vk = getattr(key, 'vk', None)
            if not vk:
                vk = {
                    'alt_l': 18, 'alt_r': 18,
                    'shift_l': 16, 'shift_r': 16,
                    'ctrl_l': 17, 'ctrl_r': 17,
                }.get(key._name_)
            if not vk:
                vk = key._value_.vk
            self.pressing_key.add(vk)
            self.editor.le_start_hotkey.PRESSED_KEY_VK = self.editor.data.BASIC.start_hotkey
            print(self.pressing_key)
            print(set(self.editor.le_start_hotkey.PRESSED_KEY_VK))
            if not (set(self.editor.le_start_hotkey.PRESSED_KEY_VK) - self.pressing_key):
                self.pressing_key.clear()
                self.run_script()
    def on_release(self, key):
        '''釋放按鈕後從集合中移出'''
        try:
            vk = getattr(key, 'vk', None)
            if not vk:
                vk = getattr(VK, key._name_.upper(), None)
            self.pressing_key.remove(vk)
        except KeyError as e:
            pass

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
class HotKeyEdit(QtWidgets.QLineEdit):
    DIC_VIRTUALKEY = {v:k for k, v in vars(VK).items() if type(v) == int}
    DIC_VIRTUALKEY = {
        **DIC_VIRTUALKEY,
        18: "ALT", 192: "`", 27: "ESC", 33: "PAGE UP", 34: "PAGE DOWN",
        111: "NUMPAD/", 106: "NUMPAD*", 107: "NUMPAD+", 109: "NUMPAD-", 110: "NUMPAD.",
        49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54:"6", 55: "7", 56: "8", 57: "9", 58: "0",
        65: "A", 66: "B", 67: "C", 68: "D", 69: "E", 70:"F", 71: "G", 72: "H", 73: "I", 74: "J",
        75: "K", 76: "L", 77: "M", 78: "N", 79: "O", 80:"P", 81: "Q", 82: "R", 83: "S", 84: "T",
        85: "U", 86: "V", 87: "W", 88: "X", 89: "Y", 90:"Z"
    }
    _PRESSED_KEY = set()
    def __init__(self, master=None, single_mode=False, *args, **kwargs):
        self.single_mode = single_mode
        super().__init__(master, *args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_InputMethodEnabled, False)

    @property
    def PRESSED_KEY_VK(self):
        return list(map(lambda key: key.vk, self._PRESSED_KEY))
    @PRESSED_KEY_VK.setter
    def PRESSED_KEY_VK(self, vks):
        self._PRESSED_KEY = set(map(pynput.keyboard.KeyCode.from_vk, vks))
        self.setText('+'.join(self.PRESSED_KEY_STR))
    @property
    def PRESSED_KEY_STR(self):
        return list(map(self.get_human_key, self.PRESSED_KEY_VK))

    # 字元轉換
    def get_human_key(self, vk):
        hkey = self.DIC_VIRTUALKEY.get(vk, 'Unknow')
        return hkey
    def get_vk(self, event):
        return event.nativeVirtualKey()
    # 按鍵綁定
    def keyPressEvent(self, event):
        if self.single_mode and self._PRESSED_KEY:
            return
        vk = self.get_vk(event)
        pkey = pynput.keyboard.KeyCode.from_vk(vk)
        self._PRESSED_KEY.add(pkey)
        self.setText('+'.join(self.PRESSED_KEY_STR))
    def keyReleaseEvent(self, event):
        try:
            vk = self.get_vk(event)
            pkey = pynput.keyboard.KeyCode.from_vk(vk)
            self._PRESSED_KEY.remove(pkey)
        except KeyError as e:
            pass


class MouseTrigger:
    def __init__(self, editor, data=None):
        self.editor = editor
        self._data = data or {
            'class_name': self.__class__.__name__,
            'cbb1': 0,
            'cbb2': 0
        }
        self.init_ui()
        self.first.data = self.data
        self.first.activate = self.activate
        self.pb_delete.clicked.connect(lambda: editor.remove_trigger(self))
        self.pb_up.clicked.connect(lambda: editor.move_up_trigger(self))
        self.pb_down.clicked.connect(lambda: editor.move_down_trigger(self))

        self.cbb1.currentIndexChanged.connect(
            lambda idx: self.change_data('cbb1', idx))
        self.cbb2.currentIndexChanged.connect(
            lambda idx: self.change_data('cbb2', idx))

    def init_ui(self):
        self.first = QtWidgets.QWidget()
        self.hlayout1 = QtWidgets.QHBoxLayout(self.first)
        self.pb_up = QtWidgets.QPushButton()
        self.pb_up.setText('↑')
        self.pb_delete = QtWidgets.QPushButton()
        self.pb_delete.setText('X')
        self.pb_down = QtWidgets.QPushButton()
        self.pb_down.setText('↓')
        self.hlayout1.addWidget(self.pb_up)
        self.hlayout1.addWidget(self.pb_delete)
        self.hlayout1.addWidget(self.pb_down)

        self.label = QtWidgets.QLabel('滑鼠操作')
        self.widget = QtWidgets.QWidget()
        self.hlayout = QtWidgets.QHBoxLayout(self.widget)

        self.cbb1 = QtWidgets.QComboBox(self.widget)
        self.cbb1.addItems(['單擊', '雙擊'])
        self.cbb1.setCurrentIndex(self.data['cbb1'])

        self.cbb2 = QtWidgets.QComboBox(self.widget)
        self.cbb2.addItems(['左鍵', '中鍵', '右鍵'])
        self.cbb2.setCurrentIndex(self.data['cbb2'])

        self.space = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.hlayout.addWidget(self.cbb1)
        self.hlayout.addWidget(self.cbb2)
        self.hlayout.addItem(self.space)

    def change_data(self, key, value):
        self._data[key] = value

    @property
    def data(self):
        return self._data

    @property
    def ui(self):
        return [self.first, self.label, self.widget]

    def activate(self):
        btn = dict(enumerate([
            pynput.mouse.Button.left,
            pynput.mouse.Button.middle,
            pynput.mouse.Button.right,
        ]))[self.data['cbb2']]
        self.editor.script.mouse_controller.click(
            btn,
            self.data['cbb1']+1
        )

class KeyboardTrigger:
    def __init__(self, editor, data=None):
        self.editor = editor
        self._data = data or {
            'class_name': self.__class__.__name__,
            'cbb1': 0,
            'le': []
        }
        self.init_ui()
        self.first.data = self.data
        self.first.activate = self.activate
        self.pb_delete.clicked.connect(lambda: editor.remove_trigger(self))
        self.pb_up.clicked.connect(lambda: editor.move_up_trigger(self))
        self.pb_down.clicked.connect(lambda: editor.move_down_trigger(self))

        self.cbb1.currentIndexChanged.connect(
            lambda idx: self.change_data('cbb1', idx))
        self.le.textChanged.connect(
            lambda txt: self.change_data('le', self.le.PRESSED_KEY_VK))

    def init_ui(self):
        self.first = QtWidgets.QWidget()
        self.hlayout1 = QtWidgets.QHBoxLayout(self.first)
        self.pb_up = QtWidgets.QPushButton()
        self.pb_up.setText('↑')
        self.pb_delete = QtWidgets.QPushButton()
        self.pb_delete.setText('X')
        self.pb_down = QtWidgets.QPushButton()
        self.pb_down.setText('↓')
        self.hlayout1.addWidget(self.pb_up)
        self.hlayout1.addWidget(self.pb_delete)
        self.hlayout1.addWidget(self.pb_down)

        self.label = QtWidgets.QLabel('鍵盤操作')
        self.widget = QtWidgets.QWidget()
        self.hlayout = QtWidgets.QHBoxLayout(self.widget)

        self.cbb1 = QtWidgets.QComboBox(self.widget)
        self.cbb1.addItem('點擊按鍵')
        self.cbb1.addItem('點擊組合鍵')
        self.cbb1.setCurrentIndex(self.data['cbb1'])

        self.le = HotKeyEdit(single_mode=True)
        self.le.PRESSED_KEY_VK = self.data['le']
        self.space = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.hlayout.addWidget(self.cbb1)
        self.hlayout.addWidget(self.le)
        self.hlayout.addItem(self.space)

    def change_data(self, key, value):
        self._data[key] = value

    @property
    def data(self):
        return self._data

    @property
    def ui(self):
        return [self.first, self.label, self.widget]

    def activate(self):
        for key in self.le._PRESSED_KEY:
            self.editor.script.keyboard_controller.press(key)
        for key in self.le._PRESSED_KEY:
            self.editor.script.keyboard_controller.release(key)

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

    def change_data(self, section, key, value):
        self.data[section][key] = value
        self.unsave = self.data != self._data
        return True
    def read_data(self):
        if self.path.is_dir():
            self.data = werdsazxc.Dict({})
            return
        if not self.path.read_text():
            self.data = werdsazxc.Dict({
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
        self.data = werdsazxc.Dict.load_json(self.path)
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

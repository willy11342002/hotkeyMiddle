from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from ui.components.hotkey_edit import HotKeyEdit
from ui.components.editor import Editor
from ui.components.editor import EditorTabWidget
from ui.components.fileexplorer import FileLink
from ui.components.fileexplorer import FileExplorer

from trigger import KeyboardTrigger
from trigger import MouseTrigger
from utils.path import Dict
from pathlib import Path
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
        self.editor.pb_screencheck.setEnabled(not bool(idx))
        self.editor.pb_screenshot.setEnabled(not bool(idx))

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

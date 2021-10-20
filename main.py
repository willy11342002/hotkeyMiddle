from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from ui.components.fileexplorer import FileExplorer
from ui.components.fileexplorer import FileLink
from ui.components.edit import HotKeyEdit
from ui.components.edit import FileEdit
from ui.components.editor import EditorTabWidget
from ui.components.editor import Editor

from ui.main import Ui_MainWindow
from utils.path import walk
from utils.path import Dict
from utils.vk import VK
from pathlib import Path
import pynput
import sys
import ui


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
        self.editor.pb_screen_check.setEnabled(not bool(idx))
        self.editor.pb_screen_shot.setEnabled(not bool(idx))

    # 關閉腳本(關閉頁簽)
    def close_editor(self):
        idx = self.mainwindow.main_script.indexOf(self.editor)
        self.mainwindow.main_script.removeTab(idx)
        self.is_open = False

    def run_script(self):
        kwargs = Dict()
        for row in range(self.editor.tb_script.rowCount()):
            first = self.editor.tb_script.cellWidget(row, 0)
            kwargs[row] = first.activate(**kwargs)

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


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.showMaximized()

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

        script = Script(self, path)
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

        script = Script(self, path)
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

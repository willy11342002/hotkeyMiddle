from window.file_explorer import FileLink

from window.editor import Editor
from utils.path import Dict
from utils.vk import VK
from pathlib import Path
import pynput


class PynputListener:
    def __init__(self):
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

    def run_script(self):
        kwargs = Dict()
        for row in range(self.editor.tb_script.rowCount()):
            first = self.editor.tb_script.cellWidget(row, 0)
            kwargs[str(row)] = first.activate(**kwargs)

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


class Script(PynputListener):
    def __init__(self, mainwindow, path):
        # 實體化UI
        self.tree = FileLink(self, path)
        self.editor = Editor(self, path)
        # 儲存變數
        self.mainwindow = mainwindow
        self.path = path
        # 創建資料夾(文件)
        if not self.path.exists():
            if self.path.name.endswith('.ini'):
                self.path.touch()
            else:
                self.path.mkdir()

        # 修改內容顯示於標題列
        self.editor.ccb_activate.currentIndexChanged.connect(
            lambda idx: self.editor.check_saved())
        self.editor.le_start_hotkey.textChanged.connect(
            lambda idx: self.editor.check_saved())
        self.editor.le_stop_hotkey.textChanged.connect(
            lambda idx: self.editor.check_saved())
        self.editor.te_descript.textChanged.connect(
            lambda idx: self.editor.check_saved())
        self.editor.rb_once.toggled.connect(
            lambda idx: self.editor.check_saved())
        self.editor.rb_while.toggled.connect(
            lambda idx: self.editor.check_saved())

    @property
    def tab_text(self) -> str:
        if self.path.is_dir():
            return self.path.stem
        return f'{"" if self.editor.compare_data() else "* "}{self.path.stem}'

    @property
    def path(self) -> Path:
        return self._path
    @path.setter
    def path(self, path):
        try:
            self._path = path
            # 改檔案總管名稱
            self.tree.setText(0, self.tab_text)
            # 改頁籤名稱
            self.editor.check_saved()
        except AttributeError:
            pass

    # 修改頁籤名稱
    def rename_tab_text(self, tab_text):
        idx = self.mainwindow.main_script.indexOf(self.editor)
        self.mainwindow.main_script.setTabText(idx, tab_text)
    # 修改檔案名撐、UI頁籤名稱
    def rename(self, new_name):
        if new_name == self.tab_text:
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

    # 開啟腳本(建立頁簽)
    def activate_editor(self):
        self.mainwindow.main_script.setCurrentWidget(self.editor)
    def open_editor(self):
        if self.path.is_dir():
            return
        if self.editor.isHidden():
            self.mainwindow.main_script.addTab(self.editor, self.tab_text)
        self.activate_editor()

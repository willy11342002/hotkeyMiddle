from .base import BaseTrigger
from itertools import zip_longest
from utils.path import Dict
from PIL import ImageGrab
import pyautogui
import win32api
import win32gui
import win32con


class ImgCheckTrigger(BaseTrigger):
    label_text = '圖像辨識'
    DIC_ARGS = Dict({
        'lbl1': {'class_name': 'QLabel', 'default': '來源圖片:'},
        'le1': {'class_name': 'QLineEdit', 'default': '0'},
        'lbl2': {'class_name': 'QLabel', 'default': '辨識種類:'},
        'cbb': {'class_name': 'QComboBox', 'choices': ['圖片', '文字'], 'default': 0},
        'lbl3': {'class_name': 'QLabel', 'default': '辨識目標:'},
        'le3': {'class_name': 'QLineEdit', 'default': '0'},
    })
    def __init__(self, editor, data=None):
        super().__init__()
        self.editor = editor
        self._data = data or self.DEFAULT_DATA
        self.init_ui()
        self.bind_function()

    def get_monitors(self):
        return win32api.GetSystemMetrics(win32con.SM_CMONITORS)

    def get_top_left(self):
        n = self.get_monitors()
        _x, _y = pyautogui.position()
        pyautogui.moveTo(-n * pyautogui.size()[0], -n * pyautogui.size()[1])
        x, y = pyautogui.position()
        pyautogui.moveTo(_x, _y)
        return x, y

    def activate(self, **kwargs):
        source = kwargs[self.le1.text()]
        target = kwargs[self.le3.text()]
        top_left = self.get_top_left()

        location = tuple(pyautogui.locate(target, source))
        location = [
            (base + shift) if shift else base
            for base, shift in zip_longest(location, top_left)
        ]
        location = pyautogui.center(location)
        return location


class ScreenShotTrigger(BaseTrigger):
    label_text = '螢幕截圖'
    DIC_ARGS = Dict({
    })
    def __init__(self, editor, data=None):
        super().__init__()
        self.editor = editor
        self._data = data or self.DEFAULT_DATA
        self.init_ui()
        self.bind_function()

    @property
    def path(self):
        dirpath = self.editor.path.with_suffix('')
        if not dirpath.exists():
            dirpath.mkdir()
        if self.cbb.currentIndex() in [0, 1]:
            return dirpath / f'{self.le.text()}.png'
        current_img = 0
        while True:
            path = dirpath / f'{self.le.text()}({current_img}).png'
            if not path.exists():
                return path
            current_img += 1
            continue


    def activate(self, **kwargs):
        return ImageGrab.grab(all_screens=1)

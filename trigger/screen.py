from .base import BaseTrigger
from utils.path import Dict
from PIL import ImageGrab


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

    def activate(self, **kwargs):
        screenshotIm = ImageGrab.grab(all_screens=1)

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

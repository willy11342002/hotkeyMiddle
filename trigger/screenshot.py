from .base import BaseTrigger
from utils.path import Dict
from PIL import ImageGrab


class ScreenShotTrigger(BaseTrigger):
    label_text = '螢幕截圖'
    DIC_ARGS = Dict({
        'le': {'class_name': 'QLineEdit', 'default': '', 'placeholder': '存檔檔名'},
        'cbb': {'class_name': 'QComboBox', 'choices': ['覆蓋', '不覆蓋(忽略)', '不覆蓋(另存新檔)'], 'default': 0}
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


    def activate(self):
        if self.cbb.currentIndex() == 1 and self.path.exists():
            return
        screenshotIm = ImageGrab.grab(all_screens=1)
        screenshotIm.save(self.path)

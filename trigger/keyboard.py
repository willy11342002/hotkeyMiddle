from .base import BaseTrigger
from utils.path import Dict


class KeyboardTrigger(BaseTrigger):
    label_text = '鍵盤操作'
    DIC_ARGS = Dict({
        'cbb1': {'class_name': 'QComboBox', 'choices': ['點擊按鍵', '點擊組合鍵'], 'default': 0},
        'le': {'class_name': 'HotKeyEdit', 'default': []}
    })
    def __init__(self, editor, data=None):
        super().__init__()
        self.editor = editor
        self._data = data or self.DEFAULT_DATA
        self.init_ui()
        self.bind_function()
        self.cbb1.currentIndexChanged.connect(
            lambda idx: setattr(self.le, 'single_mode', not bool(idx)))

    def activate(self):
        for key in self.le._PRESSED_KEY:
            self.editor.script.keyboard_controller.press(key)
        for key in self.le._PRESSED_KEY:
            self.editor.script.keyboard_controller.release(key)

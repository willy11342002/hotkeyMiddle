from .base import BaseTrigger
from utils.path import Dict
import pynput


class MouseTrigger(BaseTrigger):
    label_text = '滑鼠操作'
    DIC_ARGS = Dict({
        'cbb1': {'class_name': 'QComboBox', 'choices': ['單擊', '雙擊'], 'default': 0},
        'cbb2': {'class_name': 'QComboBox', 'choices': ['左鍵', '中鍵', '右鍵'], 'default': 0}
    })
    def __init__(self, editor, data=None):
        super().__init__()
        self.editor = editor
        self._data = data or self.DEFAULT_DATA
        self.init_ui()
        self.bind_function()

    def activate(self, **kwargs):
        btn = dict(enumerate([
            pynput.mouse.Button.left,
            pynput.mouse.Button.middle,
            pynput.mouse.Button.right,
        ]))[self.data['cbb2']]
        self.editor.script.mouse_controller.click(
            btn,
            self.data['cbb1']+1
        )


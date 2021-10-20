from .base import BaseTrigger
from utils.path import Dict
import pyautogui
import pynput


class MouseTrigger(BaseTrigger):
    label_text = '滑鼠操作'
    DIC_ARGS = Dict({
        'cbb0': {'class_name': 'QComboBox', 'choices': ['點擊', '滾輪', '移動'], 'default': 0},
        # 點擊功能
        'cbb1': {'class_name': 'QComboBox', 'choices': ['單擊', '雙擊'], 'default': 0},
        'cbb2': {'class_name': 'QComboBox', 'choices': ['左鍵', '中鍵', '右鍵'], 'default': 0},
        # 滾輪功能
        'cbb3': {'class_name': 'QComboBox', 'choices': ['向上滾動', '向下滾動'], 'default': 0},
        # 移動功能
        'le': {'class_name': 'QLineEdit', 'default': '0'},
    })
    def __init__(self, editor, data=None):
        super().__init__()
        self.editor = editor
        self._data = data or self.DEFAULT_DATA
        self.init_ui()
        self.bind_function()
        self.switch_function(self.cbb0.currentIndex())
        self.cbb0.currentIndexChanged.connect(self.switch_function)

    def switch_function(self, idx):
        self.cbb1.hide()
        self.cbb2.hide()
        self.cbb3.hide()
        self.le.hide()
        if idx == 0:
            self.cbb1.show()
            self.cbb2.show()
        if idx == 1:
            self.cbb3.show()
        if idx == 2:
            self.le.show()

    def activate(self, **kwargs):
        try:
            if self.cbb0.currentIndex() == 0:
                btn = dict(enumerate([
                    pynput.mouse.Button.left,
                    pynput.mouse.Button.middle,
                    pynput.mouse.Button.right,
                ]))[self.data['cbb2']]
                self.editor.script.mouse_controller.click(
                    btn,
                    self.data['cbb1']+1
                )
            elif self.cbb0.currentIndex() == 1:
                if self.cbb3.currentIndex() == 0:
                    shift = 1
                else:
                    shift = -1
                pyautogui.scroll(shift)
            else:
                position = kwargs[self.le.text()]
                pyautogui.moveTo(position)
        except:
            return None
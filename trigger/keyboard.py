from utils.path import Dict
from .base import BaseTrigger
import pynput


class KeyboardClickTrigger(BaseTrigger):
    controller = pynput.keyboard.Controller()
    TITLE = '單擊鍵盤'
    INFORMATION = (
        '點擊設定的按鍵'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'keys': {
                'class_name': 'HotKeyEdit', 'name': '按鍵設定',
                'single_mode': True, 'fixed': [], 'variable': '0'},
        }
    })

    def activate(self, *args, **kwargs):
        for key in self.keys.value_widget._PRESSED_KEY:
            self.controller.press(key)
            self.controller.release(key)


class HotkeyClickTrigger(BaseTrigger):
    controller = pynput.keyboard.Controller()
    TITLE = '鍵盤快速鍵'
    INFORMATION = (
        '來源(str)： 無\n\n'
        '點擊所設定的快速鍵'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'keys': {
                'class_name': 'HotKeyEdit', 'name': '按鍵設定',
                'single_mode': False, 'fixed': [], 'variable': '0'},
        }
    })

    def activate(self, *args, **kwargs):
        for key in self.keys.value_widget._PRESSED_KEY:
            self.controller.press(key)
        for key in self.keys.value_widget._PRESSED_KEY:
            self.controller.release(key)

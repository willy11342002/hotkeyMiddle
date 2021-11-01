from utils.path import Dict
from .base import BaseTrigger
import pynput


class CopyTrigger(BaseTrigger):
    controller = pynput.keyboard.Controller()
    TITLE = '剪貼簿複製'
    INFORMATION = ''
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
        }
    })

    def activate(self, *args, **kwargs):
        keys = [
            pynput.keyboard.Key.ctrl,
            pynput.keyboard.KeyCode.from_char('c')
        ]
        for key in keys:
            self.controller.press(key)
        for key in keys:
            self.controller.release(key)


class PasteTrigger(BaseTrigger):
    controller = pynput.keyboard.Controller()
    TITLE = '剪貼簿貼上'
    INFORMATION = ''
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
        }
    })

    def activate(self, *args, **kwargs):
        keys = [
            pynput.keyboard.Key.ctrl,
            pynput.keyboard.KeyCode.from_char('v')
        ]
        for key in keys:
            self.controller.press(key)
        for key in keys:
            self.controller.release(key)


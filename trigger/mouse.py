from utils.path import Dict
from .base import BaseTrigger
import pynput


class MouseClickTrigger(BaseTrigger):
    controller = pynput.mouse.Controller()
    TITLE = '點擊滑鼠'
    INFORMATION = (
        '來源(str)： 無\n\n'
        '滑鼠按鈕:  選擇左鍵，點擊左鍵\n'
        '　　　　   選擇中鍵，點擊中鍵\n'
        '　　　　   選擇右鍵，點擊右鍵\n\n'
        '點擊次數:  選擇單擊，點擊一次\n'
        '　　　　   選擇雙擊，點擊兩次'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'button': {'class_name': 'ComboBox', 'name': '滑鼠按鈕', 'choices': ['左鍵', '中鍵', '右鍵'], 'default': 0},
            'times': {'class_name': 'ComboBox', 'name': '點擊次數', 'choices': ['單擊', '雙擊'], 'default': 0},
        }
    })

    def activate(self, *args, **kwargs):
        dic_buttons = dict(enumerate([
            pynput.mouse.Button.left,
            pynput.mouse.Button.middle,
            pynput.mouse.Button.right,
        ]))
        button = dic_buttons[self.button.currentIndex()]
        count = self.times.currentIndex() + 1
        self.controller.click(button, count)

from utils.path import Dict
from .base import BaseTrigger
import pynput


class MouseClickTrigger(BaseTrigger):
    controller = pynput.mouse.Controller()
    TITLE = '點擊滑鼠'
    INFORMATION = (
        '滑鼠按鈕:  選擇左鍵，點擊左鍵\n'
        '　　　　   選擇中鍵，點擊中鍵\n'
        '　　　　   選擇右鍵，點擊右鍵\n\n'
        '點擊次數:  選擇單擊，點擊一次\n'
        '　　　　   選擇雙擊，點擊兩次'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'button': {
                'class_name': 'ComboBox', 'name': '滑鼠按鈕',
                'choices': ['左鍵', '中鍵', '右鍵'], 'fixed': 0, 'variable': '0'},
            'times': {
                'class_name': 'ComboBox', 'name': '點擊次數',
                'choices': ['單擊', '雙擊'], 'fixed': 0, 'variable': '0'},
        }
    })

    def activate(self, *args, **kwargs):
        dic_buttons = dict(enumerate([
            pynput.mouse.Button.left,
            pynput.mouse.Button.middle,
            pynput.mouse.Button.right,
        ]))
        sources = super().activate(*args, **kwargs)
        button = dic_buttons[sources.button]
        count = sources.times + 1
        self.controller.click(button, count)


class MouseScrollTrigger(BaseTrigger):
    controller = pynput.mouse.Controller()
    TITLE = '滾動滑鼠'
    INFORMATION = (
        '方向:  選擇向上滾動，滾輪向上滾動\n'
        '　　   選擇向下滾動，滾輪向下滾動\n\n'
        '滾動次數:  輸入要滾動的次數'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'forward': {
                'class_name': 'ComboBox', 'name': '方向',
                'choices': ['向上滾動', '向下滾動'], 'fixed': 0, 'variable': '0'},
            'step': {
                'class_name': 'SpinBox', 'name': '滾動次數', 'fixed': 0, 'variable': '0'},
        }
    })

    def activate(self, *args, **kwargs):
        sources = super().activate(*args, **kwargs)
        if sources.forward == 0:
            forward = 1
        else:
            forward = -1
        self.controller.scroll(0, forward*sources.step)

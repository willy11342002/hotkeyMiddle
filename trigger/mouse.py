from utils.path import Dict
from .base import BaseTrigger
import traceback
import pyautogui
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

    def activate(self, logger, *args, **kwargs):
        try:
            sources = super().activate(*args, **kwargs)
            dic_buttons = dict(enumerate([
                pynput.mouse.Button.left,
                pynput.mouse.Button.middle,
                pynput.mouse.Button.right,
            ]))
            button = dic_buttons[sources.button]
            count = sources.times + 1
            self.controller.click(button, count)

            logger.info(f'【{self.TITLE}】')
            logger.info(f'點擊{self.DIC_DEFAULT.other.button.choices[sources.button]}'f'{count}次')
            logger.info('執行成功。')
        except:
            logger.info('執行失敗。')
            logger.critical('\n' + traceback.format_exc())


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

    def activate(self, logger, *args, **kwargs):
        try:
            sources = super().activate(*args, **kwargs)
            logger.info(f'【{self.TITLE}】')
            logger.info(f'{self.DIC_DEFAULT.other.forward.choices[sources.forward]}'f'{sources.step}次')
            if sources.forward == 0:
                forward = 1
            else:
                forward = -1
            self.controller.scroll(0, forward*sources.step)
            logger.info('執行成功。')
        except:
            logger.info('執行失敗。')
            logger.critical('\n' + traceback.format_exc())


class MouseMoveTrigger(BaseTrigger):
    controller = pynput.mouse.Controller()
    TITLE = '滑鼠移動'
    INFORMATION = '將滑鼠移動至指定位置'
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'pos': {
                'class_name': 'PositionBox', 'name': '座標',
                'source': 0, 'fixed': [0, 0], 'variable': '0'},
        }
    })

    def activate(self, logger, *args, **kwargs):
        try:
            sources = super().activate(*args, **kwargs)
            pyautogui.moveTo(*sources.pos)
            logger.info(f'【{self.TITLE}】')
            logger.info(f'將滑鼠移動至{sources.pos}位置')
            logger.info('執行成功。')
        except:
            logger.info('執行失敗。')
            logger.critical('\n' + traceback.format_exc())

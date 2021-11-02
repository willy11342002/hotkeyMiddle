from utils.path import Dict
from .base import BaseTrigger
from PIL import ImageGrab
import pyautogui
import win32con
import win32api

class PrintScreenTrigger(BaseTrigger):
    TITLE = '螢幕截圖'
    INFORMATION = (
        '來源(str)： 無\n\n'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
        }
    })

    def activate(self, *args, **kwargs):
        return ImageGrab.grab(all_screens=1)


class ScreenCheckTrigger(BaseTrigger):
    TITLE = '圖片定位'
    INFORMATION = (
        '來源圖片： 前置步驟中截圖(開啟檔案)取得的圖片檔。\n'
        '目標圖片： 將要在來源圖片中定位的目標。\n'
        '灰階查找： 是否將圖片轉為灰階進行定位。\n'
        '信心度： 定位結果的信心度設定。'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'source_img': {
                'class_name': 'FileEdit', 'name': '來源圖片',
                'method': 'getOpenFileName', 'types': 'All files(*)',
                'default': 1, 'fixed': 'data', 'variable': '0',
            },
            'target_img': {
                'class_name': 'FileEdit', 'name': '目標圖片',
                'method': 'getOpenFileName', 'types': 'All files(*)',
                'default': 1, 'fixed': 'data', 'variable': '0',
            },
            'grayscale': {
                'class_name': 'ComboBox', 'name': '灰階查找',
                'choices': ['否', '是'], 'fixed': 0, 'variable': '0',
            },
            'confidence': {
                'class_name': 'DoubleSpinBox', 'name': '信心度',
                'fixed': 0, 'variable': '1.0',
            },
        }
    })

    def get_top_left(self, n):
        _x, _y = pyautogui.position()
        pyautogui.moveTo(-n * pyautogui.size()[0], -n * pyautogui.size()[1])
        x, y = pyautogui.position()
        pyautogui.moveTo(_x, _y)
        return x, y

    def activate(self, *args, **kwargs):
        sources = super().activate(*args, **kwargs)
        x, y = self.get_top_left(
            win32api.GetSystemMetrics(win32con.SM_CMONITORS))
        print(sources)
        pos = pyautogui.locate(
            sources.target_img,
            sources.source_img,
            grayscale=bool(sources.grayscale),
            confidence=sources.confidence,
        )
        print(pos)
        pos = pyautogui.center(pos)
        pos = (pos[0] + x, pos[1] + y)
        print(pos)
        return pos


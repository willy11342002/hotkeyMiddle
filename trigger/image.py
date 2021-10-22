from utils.path import Dict
from .base import BaseTrigger
from PIL import ImageGrab


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

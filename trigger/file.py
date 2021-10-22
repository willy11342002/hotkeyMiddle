from utils.path import Dict
from .base import BaseTrigger


class FileLoadTrigger(BaseTrigger):
    TITLE = '讀取檔案'
    INFORMATION = (
        '來源(str)： 輸入要開啟的檔案路徑\n\n'
        '檔案類型:  選擇圖檔，返回 PIL.Image 類型\n'
        '　　　　   選擇文字檔，返回 str 類型\n'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'file_type': {'class_name': 'ComboBox', 'name': '檔案類型', 'choices': ['圖檔', '文字檔'], 'default': 0}
        }
    })

    def activate(self, *args, **kwargs):
        pass


class FileSaveTrigger(BaseTrigger):
    TITLE = '儲存檔案'
    INFORMATION = (
        '來源(str)： 輸入要儲存的檔案路徑\n\n'
        '檔案類型:  選擇圖檔，返回 PIL.Image 類型\n'
        '　　　　   選擇文字檔，返回 str 類型\n'
        '複寫: 選擇總是覆蓋，每次執行將覆蓋舊檔\n\n'
        '　　  選擇忽略，若檔案存在就不會重覆執行存檔動作\n'
        '　　  選擇另存新檔，將在檔案目錄建立新檔儲存\n'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'file_type': {'class_name': 'ComboBox', 'name': '檔案類型', 'choices': ['圖檔', '文字檔'], 'default': 0},
            'over_write': {'class_name': 'ComboBox', 'name': '覆寫', 'choices': ['總是覆蓋', '忽略', '另存新檔'], 'default': 0},
        }
    })

    def activate(self, *args, **kwargs):
        pass

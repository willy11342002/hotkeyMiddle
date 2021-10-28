from pathlib import Path
from utils.path import Dict
from .base import BaseTrigger
from PIL import Image


class FileLoadTrigger(BaseTrigger):
    TITLE = '讀取檔案'
    NEED_SOURCE = True
    INFORMATION = (
        '檔案類型:  選擇圖檔，返回 PIL.Image 類型\n'
        '　　　　   選擇文字檔，返回 str 類型\n\n'
        '檔案路徑:  要讀取的目標檔案路徑\n\n'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'file_type': {
                'class_name': 'ComboBox', 'name': '檔案類型',
                'choices': ['圖檔', '文字檔'], 'fixed': 0, 'variable': '0'},
            'file_path': {
                'class_name': 'FileEdit', 'name': '檔案路徑',
                'method': 'getOpenFileName', 'types': 'All files(*)',
                'source': 0, 'fixed': 'data', 'variable': '0',
            }
        }
    })

    def activate(self, *args, **kwargs):
        sources = super().activate(*args, **kwargs)
        if sources.file_type == 0:
            return Image.open(sources.file_path)
        return sources.file_path.read_text(encoding='utf8')


class FileSaveTrigger(BaseTrigger):
    TITLE = '儲存檔案'
    NEED_SOURCE = True
    INFORMATION = (
        '存檔內容:  要儲存的檔案內容\n\n'
        '存檔路徑:  要儲存的目標檔案路徑\n\n'
        '檔案類型:  選擇圖檔，返回 PIL.Image 類型\n'
        '　　　　   選擇文字檔，返回 str 類型\n\n'
        '複寫: 選擇總是覆蓋，每次執行將覆蓋舊檔\n'
        '　　  選擇忽略，若檔案存在就不會重覆執行存檔動作\n'
        '　　  選擇另存新檔，將在檔案目錄建立新檔儲存\n'
    )
    DIC_DEFAULT = Dict({
        **BaseTrigger.DIC_DEFAULT,
        'other': {
            'write_content': {
                'class_name': 'TextEdit', 'name': '存檔內容',
                'source': 1, 'fixed': '', 'variable': '0',
            },
            'file_path': {
                'class_name': 'FileEdit', 'name': '檔案路徑',
                'method': 'getSaveFileName', 'types': 'All files(*)',
                'source': 0, 'fixed': 'data', 'variable': '0',
            },
            'file_type': {
                'class_name': 'ComboBox', 'name': '檔案類型',
                'choices': ['圖檔', '文字檔'], 'fixed': 0, 'variable': '0'},
            'over_write': {
                'class_name': 'ComboBox', 'name': '覆寫',
                'choices': ['總是覆蓋', '忽略', '另存新檔'], 'fixed': 0, 'variable': '0'},
        }
    })

    def activate(self, *args, **kwargs):
        sources = super().activate(*args, **kwargs)
        file_path = Path(sources.file_path)
        if not file_path.exists():
            file_path = sources.file_path
        elif sources.over_write == 0:
            file_path = sources.file_path
        elif sources.over_write == 1:
            return True
        elif sources.over_write == 2:
            cnt = len([f for f in file_path.parent.iterdir() if f.stem in str(f)])
            file_path = file_path.parent / f'{file_path.stem} ({cnt}).{file_path.suffix}'

        if sources.file_type == 0:
            if isinstance(sources.write_content, Image.Image):
                sources.write_content.save(file_path)
                return True
            else:
                return False

        file_path.write_text(
            sources.write_content,
            encoding='utf8')
        return True

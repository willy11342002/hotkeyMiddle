from pathlib import Path

from PIL import Image
from .base import BaseTrigger
from utils.path import Dict
import filetype


class FileLoadTrigger(BaseTrigger):
    label_text = '讀取檔案'
    DIC_ARGS = Dict({
        'fe': {'class_name': 'FileEdit', 'method': 'getOpenFileName',
               'default': 'data', 'types': 'All files(*)'}
    })
    def __init__(self, editor, data=None):
        super().__init__()
        self.editor = editor
        self._data = data or self.DEFAULT_DATA
        self.init_ui()
        self.bind_function()

    @property
    def DEFAULT_DATA(self):
        dic = super().DEFAULT_DATA
        dic.fe = self.editor.path.parent / 'files'
        return dic

    def activate(self, **kwargs):
        filepath = Path(self.fe.text())
        guess = filetype.guess(self.fe.text())
        if guess and guess.mime.startswith('image'):
            return Image.open(filepath)
        return filepath.read_text(encoding='utf8')

class FileSaveTrigger(BaseTrigger):
    label_text = '儲存檔案'
    DIC_ARGS = Dict({
        'lbl1': {'class_name': 'QLabel', 'default': '來源：'},
        'le': {'class_name': 'QLineEdit', 'default': '0'},
        'lbl2': {'class_name': 'QLabel', 'default': '儲存位置：'},
        'fe': {'class_name': 'FileEdit', 'method': 'getSaveFileName',
               'default': 'data'},
        'lbl3': {'class_name': 'QLabel', 'default': '是否覆蓋：'},
        'cbb': {'class_name': 'QComboBox', 'choices': ['覆蓋', '不覆蓋(忽略)', '不覆蓋(另存新檔)'], 'default': 0}
    })
    def __init__(self, editor, data=None):
        super().__init__()
        self.editor = editor
        self._data = data or self.DEFAULT_DATA
        self.init_ui()
        self.bind_function()

    @property
    def DEFAULT_DATA(self):
        dic = super().DEFAULT_DATA
        dic.fe = self.editor.path.parent / 'files'
        return dic

    def activate(self, **kwargs):
        content = kwargs.get(self.le.text())
        filepath = Path(self.fe.text())
        if not filepath.parent.exists():
            filepath.parent.mkdir()

        if self.cbb.currentIndex() == 0:
            count = 0
        if self.cbb.currentIndex() == 1:
            return None
        if self.cbb.currentIndex() == 2:
            filter_rule = lambda p: p.is_file() and filepath.stem in str(p)
            count = len(list(filter(filter_rule, filepath.parent.iterdir())))

        if count:
            filepath = filepath.parent / f'{filepath.stem}({count}){filepath.suffix}'

        if type(content) == Image:
            content.save(filepath)
        elif type(content) == str:
            filepath.write_text(content, encoding='utf8')
        else:
            filepath.write_bytes(content)

        return None
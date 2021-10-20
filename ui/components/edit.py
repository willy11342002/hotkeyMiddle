from PyQt5 import QtWidgets
from PyQt5 import QtCore
from pathlib import Path
from utils.vk import VK
import pynput


class FileEdit(QtWidgets.QPushButton):
    textChanged = QtCore.pyqtSignal(str)
    def __init__(self, path=None, method=None, types=None):
        super().__init__()
        self.path = path or Path('data')
        self.method = method or 'getOpenFileName'
        self.types = types or 'All files(*)'
        self.clicked.connect(self.choose_path)

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, p):
        self._path = p
        self.setText(str(p.absolute()))
        self.textChanged.emit(str(p.absolute()))

    def choose_path(self):
        filename, ok = getattr(QtWidgets.QFileDialog, self.method)(
            self, '選擇檢查檔', str(self.path.parent), self.types)
        if not ok:
            return
        self.path = Path(filename)


class HotKeyEdit(QtWidgets.QLineEdit):
    _PRESSED_KEY = set()
    def __init__(self, master=None, single_mode=False, *args, **kwargs):
        self.single_mode = single_mode
        super().__init__(master, *args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_InputMethodEnabled, False)

    @property
    def PRESSED_KEY_VK(self):
        return list(map(lambda key: key.vk, self._PRESSED_KEY))
    @PRESSED_KEY_VK.setter
    def PRESSED_KEY_VK(self, vks):
        self._PRESSED_KEY = set(map(pynput.keyboard.KeyCode.from_vk, vks))
        self.setText('+'.join(self.PRESSED_KEY_STR))
    @property
    def PRESSED_KEY_STR(self):
        return list(map(VK.get_string_from_vk, self.PRESSED_KEY_VK))

    # 按鍵綁定
    def focusInEvent(self, event):
        self._PRESSED_KEY.clear()
        return super().focusInEvent(event)
    def focusOutEvent(self, event):
        self.PRESSED_KEY_VK = [VK.get_vk_from_string(txt) for txt in self.text().split('+')]
        return super().focusOutEvent(event)
    def keyPressEvent(self, event):
        if self.single_mode and self._PRESSED_KEY:
            return
        vk = VK.get_vk_from_key(event)
        pkey = pynput.keyboard.KeyCode.from_vk(vk)
        self._PRESSED_KEY.add(pkey)
        self.setText('+'.join(self.PRESSED_KEY_STR))
    def keyReleaseEvent(self, event):
        vk = VK.get_vk_from_key(event)
        pkey = pynput.keyboard.KeyCode.from_vk(vk)
        self._PRESSED_KEY.discard(pkey)
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from utils.vk import VK
import pynput


class HotKeyEdit(QtWidgets.QLineEdit):
    _PRESSED_KEY = set()
    sig_current_changed = QtCore.pyqtSignal()
    def __init__(self, master=None, single_mode=False, *args, **kwargs):
        self.single_mode = single_mode
        super().__init__(master, *args, **kwargs)
        self.textChanged.connect(self.sig_current_changed.emit)
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

    @classmethod
    def from_value(cls, value):
        obj = cls()
        obj.single_mode = value.single_mode
        obj.PRESSED_KEY_VK = value.fixed
        return obj
    @property
    def current(self):
        return self.PRESSED_KEY_VK
    @current.setter
    def current(self, PRESSED_KEY_VK):
        self.PRESSED_KEY_VK = PRESSED_KEY_VK

import pynput._util.win32_vks as VK
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import pynput


class HotKeyEdit(QtWidgets.QLineEdit):
    DIC_VIRTUALKEY = {v:k for k, v in vars(VK).items() if type(v) == int}
    DIC_VIRTUALKEY = {
        **DIC_VIRTUALKEY,
        18: "ALT", 192: "`", 27: "ESC", 33: "PAGE UP", 34: "PAGE DOWN",
        111: "NUMPAD/", 106: "NUMPAD*", 107: "NUMPAD+", 109: "NUMPAD-", 110: "NUMPAD.",
        49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54:"6", 55: "7", 56: "8", 57: "9", 58: "0",
        65: "A", 66: "B", 67: "C", 68: "D", 69: "E", 70:"F", 71: "G", 72: "H", 73: "I", 74: "J",
        75: "K", 76: "L", 77: "M", 78: "N", 79: "O", 80:"P", 81: "Q", 82: "R", 83: "S", 84: "T",
        85: "U", 86: "V", 87: "W", 88: "X", 89: "Y", 90:"Z"
    }
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
        return list(map(self.get_human_key, self.PRESSED_KEY_VK))

    # 字元轉換
    def get_human_key(self, vk):
        hkey = self.DIC_VIRTUALKEY.get(vk, 'Unknow')
        return hkey
    def get_vk(self, event):
        return event.nativeVirtualKey()
    # 按鍵綁定
    def keyPressEvent(self, event):
        if self.single_mode and self._PRESSED_KEY:
            return
        vk = self.get_vk(event)
        pkey = pynput.keyboard.KeyCode.from_vk(vk)
        self._PRESSED_KEY.add(pkey)
        self.setText('+'.join(self.PRESSED_KEY_STR))
    def keyReleaseEvent(self, event):
        try:
            vk = self.get_vk(event)
            pkey = pynput.keyboard.KeyCode.from_vk(vk)
            self._PRESSED_KEY.remove(pkey)
        except KeyError as e:
            pass


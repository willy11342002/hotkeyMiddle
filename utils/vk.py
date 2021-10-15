from pynput._util import win32_vks
from PyQt5 import QtGui


class VK:
    DIC_VIRTUALKEY = {v:k for k, v in vars(win32_vks).items() if type(v) == int}
    DIC_VIRTUALKEY = {
        **DIC_VIRTUALKEY,
        18: "ALT", 192: "`", 27: "ESC", 33: "PAGE UP", 34: "PAGE DOWN",
        111: "NUMPAD/", 106: "NUMPAD*", 107: "NUMPAD+", 109: "NUMPAD-", 110: "NUMPAD.",
        49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54:"6", 55: "7", 56: "8", 57: "9", 58: "0",
        65: "A", 66: "B", 67: "C", 68: "D", 69: "E", 70:"F", 71: "G", 72: "H", 73: "I", 74: "J",
        75: "K", 76: "L", 77: "M", 78: "N", 79: "O", 80:"P", 81: "Q", 82: "R", 83: "S", 84: "T",
        85: "U", 86: "V", 87: "W", 88: "X", 89: "Y", 90:"Z"
    }
    DIC_REVERSE_VIRTUALKEY = {
        v: k for k, v in DIC_VIRTUALKEY.items()
    }

    @classmethod
    def get_vk_from_string(cls, string):
        return cls.DIC_REVERSE_VIRTUALKEY[string]

    @classmethod
    def get_string_from_vk(cls, vk):
        return cls.DIC_VIRTUALKEY[vk]

    @classmethod
    def get_vk_from_key(cls, key):
        # QT物件
        if type(key) == QtGui.QKeyEvent:
            return key.nativeVirtualKey()
        # pynput物件
        vk = getattr(key, 'vk', None)
        if not vk:
            vk = {
                'alt_l': 18, 'alt_r': 18,
                'shift_l': 16, 'shift_r': 16,
                'ctrl_l': 17, 'ctrl_r': 17,
            }.get(key._name_)
        if not vk:
            vk = key._value_.vk
        return vk

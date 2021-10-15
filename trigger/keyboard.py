from ui.component import HotKeyEdit
from .base import BaseTrigger
from PyQt5 import QtWidgets
from utils.path import Dict


class KeyboardTrigger(BaseTrigger):
    def __init__(self, editor, data=None):
        super().__init__()
        self.editor = editor
        self._data = data or Dict({
            'class_name': self.__class__.__name__,
            'cbb1': 0,
            'le': []
        })
        self.init_ui()
        self.first.data = self.data
        self.first.activate = self.activate
        self.pb_delete.clicked.connect(lambda: editor.remove_trigger(self))
        self.pb_up.clicked.connect(lambda: editor.move_up_trigger(self))
        self.pb_down.clicked.connect(lambda: editor.move_down_trigger(self))

        self.cbb1.currentIndexChanged.connect(
            lambda idx: self.change_data('cbb1', idx))
        self.le.textChanged.connect(
            lambda txt: self.change_data('le', self.le.PRESSED_KEY_VK))

    def init_ui(self):
        self.hlayout1 = QtWidgets.QHBoxLayout(self.first)
        self.pb_up = QtWidgets.QPushButton()
        self.pb_up.setText('↑')
        self.pb_delete = QtWidgets.QPushButton()
        self.pb_delete.setText('X')
        self.pb_down = QtWidgets.QPushButton()
        self.pb_down.setText('↓')
        self.hlayout1.addWidget(self.pb_up)
        self.hlayout1.addWidget(self.pb_delete)
        self.hlayout1.addWidget(self.pb_down)

        self.label.setText('鍵盤操作')

        self.hlayout2 = QtWidgets.QHBoxLayout(self.widget)
        self.cbb1 = QtWidgets.QComboBox(self.widget)
        self.cbb1.addItem('點擊按鍵')
        self.cbb1.addItem('點擊組合鍵')
        self.cbb1.setCurrentIndex(self.data['cbb1'])
        self.le = HotKeyEdit(single_mode=True)
        self.le.PRESSED_KEY_VK = self.data['le']
        self.space = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout2.addWidget(self.cbb1)
        self.hlayout2.addWidget(self.le)
        self.hlayout2.addItem(self.space)

    def activate(self):
        for key in self.le._PRESSED_KEY:
            self.editor.script.keyboard_controller.press(key)
        for key in self.le._PRESSED_KEY:
            self.editor.script.keyboard_controller.release(key)

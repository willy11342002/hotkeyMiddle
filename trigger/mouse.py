from .base import BaseTrigger
from PyQt5 import QtWidgets
from utils.path import Dict
import pynput


class MouseTrigger(BaseTrigger):
    def __init__(self, editor, data=None):
        super().__init__()
        self.editor = editor
        self._data = data or Dict({
            'class_name': self.__class__.__name__,
            'cbb1': 0,
            'cbb2': 0
        })
        self.init_ui()
        self.first.data = self.data
        self.first.activate = self.activate
        self.pb_delete.clicked.connect(lambda: editor.remove_trigger(self))
        self.pb_up.clicked.connect(lambda: editor.move_up_trigger(self))
        self.pb_down.clicked.connect(lambda: editor.move_down_trigger(self))

        self.cbb1.currentIndexChanged.connect(
            lambda idx: self.change_data('cbb1', idx))
        self.cbb2.currentIndexChanged.connect(
            lambda idx: self.change_data('cbb2', idx))

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

        self.label.setText('滑鼠操作')

        self.hlayout = QtWidgets.QHBoxLayout(self.widget)
        self.cbb1 = QtWidgets.QComboBox(self.widget)
        self.cbb1.addItems(['單擊', '雙擊'])
        self.cbb1.setCurrentIndex(self.data['cbb1'])
        self.cbb2 = QtWidgets.QComboBox(self.widget)
        self.cbb2.addItems(['左鍵', '中鍵', '右鍵'])
        self.cbb2.setCurrentIndex(self.data['cbb2'])
        self.space = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout.addWidget(self.cbb1)
        self.hlayout.addWidget(self.cbb2)
        self.hlayout.addItem(self.space)

    def activate(self):
        btn = dict(enumerate([
            pynput.mouse.Button.left,
            pynput.mouse.Button.middle,
            pynput.mouse.Button.right,
        ]))[self.data['cbb2']]
        self.editor.script.mouse_controller.click(
            btn,
            self.data['cbb1']+1
        )


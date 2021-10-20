from ui.components.edit import HotKeyEdit
from ui.components.edit import FileEdit
from PyQt5 import QtWidgets
from utils.path import Dict
from pathlib import Path


class BaseTrigger:
    label_text = ''
    def __init__(self):
        self._data = Dict()

        # 生成畫面元素
        self.first = QtWidgets.QWidget()
        self.label = QtWidgets.QLabel()
        self.widget = QtWidgets.QWidget()

        # 生成操作按鈕
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

        # 觸發指令文字設定
        self.label.setText(self.label_text)

    def bind_function(self):
        self.first.data = self.data
        self.first.activate = self.activate
        self.pb_delete.clicked.connect(lambda: self.editor.remove_trigger(self))
        self.pb_up.clicked.connect(lambda: self.editor.move_up_trigger(self))
        self.pb_down.clicked.connect(lambda: self.editor.move_down_trigger(self))

    def init_ui(self):
        # 生成參數
        self.hlayout = QtWidgets.QHBoxLayout(self.widget)
        for key, value in self.DIC_ARGS.items():
            if value.class_name == 'QLabel':
                obj = QtWidgets.QLabel()
                obj.setText(self.data.get(key, ''))
            if value.class_name == 'QLineEdit':
                obj = QtWidgets.QLineEdit()
                obj.setPlaceholderText(value.placeholder)
                obj.setText(self.data[key])
                obj.textChanged.connect(
                    lambda txt, key=key, obj=obj: self.change_data(key, obj.text()))
            if value.class_name == 'QComboBox':
                obj = QtWidgets.QComboBox()
                obj.addItems(value.choices)
                obj.setCurrentIndex(self.data[key])
                obj.currentIndexChanged.connect(
                    lambda idx, key=key, obj=obj: self.change_data(key, obj.currentIndex()))
            if value.class_name == 'FileEdit':
                obj = FileEdit(path=Path(self.data.get(key, 'data')) ,method=value.method, types=value.types)
                obj.textChanged.connect(
                    lambda txt, key=key, obj=obj: self.change_data(key, obj.text()))
            if value.class_name == 'HotKeyEdit':
                obj = HotKeyEdit(single_mode=True)
                obj.PRESSED_KEY_VK = self.data[key]
                obj.textChanged.connect(
                    lambda txt, key=key, obj=obj: self.change_data(key, obj.PRESSED_KEY_VK))
            setattr(self, key, obj)
            self.hlayout.addWidget(obj)

        self.space = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlayout.addItem(self.space)

    def change_data(self, key, value):
        self._data[key] = value

    @property
    def DEFAULT_DATA(self):
        return Dict({
            'class_name': self.__class__.__name__,
            **{k: v.default for k, v in self.DIC_ARGS.items()}
        })

    @property
    def data(self):
        return self._data

    @property
    def ui(self):
        return [self.first, self.label, self.widget]

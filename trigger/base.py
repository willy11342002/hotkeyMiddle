from PyQt5 import QtWidgets
from PyQt5 import QtCore
from ui.trigger import Ui_Form
from utils.path import Dict
import components


class ArgsWidget(QtWidgets.QWidget):
    sig_current_changed = QtCore.pyqtSignal()
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        self.h = QtWidgets.QHBoxLayout(self)

        self.ccb_source = QtWidgets.QComboBox()
        self.ccb_source.addItems(['固定值', '從前置步驟'])
        self.ccb_source.setDisabled(value.source is None)

        self.value_widget = getattr(components, value.class_name).from_value(value)
        self.le_source_variable = components.SourceEdit()
        self.le_source_variable.hide()
        space = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.h.addWidget(self.ccb_source)
        self.h.addWidget(self.value_widget)
        self.h.addWidget(self.le_source_variable)
        self.h.addItem(space)

        self.ccb_source.currentIndexChanged.connect(self.switch_source)
        self.value_widget.sig_current_changed.connect(self.sig_current_changed)

        self.current = value

    @property
    def current(self):
        return Dict({
            'source': self.ccb_source.currentIndex(),
            'fixed': self.value_widget.current,
            'variable': self.le_source_variable.text()
        })
    @current.setter
    def current(self, value):
        self.ccb_source.setCurrentIndex(value.source or value.default or 0)
        self.value_widget.current = value.fixed
        self.le_source_variable.setText(str(value.variable))

    def get_source(self, sources):
        current = self.current
        if current.source == 0:
            return current.fixed
        return sources[current.variable]

    def switch_source(self, idx):
        if idx == 0:
            self.le_source_variable.hide()
            self.value_widget.show()
        else:
            self.value_widget.hide()
            self.le_source_variable.show()


class BaseTrigger:
    TITLE = ''
    INFORMATION = ''
    NEED_SOURCE = False
    DIC_DEFAULT = Dict({
        'other': {},
    })
    _row = 0
    class Trigger(QtWidgets.QWidget, Ui_Form):
        def __init__(self, manager, data, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setupUi(self)
            self.manager = manager
            self.lbl_title.setText(manager.TITLE)
            self.lbl_information.setText(manager.INFORMATION)
            for i, (key, value) in enumerate(data.other.items()):
                name_widget = QtWidgets.QLabel(f'{value.name}：')
                value_widget = ArgsWidget(value)
                value_widget.le_source_variable.right = self
                self.formLayout_2.setWidget(i, QtWidgets.QFormLayout.LabelRole, name_widget)
                self.formLayout_2.setWidget(i, QtWidgets.QFormLayout.FieldRole, value_widget)
                value_widget.sig_current_changed.connect(self.manager.editor.check_saved)
                setattr(self, key, value_widget)
                setattr(self.manager, key, value_widget)

        @property
        def row(self):
            return self.manager.row
        @row.setter
        def row(self, row):
            self.manager.row = row

        @property
        def data(self):
            return self.manager.data

    @property
    def row(self):
        return self._row
    @row.setter
    def row(self, row):
        self._row = row
        self.right.lbl_index.setText(str(row))

    @property
    def data(self):
        data = Dict({
            'class_name': self.__class__.__name__,
            'other': {
                key: {
                    k: getattr(self, key).current.get(k, v)
                    for k, v in value.items()
                }
                for key, value in self.DIC_DEFAULT.other.items()
            }
        })
        return data
    @data.setter
    def data(self, data):
        for key, value in data.other.items():
            value_widget = getattr(self.right, key)
            value_widget.current = value

    def __init__(self, editor, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor = editor
        # 腳本清單
        self.header_item = QtWidgets.QTableWidgetItem()
        self.handle_item = QtWidgets.QWidget()
        self.name_item = QtWidgets.QTableWidgetItem(self.TITLE)
        # 腳本清單-操作
        h = QtWidgets.QHBoxLayout(self.handle_item)
        self.pb_remove = QtWidgets.QPushButton('X')
        self.pb_move_up = QtWidgets.QPushButton('↑')
        self.pb_move_down = QtWidgets.QPushButton('↓')
        self.pb_remove.clicked.connect(lambda: self.editor.remove_trigger(self))
        self.pb_move_up.clicked.connect(lambda: self.editor.move_up_trigger(self))
        self.pb_move_down.clicked.connect(lambda: self.editor.move_down_trigger(self))
        h.addWidget(self.pb_remove)
        h.addWidget(self.pb_move_up)
        h.addWidget(self.pb_move_down)

        # 腳本詳細內容
        data = data or self.DIC_DEFAULT
        self.right = self.Trigger(self, data)
        self.data = data

    def activate(self, *args, **kwargs):
        return Dict({
            key: getattr(self, key).get_source(kwargs)
            for key in self.DIC_DEFAULT.other
        })

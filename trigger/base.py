from PyQt5 import QtWidgets
from ui.trigger import Ui_Form
from utils.path import Dict
import components


class BaseTrigger:
    TITLE = ''
    INFORMATION = ''
    DIC_DEFAULT = Dict({
        'rb_source_fixed': True,
        'rb_source_variable': False,
        'le_source_fixed': '',
        'le_source_variable': '',
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
                value_widget = getattr(components, value.class_name).from_value(value)
                self.formLayout_2.setWidget(i, QtWidgets.QFormLayout.LabelRole, name_widget)
                self.formLayout_2.setWidget(i, QtWidgets.QFormLayout.FieldRole, value_widget)
                value_widget.sig_current_changed.connect(self.manager.editor.check_saved)
                setattr(self, key, value_widget)

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
        return Dict({
            'class_name': self.__class__.__name__,
            'rb_source_fixed': self.right.rb_source_fixed.isChecked(),
            'rb_source_variable': self.right.rb_source_variable.isChecked(),
            'le_source_fixed': self.right.le_source_fixed.text(),
            'le_source_variable': self.right.le_source_variable.text(),
            'other': {
                key: {
                    k: v if k != 'default' else getattr(self.right, key).current
                    for k, v in value.items()
                }
                for key, value in self.DIC_DEFAULT.other.items()
            }
        })
    @data.setter
    def data(self, data):
        self.right.rb_source_fixed.setChecked(data.rb_source_fixed)
        self.right.rb_source_variable.setChecked(data.rb_source_variable)
        self.right.le_source_fixed.setText(data.le_source_fixed)
        self.right.le_source_variable.setText(data.le_source_variable)
        for key, value in data.other.items():
            value_widget = getattr(self.right, key)
            value_widget.current = value.default

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
        self.right.le_source_variable.right = self.right
        self.data = data

        # 綁定檢查是否修改功能
        self.right.rb_source_fixed.toggled.connect(self.editor.check_saved)
        self.right.rb_source_variable.toggled.connect(self.editor.check_saved)
        self.right.le_source_fixed.textChanged.connect(self.editor.check_saved)
        self.right.le_source_variable.textChanged.connect(self.editor.check_saved)
        self.right.le_source_fixed.textChanged.connect(
            lambda txt: self.right.rb_source_fixed.setChecked(True))
        self.right.le_source_variable.textChanged.connect(
            lambda txt: self.right.rb_source_variable.setChecked(True))

    def activate(self, *args, **kwargs):
        pass

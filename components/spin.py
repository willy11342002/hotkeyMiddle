from PyQt5 import QtWidgets
from PyQt5 import QtCore


class SpinBox(QtWidgets.QSpinBox):
    sig_current_changed = QtCore.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valueChanged.connect(self.sig_current_changed.emit)
    @classmethod
    def from_value(cls, value):
        obj = cls()
        obj.setValue(value.fixed)
        return obj
    @property
    def current(self):
        return self.value()
    @current.setter
    def current(self, value):
        self.setValue(value)


class DoubleSpinBox(QtWidgets.QDoubleSpinBox):
    sig_current_changed = QtCore.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valueChanged.connect(self.sig_current_changed.emit)
    @classmethod
    def from_value(cls, value):
        obj = cls()
        obj.setValue(value.fixed)
        return obj
    @property
    def current(self):
        return self.value()
    @current.setter
    def current(self, value):
        self.setValue(value)


class PositionBox(QtWidgets.QWidget):
    sig_current_changed = QtCore.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.h = QtWidgets.QHBoxLayout(self)
        self.spb_x = QtWidgets.QSpinBox(self)
        self.spb_y = QtWidgets.QSpinBox(self)
        space = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.h.addWidget(self.spb_x)
        self.h.addWidget(self.spb_y)
        self.h.addItem(space)

        self.spb_x.valueChanged.connect(self.sig_current_changed.emit)
        self.spb_y.valueChanged.connect(self.sig_current_changed.emit)
    @classmethod
    def from_value(cls, value):
        obj = cls()
        obj.spb_x.setValue(value.fixed[0])
        obj.spb_y.setValue(value.fixed[1])
        return obj
    @property
    def current(self):
        return [
            self.spb_x.value(),
            self.spb_y.value(),
        ]
    @current.setter
    def current(self, value):
        self.spb_x.setValue(value[0])
        self.spb_y.setValue(value[1])

from PyQt5 import QtWidgets


class SourceEdit(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dragEnterEvent(self, event):
        if event.source().objectName() == 'lst_trigger':
            event.accept()
        else:
            super().dragEnterEvent(event)

    def focusInEvent(self, event):
        pass
    def keyPressEvent(self, event):
        pass

    def dropEvent(self, event):
        row = event.source().currentRow()
        if row < self.right.row:
            self.setText(str(row))

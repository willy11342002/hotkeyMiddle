from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from utils.path import Dict
import trigger


class TriggerListWidget(QtWidgets.QTableWidget):
    sig_drop_new = QtCore.pyqtSignal(str)
    def dropEvent(self, event):
        if event.source().objectName() == 'tree_scripts':
            class_name = event.source().currentItem().whatsThis(0)
            self.sig_drop_new.emit(class_name)



from ui.editor import Ui_ScriptEditor
class Editor(QtWidgets.QWidget, Ui_ScriptEditor):
    _data = Dict({
        'BASIC': {
            'activate': False,
            'start_hotkey': [121],
            'stop_hotkey': [123],
            'descript': '',
            'category': 'once'
        },
        'SCRIPT': {
            'content': []
        },
    })
    def __init__(self, script, path, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.script = script
        self.path = path
        self.read_data()
        self.lst_trigger.currentItemChanged.connect(
            lambda item: self.lst_page.setCurrentIndex(
                self.lst_trigger.currentRow()
            ))
        self.lst_trigger.sig_drop_new.connect(
            lambda class_name: self.add_trigger(class_name=class_name))

    @property
    def data(self) -> Dict:
        if self.path.is_dir():
            return self._data

        if self.rb_once.isChecked():
            category = 'once'
        if self.rb_while.isChecked():
            category = 'while'

        return Dict({
            'BASIC': {
                'activate': bool(self.ccb_activate.currentIndex()),
                'start_hotkey': self.le_start_hotkey.PRESSED_KEY_VK,
                'stop_hotkey': self.le_stop_hotkey.PRESSED_KEY_VK,
                'descript': self.te_descript.toPlainText(),
                'category': category
            },
            'SCRIPT': {
                'content': [
                    self.lst_page.widget(row).manager.data
                    for row in range(self.lst_trigger.rowCount())
                ]
            },
        })
    @data.setter
    def data(self, data):
        self._data = data
        # 修改UI
        self.ccb_activate.setCurrentIndex(int(data.BASIC.activate))
        self.le_start_hotkey.PRESSED_KEY_VK = data.BASIC.start_hotkey
        self.le_stop_hotkey.PRESSED_KEY_VK = data.BASIC.stop_hotkey
        self.te_descript.setText(data.BASIC.descript)
        if data.BASIC.category == 'once':
            self.rb_once.click()
        else:
            self.rb_while.click()
        for d in data.SCRIPT.content:
            self.add_trigger(class_name=d.class_name, data=d)

    @property
    def path(self) -> Path:
        return self.script.path
    @path.setter
    def path(self, path):
        self.script.path = path

    @property
    def tab_text(self):
        return self.script.tab_text

    # 腳本內容存讀
    def compare_data(self) -> bool:
        return self._data == self.data
    def reset_data(self):
        self.data = self._data
    def init_data(self):
        self.data.dump_json(self.path)
    def read_data(self):
        if self.path.is_dir():
            return
        if not self.path.read_text():
            self.init_data()
            return
        # 讀取資料
        self.data = Dict.load_json(self.path)
    def save_data(self, path=None):
        path = path or self.path
        self.data.dump_json(path)
        self._data = self.data

    def check_saved(self):
        self.script.rename_tab_text(self.script.tab_text)

    # 腳本設計
    def move_up_trigger(self, manager):
        self.lst_page.removeWidget(manager.right)
        self.lst_trigger.removeRow(manager.row)
        self.add_trigger(
            class_name=manager.__class__.__name__,
            row=manager.row-1,
            data=manager.data
        )
    def move_down_trigger(self, manager):
        self.lst_page.removeWidget(manager.right)
        self.lst_trigger.removeRow(manager.row)
        self.add_trigger(
            class_name=manager.__class__.__name__,
            row=manager.row+1,
            data=manager.data
        )
    def remove_trigger(self, manager):
        self.lst_trigger.removeRow(manager.row)
        self.lst_page.removeWidget(manager.right)
        self.reset_index()
        self.check_saved()
    def add_trigger(self, class_name, row=None, data=None):
        Manager = getattr(trigger, class_name, None)
        if not Manager:
            return
        row = row or self.lst_trigger.currentRow()
        row = 0 if row == -1 else row

        # 實體化
        manager = Manager(self, data)
        # 清單內容設定
        self.lst_trigger.insertRow(row)
        self.lst_trigger.setVerticalHeaderItem(row, manager.header_item)
        self.lst_trigger.setCellWidget(row, 0, manager.handle_item)
        self.lst_trigger.setItem(row, 1, manager.name_item)
        # 調整高度
        self.lst_trigger.verticalHeader().resizeSection(row, 50)
        # 右側加入
        self.lst_page.insertWidget(row, manager.right)
        # 重新排序
        self.reset_index()

    # 重新排序腳本清單編號、設定清單按鈕是否啟用
    def reset_index(self):
        for row in range(self.lst_trigger.rowCount()):
            header_item = self.lst_trigger.verticalHeaderItem(row)
            header_item.setText(str(row))

            manager = self.lst_page.widget(row).manager
            manager.row = row
            manager.pb_move_up.setDisabled(False)
            manager.pb_move_down.setDisabled(False)

            if row == 0:
                manager.pb_move_up.setDisabled(True)

            if row+1 == self.lst_trigger.rowCount():
                manager.pb_move_down.setDisabled(True)
        self.check_saved()


class EditorTabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTabBar(QtWidgets.QTabBar())
        self.tabBar().setAutoHide(False)
        self.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, idx):
        editor = self.widget(idx)
        if editor.compare_data():
            self.removeTab(idx)
            return
        result = QtWidgets.QMessageBox.information(
            self, '關閉頁籤', '若未儲存，變更將會遺失，確認關閉頁籤嗎?',
            QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No
        )
        if result == QtWidgets.QMessageBox.No:
            return
        elif result == QtWidgets.QMessageBox.Yes:
            editor.reset_data()
            self.removeTab(idx)

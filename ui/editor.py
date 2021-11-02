# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\editor.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ScriptEditor(object):
    def setupUi(self, ScriptEditor):
        ScriptEditor.setObjectName("ScriptEditor")
        ScriptEditor.resize(758, 651)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        ScriptEditor.setFont(font)
        ScriptEditor.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(ScriptEditor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(ScriptEditor)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rb_once = QtWidgets.QRadioButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.rb_once.setFont(font)
        self.rb_once.setChecked(True)
        self.rb_once.setObjectName("rb_once")
        self.horizontalLayout.addWidget(self.rb_once)
        self.rb_while = QtWidgets.QRadioButton(self.groupBox_2)
        self.rb_while.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.rb_while.setFont(font)
        self.rb_while.setObjectName("rb_while")
        self.horizontalLayout.addWidget(self.rb_while)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.ccb_activate = QtWidgets.QComboBox(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.ccb_activate.setFont(font)
        self.ccb_activate.setStyleSheet("background-color: white;")
        self.ccb_activate.setObjectName("ccb_activate")
        self.ccb_activate.addItem("")
        self.ccb_activate.addItem("")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ccb_activate)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.le_start_hotkey = HotKeyEdit(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.le_start_hotkey.setFont(font)
        self.le_start_hotkey.setStyleSheet("background-color: white;")
        self.le_start_hotkey.setObjectName("le_start_hotkey")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_start_hotkey)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setMinimumSize(QtCore.QSize(100, 0))
        self.label_3.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.le_stop_hotkey = HotKeyEdit(self.tab)
        self.le_stop_hotkey.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.le_stop_hotkey.setFont(font)
        self.le_stop_hotkey.setStyleSheet("background-color: white;")
        self.le_stop_hotkey.setObjectName("le_stop_hotkey")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.le_stop_hotkey)
        self.gridLayout_2.addLayout(self.formLayout_2, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.te_descript = QtWidgets.QTextEdit(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(12)
        self.te_descript.setFont(font)
        self.te_descript.setStyleSheet("background-color: white;")
        self.te_descript.setObjectName("te_descript")
        self.verticalLayout_5.addWidget(self.te_descript)
        self.gridLayout_2.addWidget(self.groupBox, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lst_trigger = TriggerListWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lst_trigger.sizePolicy().hasHeightForWidth())
        self.lst_trigger.setSizePolicy(sizePolicy)
        self.lst_trigger.setMinimumSize(QtCore.QSize(300, 0))
        self.lst_trigger.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lst_trigger.setDragEnabled(True)
        self.lst_trigger.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.lst_trigger.setObjectName("lst_trigger")
        self.lst_trigger.setColumnCount(2)
        self.lst_trigger.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.lst_trigger.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.lst_trigger.setHorizontalHeaderItem(1, item)
        self.lst_trigger.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout_2.addWidget(self.lst_trigger)
        self.lst_page = QtWidgets.QStackedWidget(self.tab_2)
        self.lst_page.setObjectName("lst_page")
        self.horizontalLayout_2.addWidget(self.lst_page)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lst_log = QtWidgets.QListWidget(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lst_log.sizePolicy().hasHeightForWidth())
        self.lst_log.setSizePolicy(sizePolicy)
        self.lst_log.setObjectName("lst_log")
        self.horizontalLayout_3.addWidget(self.lst_log)
        self.te_log = QtWidgets.QTextEdit(self.tab_3)
        self.te_log.setReadOnly(True)
        self.te_log.setObjectName("te_log")
        self.horizontalLayout_3.addWidget(self.te_log)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(ScriptEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ScriptEditor)

    def retranslateUi(self, ScriptEditor):
        _translate = QtCore.QCoreApplication.translate
        ScriptEditor.setWindowTitle(_translate("ScriptEditor", "腳本編輯器"))
        self.groupBox_2.setTitle(_translate("ScriptEditor", "類型"))
        self.rb_once.setText(_translate("ScriptEditor", "運行一次"))
        self.rb_while.setText(_translate("ScriptEditor", "運行直到停止"))
        self.label.setText(_translate("ScriptEditor", "啟用："))
        self.ccb_activate.setItemText(0, _translate("ScriptEditor", "否"))
        self.ccb_activate.setItemText(1, _translate("ScriptEditor", "是"))
        self.label_2.setText(_translate("ScriptEditor", "啟動熱鍵："))
        self.le_start_hotkey.setText(_translate("ScriptEditor", "F10"))
        self.label_3.setText(_translate("ScriptEditor", "停止熱鍵："))
        self.le_stop_hotkey.setText(_translate("ScriptEditor", "F12"))
        self.groupBox.setTitle(_translate("ScriptEditor", "描述"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ScriptEditor", "基本設定"))
        item = self.lst_trigger.horizontalHeaderItem(0)
        item.setText(_translate("ScriptEditor", "操作"))
        item = self.lst_trigger.horizontalHeaderItem(1)
        item.setText(_translate("ScriptEditor", "名稱"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("ScriptEditor", "腳本內容"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("ScriptEditor", "執行紀錄"))
from ui import HotKeyEdit
from window.editor import TriggerListWidget

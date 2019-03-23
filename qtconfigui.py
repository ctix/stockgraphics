# -*- coding: utf-8 -*-
import os, sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QStringListModel

from pw.readconfig import ConfigOfStocks


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = loadUi('./config/configFace.ui', self)
        #  self.setFixedSize(self.sizeHint())

        configfn = "./config/stocks.ini"

        self.qall_list = []
        self.moni_list = []
        self.cfg = ConfigOfStocks(configfn)

        self.set_listview(self.ui.monitoredListView, "monitored")
        self.set_listview(self.ui.favorListView, "all")

        self.ui.favorListView.clicked.connect(self.lv_clicked)

    def set_listview(self, LV, sect_name):
        slm = QStringListModel()
        if sect_name == "all":
            stlist = self.cfg.get_all_items_lst()
            self.qall_list = list(stlist)
        else:
            stlist = self.cfg.get_section_value_list(sect_name)
            self.moni_list = list(stlist)

        slm.setStringList(stlist)
        #  self.ui.monitoredListView.setModel(slm)
        LV.setModel(slm)

    def lv_clicked(self, qModelIndex):
        QMessageBox.information(
            self, 'ListWidget',
            'selected:' + self.qall_list[qModelIndex.row()])


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())

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

        _configfn = "./config/stocks.ini"
        self.file_lines = self.read_config_to_list(_configfn)
        self.qall_list = []
        self.moni_list = []
        self.cfg = ConfigOfStocks(_configfn)

        self.set_listview(self.ui.monitoredListView, "monitored")
        self.set_listview(self.ui.favorListView, "all")

        self.ui.favorListView.clicked.connect(self.lv_clicked)

    def read_config_to_list(self, file_name):
        _file_lines = []
        with open(file_name, "r") as fh:
            #  return fh.readlines()
            for line in fh.readlines():
                line = line[:-1]    # cut the tail "\n"
                _file_lines.append(line)

        return _file_lines

    def set_listview(self, LV, sect_name):
        slm = QStringListModel()
        if sect_name == "all":
            stlist = self.file_lines
            self.qall_list = list(self.file_lines)
        else:
            stlist = self.cfg.get_section_value_list(sect_name)
            self.moni_list = list(stlist)

        print("show the list ==>{}".format(stlist))
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



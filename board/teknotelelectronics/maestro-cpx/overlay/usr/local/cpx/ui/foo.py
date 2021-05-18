#!/usr/bin/python3
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
 
LOCAL_DIR = os.path.dirname(os.path.realpath(__file__))
 
 
class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(LOCAL_DIR + "/foo.ui", self)
        self.ui.listWidget.itemSelectionChanged.connect(self._pageUpdate)
        self.show()
 
    def _pageUpdate(self):
        index = self.ui.listWidget.currentRow()
        self.ui.stackedWidget.setCurrentIndex(index)
 
if __name__== '__main__':
    app = QtWidgets.QApplication([])
    gui = Main()
    sys.exit(app.exec_())

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

from .views.FontListView import FontListView


class AppWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWidget = FontListView(self)
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle("MainWindow")
        self.setMinimumSize(500,500)




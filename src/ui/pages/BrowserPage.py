from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ..components.FontListView import FontListView, FontListItem

from ...logic.font_loader import FontLoader

class BrowserPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QHBoxLayout(self)
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0,0,0,0)
        self.setLayout(self.grid)

        self.font_list = FontListView(self)
        self.font_list.setFixedWidth(200)
        self.grid.addWidget(self.font_list)

        self.preview_area = QWidget(self)
        self.preview_area.setStyleSheet("background-color: black;")
        self.grid.addWidget(self.preview_area)

        self.generateFontList()


    def generateFontList(self):
        font_data: list[FontLoader.FontData] = []
        
        font_data.append(FontLoader.getFontFromPath("src/resources/fonts/Arcane Nine.otf"))
        font_data.append(FontLoader.getFontFromPath("src/resources/fonts/Frostbite.ttf"))

        for data in font_data:
            if not data.valid(): continue
            for family, font in data.families.items():
                item = FontListItem(family, font)
                self.font_list.addItem(item)
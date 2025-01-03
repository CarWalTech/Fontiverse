from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ..components.FontListView import FontListView, FontListItem

from ...logic.font_loader import FontLoader
from ...logic.dafonts_scraper import DaFonts_Scraper

class BrowserPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QGridLayout(self)
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0,0,0,0)
        self.setLayout(self.grid)

        self.font_list = FontListView(self)
        self.font_list.setFixedWidth(200)
        self.grid.addWidget(self.font_list, 0, 0, 2, 1)

        self.preview_area = QWidget(self)
        self.preview_area.setStyleSheet("background-color: black;")
        self.grid.addWidget(self.preview_area, 0, 1, 1, 1)


        self.test_button = QPushButton(self)
        self.test_button.setText("Get DaFonts...")
        self.test_button.clicked.connect(self.getDaFonts)
        self.grid.addWidget(self.test_button, 1, 1, 1, 1)

        self.generateFontList()


    def getDaFonts(self):
        results = DaFonts_Scraper.scrape()
        print(results)
        


    def generateFontList(self):
        font_data: list[FontLoader.FontData] = []
        
        font_data.append(FontLoader.getFontFromPath("src/resources/fonts/Arcane Nine.otf"))
        font_data.append(FontLoader.getFontFromPath("src/resources/fonts/Frostbite.ttf"))

        for data in font_data:
            if not data.valid(): continue
            for family, font in data.families.items():
                item = FontListItem(family, font)
                self.font_list.addItem(item)
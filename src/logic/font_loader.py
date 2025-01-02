"""
Fontiverse: A Font Broswer

Development Status: W.I.P
-------------------------
The following codebase is still being developed and is subject to change at any time without notice


Current Libraries/Modules installed
PyQt6 -> User Interface
csv   -> Reading in Font Data from list


Resources used:
https://www.pythontutorial.net/pyqt/pyqt-qlabel/
https://coderslegacy.com/python/pyqt6-adding-custom-fonts/

Improvements to be made:
Add way to add multiple fonts at, rather than one at at time
Improve Error Handling

Reading CSV Data for Font List:
- Read in CSV
- Filter CSV for Fonts
- Get Font


"""
import sys
import csv
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QFontDatabase

class FontLoader:


    class FontData:
        def __init__(self, id: int):
            self.database_id = id

            if not self.database_id == -1: 
                self.__valid = True
                self.__init_data__()
            else:
                self.__valid = False

        def __init_data__(self):
            self.families: dict[str, QFont] = {}
            # Find the font by the name (font family)
            for family in QFontDatabase.applicationFontFamilies(self.database_id):
                self.families[family] = QFont(family, 16)

        def valid(self):
            return self.__valid
            

    def getFontFromPath(font_path: str) -> FontData:
        """Gets the fonts based on the provided font_path
        Font path must contain the path to the font, the font name and font extension
        example: test_fonts/Arane Nine.otf | test_fonts/ (path), Arcane Nine (name), .otf (extension) 
         """
        # Add font to PyQt6 Font Database and get the corresponding ID
        id = QFontDatabase.addApplicationFont(font_path)
        return FontLoader.FontData(id)



"""
Fontiverse: A Font Broswer

Development Status: W.I.P
-------------------------
The following codebase is still being developed and is subject to change at any time without notice


Current Libraries
PyQt6 -> User Interface


Resources used:
https://www.pythontutorial.net/pyqt/pyqt-qlabel/
https://coderslegacy.com/python/pyqt6-adding-custom-fonts/
"""
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QFontDatabase


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('PyQt Label Widget')
        self.setGeometry(100, 100, 320, 210)

        # create a QLabel widget
        default_label = QLabel('This is a QLabel widget with default font')
        font_changed_label = QLabel('This is a QLabel widget with Arcane Nine.otf Font')

        families = self.get_font("test_fonts/Arcane Nine.otf")

        print(f"Font: {families}")
        # Check if families != "Error" -> if so, then change the font. Otherwise, keep default font
        # Could use try and catch instead of checking for "Error" string but this is easier to track
        if families != "Error":
            font_changed_label.setFont(QFont(families[0], 80))
        else:
            print("Error Occured when loading font. Reverting to default font")

        # place the widget on the window
        layout = QVBoxLayout()
        layout.addWidget(default_label)
        layout.addWidget(font_changed_label)
        self.setLayout(layout)

        # show the window
        self.show()



    def get_font(self,font_path: str):
        """Gets the fonts based on the provided font_path
        Font path must contain the path to the font, the font name and font extension
        example: /test_fonts/Arane Nine.otf | /test_fonts/ (path), Arcane Nine (name), .otf (extension) 
         """
        # Add font to PyQt6 Font Database and get the corresponding ID
        id = QFontDatabase.addApplicationFont(font_path)
        if id < 0: 
            print(f"ID: {id}")
            return "Error"  # font could not be loaded so ID is -1. 

        # Find the font by the name (font family)
        families = QFontDatabase.applicationFontFamilies(id)
        return families

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = MainWindow()

    # start the event loop
    sys.exit(app.exec())

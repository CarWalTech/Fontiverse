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


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default CSV size limit is too small.Increase size to system maxsize
        csv.field_size_limit(sys.maxsize)



        self.setWindowTitle('PyQt Label Widget')
        self.setGeometry(100, 100, 320, 210)

        # create a QLabel widget
        default_label = QLabel('This is a QLabel widget with default font')
        font_changed_otf_label = QLabel('This is a QLabel widget with Arcane Nine.otf Font')
        font_changed_ttf_label = QLabel('This is a QLabel widget with Frostbite.ttf Font')

        otf_families = self.get_font("src/resources/fonts/Arcane Nine.otf")
        ttf_families = self.get_font("src/resources/fonts/Frostbite.ttf")

        # Check if families > -1 -> if so, then change the font. Otherwise, keep default font
        # Could use try and catch instead of checking for "Error" string but this is easier to track
        if otf_families != "Error":
            font_changed_otf_label.setFont(QFont(otf_families[0], 16))
        else:
            print("Error Occured when loading font. Reverting to default font")
        if ttf_families != "Error":
            font_changed_ttf_label.setFont(QFont(ttf_families[0], 16))
        else:
            print("Error Occured when loading font. Reverting to default font")

        # place the widget on the window
        layout = QVBoxLayout()
        layout.addWidget(default_label)
        layout.addWidget(font_changed_otf_label)
        layout.addWidget(font_changed_ttf_label)
        self.setLayout(layout)




        # Reading the CSV and working with the data
        font_result = self.load_font_list_from_csv("src/resources/fonts/font_list.csv")



        font = "rayman"
        result = self.find_font_from_csv_list(font_result, font)
        for i in result: 
            print(i.split(',')[0])

        # for font in sorted(font_result):
        #     print(font)

        # self.find_font_from_list(font_result)
        # self.find_font_in_file("src/resources/fonts/font_list.csv", "") # show the window
        # font_list = self.load_font_list_from_csv("src/resources/fonts/font_list.csv") # show the window


        # for i in 0..len(font_list):
        #     if i == 10:
        #         break
        #     print(font_list[i])

  
        self.show()

    def get_font(self,font_path: str):
        """Gets the fonts based on the provided font_path
        Font path must contain the path to the font, the font name and font extension
        example: test_fonts/Arane Nine.otf | test_fonts/ (path), Arcane Nine (name), .otf (extension) 
         """
        # Add font to PyQt6 Font Database and get the corresponding ID
        id = QFontDatabase.addApplicationFont(font_path)
        if id < 0: 
            return "Error"  # font could not be loaded so ID is -1. 

        # Find the font by the name (font family)
        families = QFontDatabase.applicationFontFamilies(id)
        return families

        
    def load_font_list_from_csv(self, csv_path: str) -> list:
        csv_list = []
        with open(csv_path, newline='') as csv_file:
            font_reader = csv.reader(csv_file, delimiter= ' ', quotechar='|')
            for row in font_reader:
                csv_list.append(', '.join(row))

            return csv_list

    def find_font_from_csv_list(self, font_list:list, font:str) -> str:
        matching_fonts = []
        for i in font_list:
            if font in i:
                matching_fonts.append(i)
        return matching_fonts

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = MainWindow()

    # start the event loop
    sys.exit(app.exec())




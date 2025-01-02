from PyQt6.QtWidgets import QHBoxLayout, QListView, QWidget


class FontListView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = QHBoxLayout(self)
        self.grid.setContentsMargins(0,0,0,0)
        self.setLayout(self.grid)

        self.font_list = QListView(self)
        self.font_list.setFixedWidth(200)
        self.grid.addWidget(self.font_list)

        self.preview_area = QWidget(self)
        self.preview_area.setStyleSheet("background-color: darkgray;")
        self.grid.addWidget(self.preview_area)
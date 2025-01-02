from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *



class FontListItem(QWidget):
    def __init__(self, name: str, font: QFont):
        super().__init__(None)
        
        self.grid = QVBoxLayout(self)
        self.grid.setContentsMargins(0,0,0,0)
        self.setLayout(self.grid)
        
        self.display_label_upper = QLabel(self)
        self.display_label_upper.setMaximumWidth(190)
        self.display_label_upper.setText("ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz")
        self.display_label_upper.setFont(font)
        self.grid.addWidget(self.display_label_upper)

        self.name_label = QLabel(self)
        self.name_label.setText(name)
        self.name_label.setContentsMargins(0,0,0,4)
        self.grid.addWidget(self.name_label)



class FontListView(QListWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

    def addItems(self, items: list[FontListItem]):
        for item in items: self.addItem(item)

    def addItem(self, item: FontListItem):
        list_item = QListWidgetItem(self)
        list_item.setSizeHint(item.sizeHint())
        super().addItem(list_item)
        self.setItemWidget(list_item, item)


import sys
from PyQt6.QtWidgets import QApplication
from src.ui.AppWindow import AppWindow

app = QApplication(sys.argv)
window = AppWindow()
window.show()
app.exec()
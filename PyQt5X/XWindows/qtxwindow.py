"""QtXWindow

Inherits QtXWindow class and
implements set_ui method
using self.gen_{WIDGET_NAME}
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5X.errors import *

class QtXWindow(QMainWindow):
    """Extended QMainWindow

    @parm:
        title: str, title of window
        icon_path: str, path to icon of window
            * filename extension is must be '.ico'
        style_path: str, path to css style file
            * filename extension is must be '.css'
        width: int, width of window
        height: int, height of window
        resizable: bool, fixed size or not, initially resizable (True)
    """
    app = QApplication([])
    def __init__(self, title, icon_path=None, width=None, height=None, resizable=True):
        super().__init__()
        self.setWindowTitle(title)
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
        # size
        monitor = QtXWindow.app.desktop().screenGeometry()
        width, height = (width or 600), (height or 400)
        self.setGeometry(
            (monitor.width()-width)//2, (monitor.height()-height)//2,
            width, height) # center of monitor
        if not resizable:
            self.setFixedSize(width, height)


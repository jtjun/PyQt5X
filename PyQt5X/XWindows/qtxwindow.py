"""QtXWindow

Inherits QtXWindow class and
implements set_ui method
using self.gen_{WIDGET_NAME}
"""
from PyQt5.QtCore import Qt
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
    def __init__(self, title, icon_path=None, width=None, height=None, resizable=True, style_path=None):
        super().__init__()
        self.setWindowTitle(title)
        self.setAutoFillBackground(True)
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
        # style
        if style_path:
            self.set_csstyle(css_file=style_path)

    def set_csstyle(self, css_file=None, style_dict=None):
        """set style with css"""
        if not (css_file or style_dict):
            raise ParmEmptyError('css_file or style_dict is required') 
        if css_file:
            with open(css_file, 'r', encoding='utf-8') as style:
                self.setStyleSheet(style)
        if style_dict:
            # TODO: parse dict and apply style
            pass

    def set_translucent_background(self):
        """Set the background transparent"""
        self.setAttribute(Qt.WA_TranslucentBackground)

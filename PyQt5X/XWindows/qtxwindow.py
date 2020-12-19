"""QtXWindow

Inherits QtXWindow class and
implements set_ui method
using self.gen_{WIDGET_NAME}
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5X.errors import *


class QtXWindow(QMainWindow):
    """Extended QMainWindow

    @cls_attr:
        _name_idx: int, name index
        _font_ids: list[QFontId], list of font id
        app: QApplication, to disaply QtWidget

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
    _name_idx = 0
    _font_ids = list()
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
        # name
        self.setObjectName((title or 'QtXWindow_') + str(QtXWindow._name_idx))

    def show(self):
        """display the window at monitor"""
        super().show()
        QtXWindow.app.exec_()

    def __enter__(self):
        """for 'with' context

        @return:
            window: QtXWindow, itself
        """
        self.show()
        return self

    def __exit__(self, *exc_info):
        """for 'with' context

        @parm:
            exc_info: tuple(type, value, traceback),
                      exception info
        """
        return exc_info

    def set_csstyle(self, css_file=None, style_dict=None):
        """set style with css

        @parm:
            css_file: str, path to css style file
                * filename extension is must be '.css'
            style_dict: dict, css styles
        """
        try: # Prevents program termination due to styling.
            if not (css_file or style_dict):
                raise ParmEmptyError('css_file or style_dict is required')
            if css_file:
                try:
                    with open(css_file, 'r', encoding='utf-8') as style:
                        self.setStyleSheet(style.read())
                except FileNotFoundError:
                    raise ResourceError("No Style File: " + css_file)
            if style_dict:
                # TODO: parse dict and apply style
                pass

        except Error as err:
            print('Can not apply style\n', err)

    def set_translucent_background(self):
        """Set the background transparent"""
        self.setAttribute(Qt.WA_TranslucentBackground)

    def __get_next_name(self, ui_obj):
        """identical name

        @parm:
            ui_obj: QtWidget, ui object
        @return:
            name: str, {obj_cls}_{name_idx}
        """
        QtXWindow._name_idx += 1
        return f'{ui_obj.__class__.__name__}_{QtXWindow._name_idx}'

    def regist_font_family(self, font_path):
        """Regist the font family

        @parm:
            font_path: str, path of font file such as '.ttf'
        """
        QtXWindow._font_ids.append(
            QFontDatabase.addApplicationFont(font_path))

    @staticmethod
    def gen_font(font, size, *, bold):
        """generate font

        @parm:
            font: str, font-family
            size: int, pixel size of font
            bold: bool, bold or not
        @return:
            qfont: QFont
        """
        qfont = QFont()
        if font:
            qfont.setFamily(font)
        qfont.setPixelSize(size or 12)
        qfont.setBold(bold)
        return qfont

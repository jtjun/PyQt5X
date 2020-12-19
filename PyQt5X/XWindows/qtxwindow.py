"""QtXWindow

Inherits QtXWindow class and
implements set_ui method
using self.gen_{WIDGET_NAME}
"""
from traceback import print_exception
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
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
        resizable: bool(True), fixed size or not, initially resizable
    """
    _name_idx = 0
    _font_ids = list()
    app = QApplication([])

    def __init__(self, title, icon_path=None, *, width=None, height=None, resizable=True, style_path=None):
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
        set the ui_objects in the 'with' context,
        when exit the context, show the itself

        @return:
            window: QtXWindow, itself
        """
        return self

    def __exit__(self, *exc_info):
        """for 'with' context
        call the show() to display itself.
        If exception is raised when set the ui (in the 'with' context),
        print traceback at console.

        @parm:
            exc_info: tuple(type, value, traceback),
                      exception info
        """
        self.show()
        if exc_info[0]:
            print_exception(*exc_info)
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
    def gen_font(font_family, size, *, bold):
        """generate font

        @parm:
            font_family: str, font-family
            size: int, pixel size of font
            bold: bool, bold or not
        @return:
            font: QFont
        """
        font = QFont()
        if font_family:
            font.setFamily(font_family)
        font.setPixelSize(size or 12)
        font.setBold(bold)
        return font

    def init_ui_obj(self, ui_obj, name, x, y, width, height, font_family, font_size, bold, font_color, *, func=None, backgrond=None, align=None):
        """initialize ui object

        @parm:
            ui_obj: QtWidget, ui object
            name: str, name of ui object
            x: int, x-position
            y: int, y-positin
            width: int, width
            height: int, height
            font_family: str, font-family of content
            font_size: int, size of point (px)
            bold: bool(False), bold text or not
            font_color: str, #RRGGBB rgb(r, g, b) rgba(r, g, b, opacity)
            func: function, connected function
            backgrond: str, #RRGGBB rgb(r, g, b) rgba(r, g, b, opacity)
            align: str, [center, left, right] text alignment
        @return:
            ui_obj: QtWidget, ui object
        """
        ui_obj.move(x, y)
        ui_obj.setObjectName(name or self.__get_next_name(ui_obj))
        if width and height:
            ui_obj.setFixedSize(width, height)
        ui_obj.setFont(self.gen_font(font_family, font_size, bold=bold))
        if font_color:
            ui_obj.setStyleSheet(f'color: {font_color}')
        if func:
            QtXWindow.connect_func(ui_obj, func)
        if backgrond:
            ui_obj.setStyleSheet(f'background: {backgrond}')
        if align:
            align_flag = {
                'LEFT': Qt.AlignLeft,
                'RIGHT': Qt.AlignRight
            }.get(align.upper(), Qt.AlignCenter)
            ui_obj.setAlignment(align_flag|Qt.AlignVCenter)
        return ui_obj

    @staticmethod
    def connect_func(ui_obj, func):
        """connect ui object and function

        @parm:
            ui_obj: QtWidget, ui object
            func: function, event handler
        @return:
            success: bool, True if connection is successful.
        """
        # TODO: check class of ui_obj and connect func
        try:
            if isinstance(ui_obj, QPushButton):
                ui_obj.clicked.connect(func)
            else:
                raise ParmTypeError('Can not connect function to {ui_obj.__class__.__name__}')
        except:
            return False
        return True


    def gen_label(self, text, name=None, *, align='center', x=0, y=0, width=0, height=0, font_family=None, font_size=0, bold=False, font_color=None, transparent=False):
        """generate label at (x, y) size (width, height) with text

        @parm:
            text: str, label's content
            name: str, name of label
            align: str, [center, left, right] text alignment
            x: int, x-position
            y: int, y-positin
            width: int, width
            height: int, height
            font_family: str, font-family of content
            font_size: int, size of point (px)
            bold: bool(False), bold text or not
            font_color: str, #RRGGBB rgb(r, g, b) rgba(r, g, b, opacity)
            transparent: bool(False), transparent background or not
        """
        background = 'rgba(0,0,0)' if transparent else None
        lbl = QLabel(text, self)
        return self.init_ui_obj(lbl, name, x, y, width, height, font_family, font_size, bold, font_color, backgrond=background, align=align)

    def gen_btn(self, text, name=None, func=None, *, x=0, y=0, width=0, height=0, font_family=None, font_size=0, bold=False, font_color=None, background=None):
        """generate button at (x, y) size (width, height) with text,
        when click the button 'func' is called.

        @parm:
            text: str, label's content
            name: str, name of label
            func: function, button click event handler
            x: int, x-position
            y: int, y-positin
            width: int, width
            height: int, height
            font_family: str, font-family of content
            font_size: int, size of point (px)
            bold: bool(False), bold text or not
            font_color: str, #RRGGBB rgb(r, g, b) rgba(r, g, b, opacity)
            background: str, #RRGGBB rgb(r, g, b) rgba(r, g, b, opacity)
        """
        btn = QPushButton(text, self)
        return self.init_ui_obj(btn, name, x, y, width, height, font_family, font_size, bold, font_color, func=func, backgrond=background)

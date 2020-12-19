"""PyQt5.XWindow.QtXWindow Test"""
from xtest import DATA_PATH
from PyQt5X.XWindows import QtXWindow

def basic_init_test():
    """QtXWindow init tests"""
    # base
    QtXWindow('test').show()
    # width & height
    QtXWindow('test-size', width=300, height=200).show()
    # resizable
    QtXWindow('test-fixed', width=150, height=150, resizable=False).show()
    # css-style
    QtXWindow('test-csstyle', style_path=DATA_PATH + 'basic_init.css').show()
    # with
    with QtXWindow('test-with') as window:
        print(id(window))

def font_test():
    """QtXWindow font tests"""
    window = QtXWindow('test')
    window.regist_font_family(DATA_PATH + 'Noto_Sans\\NotoSans-Regular.ttf')
    font = window.gen_font('NotoSans', 13, bold=True)
    window.show()

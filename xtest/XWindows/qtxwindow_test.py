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
    window = QtXWindow('font-test')
    window.regist_font_family(DATA_PATH + 'Noto_Sans\\NotoSans-Regular.ttf')
    font = window.gen_font('NotoSans', 13, bold=True)
    window.show()

def lbl_test():
    """QtXWindow lbl generator test"""
    window = QtXWindow('lbl-test', width=300, height=200)
    window.gen_label('Test', 'lbl', x=50, y=50, width=200, height=20, font_family='맑은 고딕', font_size=15, font_color='black', align='left')
    window.gen_label('CSS', 'lblcss', x=50, y=100, width=200, height=20, font_size=15)
    window.set_csstyle(DATA_PATH + 'lbl_test.css')
    window.show()

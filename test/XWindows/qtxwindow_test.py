"""PyQt5.XWindow.QtXWindow Test"""
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
    QtXWindow('test-csstyle', style_path='test\\data\\basic_init.css').show()
    # with
    with QtXWindow('test-with') as window:
        print(id(window))

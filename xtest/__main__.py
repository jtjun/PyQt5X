"""Execute PyQt5X tests
"""
import __init__
import PyQt5X
from XWindows.qtxwindow_test import basic_init_test, font_test


if __name__ == '__main__':
    print(PyQt5X.ver)
    #basic_init_test()
    font_test()
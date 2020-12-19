"""Errors used by PyQt5X
"""

class Error(Exception):
    """Base Exception fo all exceptions raised by PyQt5X"""

class ParmError(Error):
    """Parameter Error"""

class ParmEmptyError(ParmError):
    """Parameter did not passed"""

class ParmTypeError(ParmError):
    """Invalid type of parameter has passed"""

class ResourceError(Error):
    """Error about Resources such as FileNotFoundError"""

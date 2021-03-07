# external
from PyQt5.QtCore import QObject, pyqtSignal


class InternetSignals(QObject):
    """Internet Signals"""
    connected = pyqtSignal()


class MBSignals(QObject):
    """MB Signals"""
    error = pyqtSignal([object], [object, bool])


class UISignals(QObject):
    """UI Signals"""
    action = pyqtSignal()
    get_settings = pyqtSignal()
    set_settings = pyqtSignal()

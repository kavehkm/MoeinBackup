# standard
import socket
# internal
from src.signals import InternetSignals
# external
from PyQt5.QtCore import QTimer


class Internet(object):
    """Internet"""
    def __init__(self, address, port, timeout, interval):
        self._address = address
        self._port = port
        self._timeout = timeout
        self._interval = interval
        self._timer = QTimer()
        self.signals = InternetSignals()
        self._bootstrap()

    def _bootstrap(self):
        self._connect_signals()

    def _connect_signals(self):
        self._timer.timeout.connect(self._check)

    def _check(self):
        try:
            s = socket.create_connection((self._address, self._port), self._timeout)
            s.close()
        except OSError:
            pass
        else:
            self._timer.stop()
            self.signals.connected.emit()

    def connecting(self):
        self._timer.start(self._interval)

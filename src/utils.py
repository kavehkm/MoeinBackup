# standard
import os
import socket
import configparser
# internal
from src import settings
from src.signals import InternetSignals
# external
from PyQt5.QtCore import QTimer


class Singleton(type):
    """Singleton MetaClass"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SettingsAPI(metaclass=Singleton):
    """Settings API"""
    def __init__(self):
        self._filepath = settings.SETTINGS_API_FILEPATH
        self._parser = configparser.ConfigParser()
        # initialize parser
        if os.access(self._filepath, 6):
            self._parser.read(self._filepath)
        else:
            self._parser.read_dict(settings.SETTINGS_API_DEFAULT)

    def get(self, section, default=None):
        if default is None:
            default = {}
        try:
            return dict(self._parser[section])
        except KeyError:
            return default

    def set(self, section, value):
        self._parser[section] = value

    def get_bulk(self, sections):
        return {
            section: self.get(section)
            for section in sections
        }

    def set_bulk(self, sections_values):
        for section, value in sections_values.items():
            self.set(section, value)

    def save(self):
        with open(self._filepath, 'w') as f:
            self._parser.write(f)


class Internet(object):
    """Internet"""
    def __init__(self):
        self._address = settings.INTERNET_ADDRESS
        self._port = settings.INTERNET_PORT
        self._timeout = settings.INTERNET_TIMEOUT
        self._interval = settings.INTERNET_INTERVAL
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
        self._timer.start(self._interval * 1000)

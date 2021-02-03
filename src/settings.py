# standard
import os
import configparser


# heartbeat
HEARTBEAT = 10


# internet settings
INTERNET = {
    'address': '1.1.1.1',
    'port': 53,
    'timeout': 3,
    'interval': 5
}


# modules
MODULES = ('fb', 'synker')


# modules dir
MODULES_DIR = 'src.modules'


# modules class naming convention
CONVENTION = 'title'


# modules default settings
MODULES_SETTINGS = {
    'fb': {
        'interval': 0,
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 's3cret',
        'dbname': 'dbname',
        'temp': '/tmp'
    },
    'synker': {
        'interval': 0,
        'localdir': '',
        'pattern': '.*',
        'limit': 0,
        'clouddir': '/backup',
        'mtimefile': '/mtime.txt',
        'token': ''
    }
}


# settings file name
SETTINGS_FILE_NAME = 'settings.ini'


# settings file path
SETTINGS_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), SETTINGS_FILE_NAME)


# settings api
class SettingsAPI(object):
    """Settings API"""
    def __init__(self):
        self._parser = None

    @property
    def parser(self):
        if self._parser is None:
            self._parser = configparser.ConfigParser()
            if os.access(SETTINGS_FILE_PATH, 6):
                self._parser.read(SETTINGS_FILE_PATH)
            else:
                self._parser.read_dict(MODULES_SETTINGS)
        return self._parser

    def get(self, section, default=None):
        if default is None:
            default = {}
        try:
            return dict(self.parser[section])
        except KeyError:
            return default

    def set(self, section, value):
        self.parser[section] = value

    def get_bulk(self, sections):
        return {
            section: self.get(section)
            for section in sections
        }

    def set_bulk(self, sections_values):
        for section, value in sections_values.items():
            self.set(section, value)

    def save(self):
        with open(SETTINGS_FILE_PATH, 'w') as f:
            self.parser.write(f)

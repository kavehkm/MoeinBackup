# standard
import os
import configparser
# internal
from src import settings
from src.helper import Singleton


class Config(metaclass=Singleton):
    """Config"""
    def __init__(self, filepath, default_configs):
        self._filepath = filepath
        self._parser = configparser.ConfigParser()
        if os.access(self._filepath, 6):
            self._parser.read(self._filepath)
        else:
            self._parser.read_dict(default_configs)

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


# interface
_config = Config(settings.CONFIG_FILEPATH, settings.CONFIG_DEFAULT)


get = _config.get


set = _config.set


get_bulk = _config.get_bulk


set_bulk = _config.set_bulk


save = _config.save

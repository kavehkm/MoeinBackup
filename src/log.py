# standard
import logging
# internal
from src import settings
from src.helper import Singleton


class Log(metaclass=Singleton):
    """Log"""
    def __init__(self, level, filepath, frmt):
        self._level = level
        self._filepath = filepath
        self._frmt = frmt
        self._handler = None
        self._loggers = {}

    @property
    def handler(self):
        if self._handler is None:
            formatter = logging.Formatter(self._frmt)
            self._handler = logging.FileHandler(self._filepath, 'w', 'utf-8')
            self._handler.setFormatter(formatter)
        return self._handler

    def get_logger(self, name='root'):
        if name not in self._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(getattr(logging, self._level.upper()))
            logger.addHandler(self.handler)
            self._loggers[name] = logger
        return self._loggers[name]


# interface
_log = Log(settings.LOG_LEVEL, settings.LOG_FILEPATH, settings.LOG_FORMAT)


get_logger = _log.get_logger


_logger = _log.get_logger()


debug = _logger.debug


info = _logger.info


warning = _logger.warning


error = _logger.error


critical = _logger.critical

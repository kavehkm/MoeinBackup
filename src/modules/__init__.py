# standard
from time import time
# internal
from src import errors


class BaseModule(object):
    """Base Module"""
    __module_name__ = 'base_module'

    def __init__(self, interval=0):
        self._ran = 0
        # validation
        error = ''
        try:
            interval = int(interval)
        except Exception:
            error = 'invalid interval'
        else:
            if interval < 0:
                error = 'interval cannot be negative integer'
        if error:
            raise errors.ModuleError(self.name, error)
        self._interval = interval

    @property
    def name(self):
        return self.__module_name__

    def _do(self):
        print(self.name, ': ', self._ran)

    def run(self):
        if time() - self._ran > self._interval:
            self._do()
            self._ran = time()

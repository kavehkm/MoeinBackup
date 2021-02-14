# standard
from time import time
# internal
from src import errors


class BaseModule(object):
    """Base Module"""
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
                error = 'interval cannot be negative'
        if error:
            raise errors.ModuleError(error)
        self._interval = interval

    def _do(self):
        print(self.__class__.__name__, ': ', self._ran)

    def run(self):
        if time() - self._ran > self._interval:
            self._do()
            self._ran = time()

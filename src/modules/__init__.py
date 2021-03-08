# standard
from time import time
# internal
from src.translation import _
from src.errors import ModuleError


class BaseModule(object):
    """Base Module"""
    def __init__(self, interval=0):
        self._ran = 0
        # validation
        error = ''
        try:
            interval = int(interval)
        except Exception:
            error = _('invalid interval')
        else:
            if interval < 0:
                error = _('interval cannot be negative')
        if error:
            raise ModuleError(error)
        self._interval = interval

    def _do(self):
        print(self.__class__.__name__, ': ', self._ran)

    def run(self):
        if time() - self._ran > self._interval:
            self._do()
            self._ran = time()

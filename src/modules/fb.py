# standard
import os
# internal
from src.modules import BaseModule
from src.errors import ModuleError


class Fb(BaseModule):
    """Fb"""
    def __init__(self, interval, instance, user, password, temp, dest):
        super().__init__(interval)
        # validation
        error = ''
        if not instance:
            error = 'instance is required'
        elif not user:
            error = 'user is required'
        elif not password:
            error = 'password is required'
        elif not temp or not os.access(temp, 7):
            error = 'invalid temp'
        elif not dest or not os.access(dest, 7):
            error = 'invalid destination'
        else:
            # check instance, username and password against dbms
            pass
        if error:
            raise ModuleError(error)
        self._instance = instance
        self._user = user
        self._password = password
        self._temp = temp
        self._dest = dest

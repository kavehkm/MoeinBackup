# internal
from src.translation import _


class BaseError(Exception):
    """Base Error"""
    msg = _('base error')

    def __init__(self, msg='', details=''):
        if msg:
            self.msg = msg
        self.details = details

    def __str__(self):
        return self.msg


class NetworkError(BaseError):
    """Network Error"""
    msg = _('network error')


class ModuleError(BaseError):
    """Module Error"""
    msg = _('module error')

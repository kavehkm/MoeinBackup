class BaseError(Exception):
    """Base Error"""
    def __init__(self, error='', details=''):
        self.error = error
        self.details = details

    def __str__(self):
        return self.error


class NetworkError(BaseError):
    """Network Error"""
    pass


class ModuleError(BaseError):
    """Module Error"""
    def __init__(self, module, error='', details=''):
        self.module = module
        super().__init__(error, details)

    def __str__(self):
        return '{}: {}'.format(self.module, self.error)

# internal
from src.errors import ModuleError


class ProviderError(ModuleError):
    """Provider Error"""
    msg = 'cloud provider base error'


class ProviderBadInputError(ProviderError):
    """Provider Bad Input Error"""
    msg = 'cloud provider bad input parameter'


class ProviderAuthError(ProviderError):
    """Provider Auth Error"""
    msg = 'cloud provider invalid authentication credentials'


class ProviderAccessError(ProviderError):
    """Provider Access Error"""
    msg = 'cloud provider access dined'


class ProviderAPIError(ProviderError):
    """Provider API Error"""
    msg = 'cloud provider api error'


class ProviderLimitReachError(ProviderError):
    """Provider Limit Reach Error"""
    msg = 'cloud provider limit reach'


class ProviderInternalError(ProviderError):
    """Provider Internal Error"""
    msg = 'cloud provider internal error'

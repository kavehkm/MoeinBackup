# internal
from src.translation import _
from src.errors import ModuleError


class ProviderError(ModuleError):
    """Provider Error"""
    msg = _('cloud provider base error')


class ProviderBadInputError(ProviderError):
    """Provider Bad Input Error"""
    msg = _('cloud provider bad input parameter')


class ProviderAuthError(ProviderError):
    """Provider Auth Error"""
    msg = _('cloud provider invalid authentication credentials')


class ProviderAccessError(ProviderError):
    """Provider Access Error"""
    msg = _('cloud provider access dined')


class ProviderAPIError(ProviderError):
    """Provider API Error"""
    msg = _('cloud provider api error')


class ProviderLimitReachError(ProviderError):
    """Provider Limit Reach Error"""
    msg = _('cloud provider limit reach')


class ProviderInternalError(ProviderError):
    """Provider Internal Error"""
    msg = _('cloud provider internal error')

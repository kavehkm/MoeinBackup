# standard
import gettext
# internal
from src import settings


lang = gettext.translation(settings.TRANSLATION_DOMAIN,
                           localedir=settings.LOCALE_DIRPATH,
                           languages=[settings.LANG_CODE])
lang.install()


_ = lang.gettext

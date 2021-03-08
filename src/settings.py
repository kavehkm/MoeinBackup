# standard
import os


# BASE DIRECTORY
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# HEARTBEAT
HEARTBEAT = 10 * 1000


# INTERNET
INTERNET = {
    'address': '1.1.1.1',
    'port': 53,
    'timeout': 3,
    'interval': 5 * 1000
}


# MODULES
MODULES = ('fb', 'synker')
MODULES_DIR = 'src.modules'
MODULES_CONVENTION = 'title'
MODULES_SETTINGS = {
    'fb': {
        'interval': 60,
        'instance': 'localhost',
        'user': 'root',
        'password': 's3cret',
        'temp': '/tmp',
        'dest': ''
    },
    'synker': {
        'interval': 30,
        'localdir': '',
        'pattern': '*',
        'clouddir': '/backup',
        'limit': 0,
        'token': ''
    }
}


# CONFIG
CONFIG_FILENAME = 'settings.ini'
CONFIG_FILEPATH = os.path.join(BASE_DIR, CONFIG_FILENAME)
CONFIG_DEFAULT = {**MODULES_SETTINGS}


# LOG
LOG_LEVEL = 'DEBUG'
LOG_FILENAME = 'log/logs.log'
LOG_FILEPATH = os.path.join(BASE_DIR, LOG_FILENAME)
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


# TRANSLATION
LANGUAGES = (
    ('en', 'English'),
    ('fa', 'Persian')
)
LANG_CODE = 'fa'
TRANSLATION_DOMAIN = 'mb'
LOCALE_DIRNAME = 'locale'
LOCALE_DIRPATH = os.path.join(BASE_DIR, LOCALE_DIRNAME)

# standard
import os


# BASE DIRECTORY
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# HEART BEAT
HEARTBEAT = 10 * 1000


# INTERNET SETTINGS
INTERNET_ADDRESS = '1.1.1.1'
INTERNET_PORT = 53
INTERNET_TIMEOUT = 3
INTERNET_INTERVAL = 5


# MODULES SETTINGS
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


# SETTINGS API
SETTINGS_API_FILENAME = 'settings.ini'
SETTINGS_API_FILEPATH = os.path.join(BASE_DIR, SETTINGS_API_FILENAME)
SETTINGS_API_DEFAULT = {**MODULES_SETTINGS}

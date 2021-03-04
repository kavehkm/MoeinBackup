# standard
import json
import requests
from datetime import datetime
# internal
from src.errors import NetworkError
from src.modules.synker.providers.errors import *


class DropboxProvider(object):
    """Dropbox Provider"""
    _datetime_format = '%Y-%m-%dT%H:%M:%SZ'
    _urls = {
        'account_info': 'https://api.dropboxapi.com/2/users/get_current_account',
        'get_files':    'https://api.dropboxapi.com/2/files/list_folder',
        'upload':       'https://content.dropboxapi.com/2/files/upload',
        'download':     'https://content.dropboxapi.com/2/files/download',
        'delete':       'https://api.dropboxapi.com/2/files/delete'
    }

    def __init__(self, token):
        self._token = token
        self._check_token()

    def _check_token(self):
        self._send_request(self._urls['account_info'])

    def _mtime2iso(self, mtime):
        return datetime.fromtimestamp(mtime).strftime(self._datetime_format)

    def _iso2mtime(self, iso):
        return datetime.strptime(iso, self._datetime_format).timestamp()

    def _send_request(self, url, **p):
        headers = p.get('headers', {})
        headers['Authorization'] = 'Bearer {}'.format(self._token)
        p['headers'] = headers
        try:
            r = requests.post(url, **p)
        except requests.exceptions.RequestException:
            raise NetworkError
        else:
            if r.status_code == 200:
                return r
            elif r.status_code == 400:
                raise ProviderBadInputError(details=r.text)
            elif r.status_code == 401:
                raise ProviderAuthError(details=r.json()['error_summary'])
            elif r.status_code == 403:
                raise ProviderAccessError
            elif r.status_code == 409:
                raise ProviderAPIError(details=r.json()['error_summary'])
            elif r.status_code == 429:
                raise ProviderLimitReachError
            else:
                raise ProviderInternalError

    def get_files(self, path, recursive=True):
        p = {
            'headers': {
                'Content-Type': 'application/json'
            },
            'json': {
                'path': path,
                'recursive': recursive
            }
        }
        r = self._send_request(self._urls['get_files'], **p).json()
        return [
            [entry['path_display'], entry['size'], self._iso2mtime(entry['client_modified'])]
            for entry in r['entries'] if entry['.tag'] == 'file'
        ]

    def upload(self, content, path, mtime):
        p = {
            'headers': {
                'Dropbox-API-Arg': json.dumps({
                    'path': path,
                    'mode': 'overwrite',
                    'client_modified': self._mtime2iso(mtime)
                }),
                'Content-Type': 'application/octet-stream'
            },
            'data': content
        }
        self._send_request(self._urls['upload'], **p)

    def delete(self, path):
        p = {
            'headers': {
                'Content-Type': 'application/json'
            },
            'json': {
                'path': path
            }
        }
        self._send_request(self._urls['delete'], **p)

# standard
import os
import bisect
import pathlib
# internal
from src.translation import _
from src.errors import ModuleError
from src.modules import BaseModule
from src.modules.synker.providers import DropboxProvider
from src.modules.synker.providers.errors import ProviderAPIError


class File(object):
    """File"""
    def __init__(self, path, size, mtime):
        self._path = path
        self._size = size
        self._mtime = mtime

    @property
    def path(self):
        return self._path

    @property
    def size(self):
        return self._size

    @property
    def mtime(self):
        return self._mtime

    def __eq__(self, other):
        return self.mtime == other.mtime

    def __ne__(self, other):
        return self.mtime != other.mtime

    def __gt__(self, other):
        return self.mtime > other.mtime

    def __ge__(self, other):
        return self.mtime >= other.mtime

    def __lt__(self, other):
        return self.mtime < other.mtime

    def __le__(self, other):
        return self.mtime <= other.mtime


class FileQueue(object):
    """File Queue"""
    def __init__(self):
        self._files = []
        self._used_space = 0

    @property
    def used_space(self):
        return self._used_space

    def push(self, file):
        bisect.insort(self._files, file)
        self._used_space += file.size

    def pop(self):
        file = self._files.pop(0)
        self._used_space -= file.size
        return file

    def head(self):
        return self._files[-1]

    def tail(self):
        return self._files[0]


class Synker(BaseModule):
    """Synker"""
    def __init__(self, interval, localdir, pattern, clouddir, limit, token):
        super().__init__(interval)
        # validation
        error = ''
        if not localdir or not os.access(localdir, 7):
            error = _('invalid localdir')
        elif not pattern:
            error = _('pattern is required')
        elif not clouddir or not clouddir.startswith('/'):
            error = _('invalid clouddir')
        elif not token:
            error = _('token is required')
        else:
            try:
                limit = int(limit)
            except Exception:
                error = _('invalid limit')
        if error:
            raise ModuleError(error)
        self._localdir = localdir
        self._pattern = pattern
        self._clouddir = clouddir
        self._limit = limit
        self._provider = DropboxProvider(token)
        self._cloud = None

    @property
    def cloud(self):
        if self._cloud is None:
            fq = FileQueue()
            try:
                for f in self._provider.get_files(self._clouddir):
                    fq.push(File(*f))
            except ProviderAPIError:
                pass
            self._cloud = fq
        return self._cloud

    @property
    def max_mtime(self):
        try:
            head = self.cloud.head()
        except IndexError:
            mtime = 0
        else:
            mtime = head.mtime
        return mtime

    @property
    def remain_space(self):
        return self._limit - self.cloud.used_space

    @property
    def new_files(self):
        mtime = self.max_mtime
        return sorted([
            entry for entry in pathlib.Path(self._localdir).rglob(self._pattern)
            if entry.is_file() and entry.stat().st_mtime > mtime and entry.stat().st_size < self._limit
        ], key=lambda f: f.stat().st_mtime)

    def _do(self):
        for nf in self.new_files:
            while nf.stat().st_size > self.remain_space:
                tail = self.cloud.tail()
                try:
                    self._provider.delete(tail.path)
                except ProviderAPIError:
                    pass
                self.cloud.pop()
            content = nf.read_bytes()
            size = nf.stat().st_size
            mtime = nf.stat().st_mtime
            relpath = nf.relative_to(self._localdir).as_posix()
            path = self._clouddir + '/' + relpath
            self._provider.upload(content, path, mtime)
            self.cloud.push(File(path, size, mtime))

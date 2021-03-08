# standard
import os
import zipfile
from datetime import datetime
# internal
from src.translation import _
from src.modules import BaseModule
from src.errors import ModuleError
# external
import pyodbc


class Fb(BaseModule):
    """Fb"""
    def __init__(self, interval, instance, user, password, temp, dest):
        super().__init__(interval)
        # validation
        error, details = '', ''
        if not instance:
            error = _('instance is required')
        elif not user:
            error = _('user is required')
        elif not password:
            error = _('password is required')
        elif not temp or not os.access(temp, 7):
            error = _('invalid temp')
        elif not dest or not os.access(dest, 7):
            error = _('invalid destination')
        else:
            try:
                connection = self._get_connection(instance, user, password)
                with connection.cursor() as c:
                    c.execute("SELECT @@VERSION")
            except pyodbc.Error as e:
                error = _('cannot connect to database')
                details = str(e)
        if error:
            raise ModuleError(error, details)
        self._instance = instance
        self._user = user
        self._password = password
        self._temp = temp
        self._dest = dest

    @staticmethod
    def _get_connection(instance, user, password, autocommit=True):
        driver = [d for d in pyodbc.drivers() if d.find('SQL') != -1][0]
        dsn = 'driver={};server={};uid={};pwd={}'.format(driver, instance, user, password)
        return pyodbc.connect(dsn, autocommit=autocommit)

    @property
    def connection(self):
        return self._get_connection(self._instance, self._user, self._password)

    @property
    def filename(self):
        return datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ_Moein')

    @property
    def databases(self):
        sql = "SELECT name FROM master.dbo.sysdatabases WHERE name NOT IN ('master', 'model', 'msdb', 'tempdb')"
        with self.connection.cursor() as c:
            r = c.execute(sql).fetchall()
        return [db[0] for db in r]

    def _take(self, databases):
        sql = "BACKUP DATABASE ? TO DISK=?"
        with self.connection.cursor() as c:
            for database in databases:
                dest = self._temp + '/' + database + '.BAK'
                c.execute(sql, [database, dest])
                while c.nextset():
                    pass

    def _move(self):
        backups = [b for b in os.listdir(self._temp) if b.endswith('.BAK')]
        with zipfile.ZipFile(self._dest + '/' + self.filename, 'w', zipfile.ZIP_BZIP2) as zf:
            for backup in backups:
                p = self._temp + '/' + backup
                zf.write(p, backup)
                os.remove(p)

    def _do(self):
        try:
            self._take(self.databases)
        except pyodbc.Error as e:
            raise ModuleError(_('cannot take backup'), str(e))
        else:
            self._move()

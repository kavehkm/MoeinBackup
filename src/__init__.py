# standard
import importlib
import threading
# internal
from src import errors, settings
from src.signals import MBSignals
from src.utils import Internet
# external
from PyQt5.QtCore import QTimer


class MB(object):
    """Moein Backup"""
    def __init__(self, ui):
        self._ui = ui
        self._lock = False
        self._running = False
        self._initialized = False
        self._modules = []

        self._timer = QTimer()
        self._signals = MBSignals()
        self._sa = settings.SettingsAPI()
        self._internet = Internet(**settings.INTERNET)
        self._bootstrap()

    def _bootstrap(self):
        self._connect_signals()

    def _connect_signals(self):
        # timer
        self._timer.timeout.connect(self._run)
        # internet
        self._internet.signals.connected.connect(self.start)
        # MB
        self._signals.error.connect(self._error_handle)

    def _init_modules(self, s):
        for m in settings.MODULES:
            module = importlib.import_module(settings.MODULES_DIR + '.' + m)
            cls = getattr(m, settings.CONVENTION)()
            self._modules.append(getattr(module, cls)(**s[m]))
        self._initialized = True

    def _run_modules(self):
        self._lock = True
        try:
            for module in self._modules:
                module.run()
        except Exception as e:
            self._signals.error.emit(e)
        finally:
            self._lock = False

    def _run(self):
        if not self._lock:
            threading.Thread(target=self._run_modules).start()

    def get_settings(self):
        s = self._sa.get_bulk(settings.MODULES)
        self._ui.set_settings(s)

    def set_settings(self):
        s = self._ui.get_settings()
        try:
            self._init_modules(s)
            self._sa.set_bulk(s)
            self._sa.save()
        except Exception as e:
            self._signals.error.emit(e)
        else:
            self._ui.show_message('settings updated', 1)

    def start(self):
        if not self._initialized:
            s = self._sa.get_bulk(settings.MODULES)
            try:
                self._init_modules(s)
            except Exception as e:
                self._signals.error.emit(e)
        if self._initialized:
            self._ui.running()
            self._running = True
            self._timer.start(settings.HEARTBEAT * 1000)

    def stop(self):
        self._timer.stop()
        self._running = False
        self._ui.stopped()

    def action(self):
        if self._running:
            self.stop()
        else:
            self.start()

    def _error_handle(self, e):
        self.stop()
        if isinstance(e, errors.NetworkError):
            self._ui.connecting()
            self._internet.connecting()
        elif isinstance(e, errors.ModuleError):
            self._ui.show_message('{} ---> {}'.format(e.msg, e.details), 0)
        else:
            self._ui.show_message(str(e), 0)

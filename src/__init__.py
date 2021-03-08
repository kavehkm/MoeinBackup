# standard
import importlib
import threading
# internal
from src.translation import _
from src.utils import Internet
from src.signals import MBSignals
from src import errors, settings, config, log
# external
from PyQt5.QtCore import QTimer


class MB(object):
    """Moein Backup"""
    def __init__(self, ui):
        log.debug('initializing MB')
        log.debug('about to set: ui, lock, running, initialized and modules')
        self._ui = ui
        self._lock = False
        self._running = False
        self._initialized = False
        self._modules = []
        log.debug('about to attach: timer, signals and internet')
        self._timer = QTimer()
        self._signals = MBSignals()
        self._internet = Internet(**settings.INTERNET)
        self._bootstrap()
        log.debug('MB initialized')

    def _bootstrap(self):
        log.debug('bootstraping MB')
        self._connect_signals()
        log.debug('MB bootstrapped')

    def _connect_signals(self):
        log.debug('MB connecting signals')
        # timer
        self._timer.timeout.connect(self._run)
        log.debug('timer-signal connected')
        # internet
        self._internet.signals.connected.connect(self.start)
        log.debug('internet-signal connected')
        # MB
        self._signals.error[object].connect(self._error_handle)
        self._signals.error[object, bool].connect(self._error_handle)
        log.debug('error-handle-signal connected')
        # UI
        self._ui.signals.action.connect(self.action)
        self._ui.signals.get_settings.connect(self.get_settings)
        self._ui.signals.set_settings.connect(self.set_settings)
        log.debug('ui-signals connected')
        log.debug('MB signals connected')

    def _init_modules(self, s):
        modules = []
        for module_name in settings.MODULES:
            module = importlib.import_module(settings.MODULES_DIR + '.' + module_name)
            cls = getattr(module_name, settings.MODULES_CONVENTION)()
            modules.append(getattr(module, cls)(**s[module_name]))
        self._modules = modules
        self._initialized = True

    def _run_modules(self):
        self._lock = True
        try:
            for module in self._modules:
                module.run()
        except Exception as e:
            self._signals.error[object].emit(e)
        finally:
            self._lock = False

    def _run(self):
        if not self._lock:
            threading.Thread(target=self._run_modules).start()

    def get_settings(self):
        s = config.get_bulk(settings.MODULES)
        self._ui.set_settings(s)

    def set_settings(self):
        s = self._ui.get_settings()
        try:
            self._init_modules(s)
            config.set_bulk(s)
            config.save()
        except Exception as e:
            self._signals.error[object, bool].emit(e, False)
        else:
            self._ui.show_message(_('settings updated'), 1)

    def start(self):
        log.info('MB start')
        log.debug('about to check modules status')
        if not self._initialized:
            log.debug('modules not initialized')
            log.debug('get modules settings')
            s = config.get_bulk(settings.MODULES)
            try:
                log.debug('try to initialize modules')
                self._init_modules(s)
                log.debug('modules initialized successfully')
            except Exception as e:
                self._signals.error[object].emit(e)
        if self._initialized:
            log.debug('modules already initialized')
            log.debug('about to put ui on running state')
            self._ui.running()
            log.debug('about to turn MB running state to true')
            self._running = True
            log.debug('about to start MB timer with heartbeat: %s', settings.HEARTBEAT)
            self._timer.start(settings.HEARTBEAT)

    def stop(self):
        log.info('MB stopped')
        log.debug('about to stop MB timer')
        self._timer.stop()
        log.debug('about to turn MB running state to false')
        self._running = False
        log.debug('about to put ui on stopped state')
        self._ui.stopped()

    def action(self):
        if self._running:
            self.stop()
        else:
            self.start()

    def _error_handle(self, e, continues=True):
        msg = str(e)
        details = e.details if hasattr(e, 'details') else ''
        log.error('%s:%s', msg, details)
        self.stop()
        log.debug('about to dispatch and handle error')
        if isinstance(e, errors.NetworkError) and continues:
            log.debug('about to put ui on connecting state')
            self._ui.connecting()
            log.info('try connecting')
            self._internet.connecting()
        else:
            log.debug('about to show error message on ui')
            self._ui.show_message(msg, 0)

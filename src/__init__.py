# standard
import importlib
import threading
# internal
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
        self._signals.error.connect(self._error_handle)
        log.debug('error-handle-signal connected')
        log.debug('MB signals connected')

    def _init_modules(self, s):
        for m in settings.MODULES:
            module = importlib.import_module(settings.MODULES_DIR + '.' + m)
            cls = getattr(m, settings.MODULES_CONVENTION)()
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
        s = config.get_bulk(settings.MODULES)
        self._ui.set_settings(s)

    def set_settings(self):
        s = self._ui.get_settings()
        try:
            self._init_modules(s)
            config.set_bulk(s)
            config.save()
        except Exception as e:
            self._signals.error.emit(e)
        else:
            self._ui.show_message('settings updated', 1)

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
                self._signals.error.emit(e)
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

    def _error_handle(self, e):
        # create log message
        if isinstance(e, errors.BaseError):
            msg = e.msg
            if e.details:
                msg += ': {}'.format(e.details)
        else:
            msg = str(e)
        log.error(msg)
        self.stop()
        log.debug('about to dispatch and handle error')
        if isinstance(e, errors.NetworkError):
            log.debug('about to put ui on connecting state')
            self._ui.connecting()
            log.info('try connecting')
            self._internet.connecting()
        else:
            log.debug('about to show error message')
            self._ui.show_message(str(e), 0)

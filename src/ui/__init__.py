# internal
from src.signals import UISignals


class BaseUI(object):
    """Base UI"""
    def __init__(self):
        self.signals = UISignals()
        self._bootstrap()

    def _bootstrap(self):
        self._create_ui()
        self._connect_signals()

    def _create_ui(self):
        pass

    def _connect_signals(self):
        pass

    def get_settings(self):
        pass

    def set_settings(self):
        pass

    def show_message(self, msg, code):
        bg_color = 'white'
        if code == 0:
            # error
            bg_color = 'red'
        elif code == 1:
            # success
            bg_color = 'green'
        print(bg_color, ': ', msg)

    def running(self):
        print('running...')

    def stopped(self):
        print('stopped...')

    def connecting(self):
        print('connecting...')


class UI(BaseUI):
    """UI"""
    pass

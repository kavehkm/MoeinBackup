# standard
import sys
# internal
from src import MB
from src.ui import UI
# external
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    ui = UI()
    mb = MB(ui)
    mb.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

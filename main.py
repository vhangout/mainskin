import sys
from main_window import MainWindow
from PyQt5.QtWidgets import QApplication

import re

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()

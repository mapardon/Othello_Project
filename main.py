import sys
from gui.WindowUI import WindowUI
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    ui = WindowUI()
    ui.show()
    sys.exit(app.exec_())

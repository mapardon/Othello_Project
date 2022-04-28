import sys
from gui.ManagerUI import ManagerUI
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    ui = ManagerUI()
    ui.show()
    sys.exit(app.exec_())

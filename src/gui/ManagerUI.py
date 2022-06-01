from PyQt5.QtWidgets import *
from src.gui.MenuTab import MenuTab
from src.gui.GameTab import GameTab


class ManagerUI(QMainWindow):
    """ Run some initializations for UI """

    def __init__(self):
        # window pars
        super(ManagerUI, self).__init__()
        self.setMinimumSize(900, 700)
        self.setWindowTitle("Othello")

        self.move(700, 125)

        # central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Parameters transmission between tabs
        self.pawns_style = None
        self.game_parameters = None

        # Stacking
        self.stack1 = QWidget(self.centralWidget)
        self.stack2 = QWidget(self.centralWidget)

        self.Stack = QStackedWidget(self)
        MenuTab(self.centralWidget, self.Stack, self.stack1, self)
        GameTab(self.centralWidget, self.Stack, self.stack2, self)

        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)

        # laying out
        self.baselayout = QVBoxLayout(self.centralWidget)
        self.baselayout.addWidget(self.Stack)

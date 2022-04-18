from PyQt5.QtWidgets import *
from gui.MainMenu import MainMenu
from gui.GameTab import GameTab
from game.GameEngine import GameEngine


class WindowUI(QMainWindow):
    def __init__(self):
        # window pars
        super(WindowUI, self).__init__()
        self.setMinimumSize(900, 700)
        self.setWindowTitle("Almanach")

        # central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # game manager
        self.game_engine = GameEngine(None)

        # Stacking
        self.stack1 = QWidget(self.centralWidget)
        self.stack2 = QWidget(self.centralWidget)

        self.Stack = QStackedWidget(self)
        MainMenu(self.centralWidget, self.Stack, self.stack1, self)
        GameTab(self.centralWidget, self.Stack, self.stack2, self)

        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)

        # laying out
        self.baselayout = QVBoxLayout(self.centralWidget)
        self.baselayout.addWidget(self.Stack)

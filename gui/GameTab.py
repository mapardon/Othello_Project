from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.ClickableIcon import ClickableIcon
from gui.WindowUtils import WindowUtils
from game.GameEngine import GameEngine


class GameTab(WindowUtils):
    class Tile(ClickableIcon):
        """ClickableIcon with its tile number on the board"""
        def __init__(self, number, icon):
            super(GameTab.Tile, self).__init__(icon)
            self.number = number

    def __init__(self, centralWidget, baseStack, ownStack, wrap):
        super(GameTab, self).__init__(wrap)
        self.baseStack = baseStack

        # game management
        self.player_move = None
        self.game_ended = False

        # TODO delete
        self.dummy_parameter = 7

        # Main title {{{
        main_title = QLabel("Play the Game")
        main_title.setFont(QFont('Courier', 18))

        # laying out
        title_layout = self.horizontal_menu_widget_layouter(main_title)
        # }}}

        # back / start buttons {{
        go_back_btn = QPushButton("Back", centralWidget)
        go_back_btn.setMinimumWidth(250)
        start_btn = QPushButton("Start", centralWidget)
        start_btn.setMinimumWidth(250)

        # Connect
        go_back_btn.clicked.connect(lambda: self.go_back(0))
        start_btn.clicked.connect(lambda: self.game_launched())

        go_back_lt = self.horizontal_menu_widget_layouter(go_back_btn, start_btn)
        # }}

        # Board {{

        self.tiles_list = list()
        self.board_lt = QGridLayout()

        for x in range(8):
            for y in range(8):
                tile = GameTab.Tile(8 * x + y, "icons/white.png")
                tile.clicked.connect(lambda: self.tile_clicked())
                #tile.setDisabled(True)
                self.board_lt.addWidget(tile, x, y)
                self.tiles_list.append(tile)
        self.board_lt.setSpacing(0)
        self.board_lt.setAlignment(Qt.AlignCenter)
        # }}

        self.gametab_layout = QVBoxLayout()
        self.gametab_layout.addLayout(title_layout)
        self.gametab_layout.addStretch()
        self.gametab_layout.addLayout(self.board_lt)
        self.gametab_layout.addStretch()
        self.gametab_layout.addLayout(go_back_lt)
        self.gametab_layout.addStretch()

        ownStack.setLayout(self.gametab_layout)

    def game_launched(self):
        """ Game is run in a QThread, this functions launches the thread and connects signals """
        # Initialization of the QThread object
        self.thread = QThread()
        self.worker = GameEngine(self)
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # Other slots
        self.worker.progress.connect(self.update_board)

        # Start the thread
        self.thread.start()

        # Eventual other final resets can be implemented here

    def update_board(self, board):
        for i, v in enumerate(board):
            self.tiles_list[i].editPixmap("icons/white" if v is None else "icons/undyne" if not v else "icons/sans")

    def input_request(self):
        """ Player has to make a move """
        self.player_move = None  # reset from previous time

        while self.player_move is None:
            continue

    def game_finished(self):
        """ Kind of strong coupling with GameEngine but this was the easiest for UI connection """
        print("game finished")

    def tile_clicked(self):
        self.player_move = self.sender().number

    def go_back(self, menu_index):
        for tile in self.tiles_list:
            tile.editPixmap("icons/white")
        self.baseStack.setCurrentIndex(menu_index)

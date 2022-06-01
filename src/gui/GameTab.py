from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.game.GameEngine import GameEngine, wait_condition
from src.gui.ClickableIcon import ClickableIcon
from src.gui.WindowUtils import WindowUtils

icon_directory = "./src/icons"

class GameTab(WindowUtils):
    """ Defines UI elements for a game between agents or humans """

    class Tile(ClickableIcon):
        """ ClickableIcon (see inherited class) with a number representing its position on the board """
        def __init__(self, number, icon):
            super(GameTab.Tile, self).__init__(icon)
            self.number = number

    def __init__(self, centralWidget, baseStack, ownStack, wrap):
        """ Widgets declaration and connection to methods """

        super(GameTab, self).__init__(wrap)
        self.baseStack = baseStack
        self.icon_p1 = None
        self.icon_p2 = None

        # Main title {{{
        main_title = QLabel("Play the Game")
        main_title.setFont(QFont('Courier', 18))

        # laying out
        title_layout = self.horizontal_menu_widget_layout(main_title)
        # }}}

        # back / start buttons {{
        self.go_back_btn = QPushButton("Back", centralWidget)
        self.go_back_btn.setMinimumWidth(250)
        self.start_btn = QPushButton("Start", centralWidget)
        self.start_btn.setMinimumWidth(250)

        # Connect
        self.go_back_btn.clicked.connect(lambda: self.return_config_menu(0))
        self.start_btn.clicked.connect(lambda: self.game_launched())

        buttons_lt = self.horizontal_menu_widget_layout(self.go_back_btn, self.start_btn)
        # }}

        # Board {{
        self.tiles_list = list()
        self.board_lt = QGridLayout()

        for x in range(8):
            for y in range(8):
                tile = GameTab.Tile(8 * x + y, icon_directory+"/green.png")
                tile.clicked.connect(lambda: self.tile_clicked())
                tile.setDisabled(True)
                self.board_lt.addWidget(tile, x, y)
                self.tiles_list.append(tile)
        self.board_lt.setSpacing(0)
        self.board_lt.setAlignment(Qt.AlignCenter)
        # }}

        # Game informations {{
        ginfo_subtitle = QLabel("Game info", centralWidget)
        ginfo_subtitle.setFont(QFont('Courier', 12))

        self.ginfo_dsp = QLabel("", centralWidget)
        self.ginfo_dsp.setFont(QFont('Courier', 10))

        # laying out
        ginfo_lt = QVBoxLayout()
        ginfo_lt.addWidget(ginfo_subtitle)
        ginfo_lt.addWidget(self.ginfo_dsp)
        ginfo_lt.addStretch()
        # }}

        game_layout = QVBoxLayout()
        game_layout.addWidget(main_title, alignment=Qt.AlignCenter)
        game_layout.addStretch()
        game_layout.addLayout(self.board_lt)
        game_layout.addStretch()
        game_layout.addLayout(buttons_lt)
        game_layout.addStretch()

        self.gametab_layout = QHBoxLayout()
        self.gametab_layout.addLayout(ginfo_lt)
        self.gametab_layout.addLayout(game_layout)

        ownStack.setLayout(self.gametab_layout)

    def game_launched(self):
        """ Game is run in a QThread, this functions launches the thread and connects signals """

        # choose pawns style
        self.icon_p1, self.icon_p2 = (icon_directory+"/black_dot_green.png", icon_directory+"/white_dot_green.png") if self.wrap.pawns_style == "classic" else (icon_directory+"/undyne.png", icon_directory+"/sans.png")
        self.toggle_buttons_activation()

        # Initialization of the QThread object
        self.thread = QThread()
        self.worker = GameEngine(self, self.wrap.game_parameters)
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.toggle_buttons_activation)

        # Other signals & slots
        self.worker.match_progress.connect(self.update_board)
        self.worker.input_request.connect(self.toggle_tiles_activation)
        self.worker.match_log.connect(self.ginfo_dsp.setText)

        # Start the thread
        self.thread.start()

    def update_board(self, board):
        for i, v in enumerate(board):
            self.tiles_list[i].editPixmap(icon_directory+"/green" if v is None else self.icon_p1 if not v else self.icon_p2)

    def toggle_tiles_activation(self):
        """ Player has to make a move
        :parameter enable: indicates if input is needed (True) or not needed anymore (False) """
        value = self.tiles_list[0].isEnabled()
        for tile in self.tiles_list:
            tile.setDisabled(value)

    def toggle_buttons_activation(self):
        value = self.start_btn.isEnabled()
        for btn in [self.start_btn, self.go_back_btn]:
            btn.setDisabled(value)

    def tile_clicked(self):
        self.worker.player_move = self.sender().number
        self.toggle_tiles_activation()
        wait_condition.wakeAll()

    def return_config_menu(self, menu_index):
        for tile in self.tiles_list:
            tile.editPixmap(icon_directory+"/green")
        self.ginfo_dsp.setText("")
        self.baseStack.setCurrentIndex(menu_index)

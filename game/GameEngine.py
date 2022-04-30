import time
from math import ceil

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal

from game.OthelloGame import OthelloGame
from game.PlayerHuman import PlayerHuman
from ai.PlayerML import PlayerML
from ai.PlayerMinimax import PlayerMinimax
from ai.PlayerRandom import PlayerRandom
from db.NNstorage import *


""" Communication with UI thread """
wait_condition = QtCore.QWaitCondition()
mutex = QtCore.QMutex()


class GameEngine(QObject):
    """ Perform initializations and supervises progress of the game:
        * Make players choose a move alternatively
        * In match loop, request inputs to the UI (if any human player is part of the game)
        * In train and compare loops, run game several times and send progression and/or result to the UI

    :param game_parameters: {mode: match | train | compare,
                             player1: {type: human | random | minimax | ml agent,
                                       pars: {network_name, eps, [mv_selec, ls, lr, act_f] | ehits, eps}
                                        },
                             player2: {type: human | random | minimax | ml agent,
                                       pars: {network_name, eps, [mv_selec, ls, lr, act_f] | ehits, eps}
                                        },
                            nb_games}
    """

    # Communication signals with main thread
    match_progress = pyqtSignal(list)
    match_log = pyqtSignal(str)
    input_request = pyqtSignal()
    train_progress = pyqtSignal(int)
    compare_progress = pyqtSignal(int)
    compare_result = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, ui_reference, game_parameters):
        super().__init__()
        self.ui_reference = ui_reference

        self.game_parameters = game_parameters
        self.players = list()
        self.game = None

        # player move (used to receive user input from gui)
        self.player_move = None

    def run(self):
        """Long-running task."""
        self.configure_game()

        if self.game_parameters["mode"] == "match":
            self.match_loop()
        elif self.game_parameters["mode"] == "train":
            self.train_agent()
        elif self.game_parameters["mode"] == "compare":
            self.compare_agents()

        self.finished.emit()

    def configure_game(self):
        """ Initialize game and instantiate players objects (depending on the strategy) """

        # initialize board
        self.game = OthelloGame()

        # initialize players
        self.players.clear()

        if self.game_parameters["mode"] == "match" or self.game_parameters["mode"] == "compare":
            for role, player in enumerate(("player1", "player2")):
                if self.game_parameters[player]["type"] == "human":
                    self.players.append(PlayerHuman(role))
                elif self.game_parameters[player]["type"] == "random":
                    self.players.append(PlayerRandom(role))
                elif self.game_parameters[player]["type"] == "minimax":
                    self.players.append(PlayerMinimax(role, self.game_parameters[player]["pars"]))
                elif self.game_parameters[player]["type"] == "ml agent":
                    self.game_parameters[player]["pars"]["ls"], self.game_parameters[player]["pars"]["act_f"], w_int, w_out = load_network(self.game_parameters[player]["pars"]["network_name"])
                    network = w_int, w_out
                    self.players.append(PlayerML(self.game_parameters["mode"], role, network,
                                                 self.game_parameters[player]["pars"]))

        elif self.game_parameters["mode"] == "train":  # ML only
            self.game_parameters["player1"]["pars"]["ls"], self.game_parameters["player1"]["pars"]["act_f"], w_int, w_out = load_network(self.game_parameters["player1"]["pars"]["network_name"])
            network = w_int, w_out
            self.players += [PlayerML(self.game_parameters["mode"], 0, network,
                                      self.game_parameters["player1"]["pars"]),
                             PlayerML(self.game_parameters["mode"], 1, network,
                                      self.game_parameters["player1"]["pars"])]

    def train_agent(self):
        t = time.time()  # performance measure
        nb = self.game_parameters["nb_games"]

        for i in range(nb):
            if not (i % int(nb / 100)):  # display progression
                self.train_progress.emit(ceil(100 * i / nb))
            self.train_loop()
            self.game.init_board()  # reinit board

        # save results
        update_network(self.game_parameters["player1"]["pars"]["network_name"], self.players[0].network[0], self.players[0].network[1])

        # outro
        self.train_progress.emit(100)
        print("Ran {} games in {} seconds".format(nb, round(time.time() - t, 2)))

    def compare_agents(self):

        score = [int(), int()]
        nb = self.game_parameters["nb_games"]

        for i in range(nb):
            if not (i % int(nb / 100)):
                self.compare_progress.emit(ceil(100 * i / nb))

            score[self.compare_loop()] += 1
            self.game.init_board()

        # outro
        self.compare_progress.emit(100)
        self.compare_result.emit("Black won {}%".format(round(100 * score[0] / nb, 2)))

    # Game loops #

    def match_loop(self):
        """ Implements game player vs AI, display board after each move. """
        end = False
        log = str()
        p = int()  # index for players, black is first index
        prev_no_play = False

        while not end:
            cur_player = self.players[p]  # each player in turn

            self.match_progress.emit(self.game.get_board())  # send update of board

            (not isinstance(cur_player, PlayerHuman) or log) and time.sleep(1.2)  # short break before AI move

            new_move = self.game.player_has_move(cur_player.get_role())  # check if available move
            if new_move:
                new_move = None

                if isinstance(cur_player, PlayerHuman):
                    while new_move is None:
                        self.input_request.emit()

                        # wait for input...
                        mutex.lock()
                        wait_condition.wait(mutex)
                        mutex.unlock()

                        new_move = self.game.is_valid_move(cur_player.get_role(), divmod(self.player_move, 8))
                else:
                    new_move = cur_player.make_move(self.game)

                old = self.game.get_board()  # allow to display ai move, no other use
                self.game.swap_states(new_move)

                end = self.game.all_tiles_used()
                prev_no_play = False

            else:
                if prev_no_play:
                    end = True
                prev_no_play = True
                self.match_log.emit("{} had no option".format("Black" if not p else "White"))

            p = (p + 1) % 2

        self.match_progress.emit(self.game.get_board())

        log = str()
        if prev_no_play:
            log += "Game reached frozen state\n"
        log += "White white_victory" if self.game.white_victory() else "Black white_victory"
        self.match_log.emit(log)

    def train_loop(self):
        end = False
        p = int()
        no_play = False

        while not end:
            cur_player = self.players[p]
            new_move = cur_player.make_move(self.game)

            if new_move is not None:
                self.game.swap_states(new_move)
                no_play = False
                end = self.game.all_tiles_used()
            else:
                if no_play:
                    end = True
                no_play = True

            p = (p + 1) % 2

        victory = self.game.white_victory()
        self.players[0].end_game(self.game, victory)

    def compare_loop(self):

        end = False
        p = int()
        no_play = False

        while not end:
            cur_player = self.players[p]
            new_move = cur_player.make_move(self.game)

            if new_move is not None:
                self.game.swap_states(new_move)
                no_play = False
                end = self.game.all_tiles_used()
            else:
                if no_play:
                    end = True
                no_play = True

            p = (p + 1) % 2

        return False if no_play else self.game.white_victory()

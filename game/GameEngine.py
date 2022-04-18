import os
import time

import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal

from ai.ml_utils import createNN
from game.OthelloGame import OthelloGame
from game.PlayerHuman import PlayerHuman
from game.PlayerML import PlayerML
from game.PlayerRandom import PlayerRandom


class GameEngine(QObject):
    """ Supervises the progress of the game: perform initializations, run adequate loop (fight, train or compare) and
    request moves alternatively between two players to send them to OthelloGame instance. """

    finished = pyqtSignal()
    progress = pyqtSignal(list)

    def __init__(self, ui_reference):
        super().__init__()
        self.ui_reference = ui_reference
        self.game_parameters = {"type_ai": "random"}
        self.game_finished = False

        self.opponents = None
        self.game_board = None

    def run(self):
        """Long-running task."""
        self.initialize_parameters()
        self.fight_loop()

        self.finished.emit()

    def initialize_parameters(self):

        # initialize players + board
        self.game_board = OthelloGame()
        self.game_finished = False

        human_player = PlayerHuman(0, self.ui_reference)
        if self.game_parameters["type_ai"] == "random":
            artificial_player = PlayerRandom(1)
        elif self.game_parameters["type_ai"] == "ML":
            artificial_player = PlayerRandom(1)
        elif self.game_parameters["type_ai"] == "minimax":
            artificial_player = PlayerRandom(1)
        else:
            # TODO remove after testing
            print("shouldn't have landed here (NeoGameEngine)")
            artificial_player = PlayerRandom(1)
        opponents = [human_player, artificial_player]

        # TODO delete
        self.opponents = [PlayerRandom(0), PlayerRandom(1)]

    def train_agent(self):
         return

    def compare_agents(self):
        return

    def manager(self, mode, b_player, AI1, AI2, nb, ls, lr, eps, lamb):
        """ AI1/2 : contain information required for initializing or loading agents (new/load ; [median layer size ;]
        filename) ; nb is number of games.
        May raise TypeError if called with exit message """

        if mode == "fight":
            opponents = [PlayerHuman(0), self.othellist(mode, 1, AI1, None, None, float(), None)]
            # match: ai only does best moves
            if b_player != "Human":
                opponents.reverse()
                opponents[0].switch_role()
                opponents[1].switch_role()
            # run
            self.fight_loop(opponents)
            feedback = str()

        elif mode == "train":
            opponents = [*self.othellist(mode, 0, AI1, ls, lr, eps, lamb)]
            t = time.time()
            for i in range(nb):
                if not (i % int(nb / 100)):  # display progression
                    os.system('clear')
                    print("Loops achieved : {}%".format(round(i / nb, 2) * 100))
                self.train_loop(opponents)
                self.game_board.init_board()

            # save results
            out = AI1[2] if AI1[0] == "new" else AI1[1]
            network = opponents[0].network
            np.savez(out, Wi=network[0], Wo=network[1])

            # outro
            os.system('clear')
            input("Ran {} games in {} seconds > ".format(nb, round(time.time() - t, 2)))
            feedback = "Trained and saved AI1 on {} games".format(nb)

        else:
            # Rmk : In comparison mode, we can specify an eps to measure ability of ais to react to a sub-optimal move
            opponents = [self.othellist(mode, 0, AI1, None, None, eps, None),
                         self.othellist(mode, 1, AI2, None, None, eps, None)]
            score = [int(), int()]

            # gas
            for i in range(nb):
                if not (i % int(nb / 100)):
                    os.system('clear')
                    print("Loops achieved : {}%".format(round(i / nb, 2) * 100))

                score[self.compare_loop(opponents)] += 1
                self.game_board.init_board()

            # outro
            os.system('clear')
            input("Victories of black on {} games : {} > ".format(nb, round(100 * score[0] / nb, 2)))
            feedback = "Compared AIs on {} games".format(nb)
            self.save_results("{} vs {} won {}% (eps={})".format(AI1[1], AI2[1], round(100 * score[0] / nb, 2), eps))

        return feedback

    def othellist(self, mode, role, ai_source, ls, lr, eps, lamb):
        """ Parameters processing for the creation of ai player. """

        if ai_source[0] == "new":
            network = createNN(128, ai_source[1])
        else:
            data = np.load(ai_source[1])
            network = data['Wi'], data['Wo']

        if ls == "Q-learning":
            strategy = ("Q-learning", lr)
        elif ls == "TD-lambda":
            z_network = np.zeros(network[0].shape), np.zeros(network[1].shape)
            strategy = ("TD-lambda", lr, lamb, *z_network)
        else:
            strategy = None

        if mode == "train":  # must share same matrices object
            return PlayerML(role, network, strategy, eps), PlayerML(not role, network, strategy, eps)
        else:
            return PlayerML(role, network, strategy, eps)

    def fight_loop(self):
        """ Implements game player vs AI, display board after each move. """
        end = False
        log = str()
        p = int()  # index for players, black is first index
        prev_no_play = False
        game_board = self.game_board

        while not end:
            cur_player = self.opponents[p]  # each player in turn

            (not isinstance(cur_player, PlayerHuman) or log) and time.sleep(1.2)  # short break before AI move
            print(log)
            self.progress.emit(game_board.get_board())  # send update of board

            new_move = cur_player.make_move(game_board)
            if new_move is not None:
                old = game_board.get_board()  # display ai move, no other use
                game_board.swap_states(new_move)

                # TODO check if useful
                # display coordinates of AI move (if ever useful in way or another)
                if not isinstance(cur_player, PlayerHuman):
                    for i in range(64):
                        if old[i] is None and game_board.get_board()[i] is not None:
                            log = "AI played ({}, {})".format(*(k + 1 for k in divmod(i, 8)))

                end = game_board.all_tiles_used()
                prev_no_play = False
            else:
                if prev_no_play:
                    end = True
                prev_no_play = True
                log = "{} had no option".format("Black" if not p else "White")

            p = (p + 1) % 2

        self.ui_reference.update_board(game_board.get_board())

        self.ui_reference.set_game_ended(True)

        if not prev_no_play:
            print("Game reached frozen state (no play possible)")
        print("White won") if game_board.victory() else print("Black won")

    def train_loop(self, opponents):
        end = False
        p = int()
        no_play = False

        while not end:
            cur_player = opponents[p]
            new_move = cur_player.make_move(self.game_board)

            if new_move is not None:
                self.game_board.swap_states(new_move)
                no_play = False
                end = self.game_board.all_tiles_used()
            else:
                if no_play:
                    end = True
                no_play = True

            p = (p + 1) % 2

        victory = self.game_board.victory()
        opponents[0].end_game(self.game_board, victory)

    def compare_loop(self, opponents):
        end = False
        p = int()
        no_play = False

        while not end:
            cur_player = opponents[p]
            new_move = cur_player.make_move(self.game_board)

            if new_move is not None:
                self.game_board.swap_states(new_move)
                no_play = False
                end = self.game_board.all_tiles_used()
            else:
                if no_play:
                    end = True
                no_play = True

            p = (p + 1) % 2

        return False if no_play else self.game_board.victory()

    def save_results(self, msg):
        with open("results.txt", 'a', encoding='utf-8') as f:
            f.write(msg + '\n')

import random

from game.Player import Player
from game.OthelloGame import OthelloGame

infinity = 100000


class PlayerMinimax(Player):
    def __init__(self, role, agent_parameters):
        print("PlayerMinimax : ", role, agent_parameters)
        super(PlayerMinimax, self).__init__(role)
        self.max_depth = agent_parameters["ehits"]  # check that depth > 0
        self.eps = agent_parameters["eps"]
        # self.max_depth = 1

    def make_move(self, game):
        """ :returns None if no play is available """

        if not game.player_has_move(self.role):
            print("minimax no moves", game.player_has_move(self.role))
            return None
        else:  # TODO minimax
            v, move = self.minimax(game.get_board(), self.max_depth, True)
            return move

    def minimax(self, state, depth, player):  # without prunning
        if depth == 0:  # or game over
            v = self.evaluate_state(player, state)  # gives a numeric evaluation of this state
            return v, state
        if player:  # max
            max_eval = -infinity
            moves = self.possible_moves(state, player)
            best_move = None
            for m in moves:
                v, n_s = self.minimax(m, depth - 1, (
                            player + 1) % 2)  # next_state is not use, unless for the last return (which is really played)
                if v > max_eval:
                    max_eval = v
                    best_move = m
            return max_eval, best_move
        else:  # min
            min_eval = infinity
            moves = self.possible_moves(state, player)
            best_move = None
            for m in moves:
                v, n_s = self.minimax(m, depth - 1, (player + 1) % 2)
                if v < min_eval:
                    min_eval = v
                    best_move = m
            return min_eval, best_move

    def possible_moves(self, state, player):
        board = OthelloGame()
        board.swap_states(state)
        return board.playable_moves(player)

    def evaluate_state(self, player, state):  # TODO: choisir poids de chaque heuristique
        eval = 1 * self.count_corner_coin(player, state) + -1 * self.count_close_corner_coint(player, state) \
               + -1 * self.count_frontier_discs(player, state) \
               + 1 * self.count_coins(player, state) + 1 * self.count_possible_moves(player, state)

        return eval

    def count_possible_moves(self, player, state):

        return len(self.possible_moves(state, player))

    def count_coins(self, player, board):
        if player == 1:
            return board.count(1)
        return board.count(0)

    def count_corner_coin(self, player, board):  # advantage

        return int(board[0] == player) + int(board[7] == player) + int(board[55] == player) + int(board[63] == player)

    def count_close_corner_coint(self, player, board):  # disavantage
        close_to_corner = [1, 8, 9, 6, 14, 15, 48, 49, 57, 54, 55, 62]

        tot = 0
        for i in close_to_corner:
            if board[i] == player:
                tot += 1
        return -tot

    def count_frontier_discs(self, player, board):  # try to minimize number of discs adjacent to empty square

        tot = 0
        for i in board:
            if i == player:
                if self.is_adjecent_empty(player, board):
                    tot += 1

        return tot

    def is_adjecent_empty(self, pos, board):

        for adj in [-1, -9, -8, -7, 1, 9, 8, 7]:
            if 0 <= pos + adj <= 63:
                if not board[pos + adj]: # adjacent square == None
                    return True
        return False

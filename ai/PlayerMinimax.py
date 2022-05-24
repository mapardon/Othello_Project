import random

from game.Player import Player
from game.OthelloGame import OthelloGame

infinity = 100000


class PlayerMinimax(Player):
    def __init__(self, role, agent_parameters):
        # Weight : #TODO in UI : let user choose the weights of the heuristic
        self.W_CORNER = 5
        self.W_CLOSE_CORNER = 2 # as the next state already evaluate the matter of corner, no need to over evaluate this one ?
        self.W_NEXT_EMPTY = 2 #modify this value during the game ?
        self.W_COINS = 1/3
        self.W_MOVES = 1
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
        if depth == 0 or len(self.possible_moves(state, player)) == 0 :  # or game over TODO
            state_eval = self.evaluate_state(player, state)  # gives a numeric evaluation of this state
            return state_eval, state
        if player:  # max
            max_eval = -infinity
            moves = self.possible_moves(state, player)
            best_move = None
            for m in moves:
                state_eval, n_s = self.minimax(m, depth - 1, (
                            player + 1) % 2)  # next_state is not used, except for the last return (which is played)
                if state_eval > max_eval:
                    max_eval = state_eval
                    best_move = m
            return max_eval, best_move
        else:  # min
            min_eval = infinity
            moves = self.possible_moves(state, player)
            best_move = None
            for m in moves:
                state_eval, n_s = self.minimax(m, depth - 1, (player + 1) % 2)
                if state_eval < min_eval:
                    min_eval = state_eval
                    best_move = m
            return min_eval, best_move

    def possible_moves(self, state, player):
        board = OthelloGame()
        board.swap_states(state)
        return board.playable_moves(player)

    def evaluate_state(self, player, state):
        eval =     1 * infinity * self.has_won(player, state) \
                + -1 * infinity * self.has_won((player+1)%2, state) \
                +  1 * self.W_CORNER * self.count_corner_coin(player, state) \
                + -1 * self.W_CORNER * self.count_corner_coin((player+1)%2, state) \
                + -1 * self.W_CLOSE_CORNER * self.count_close_corner_coint(player, state) \
                +  1 * self.W_CLOSE_CORNER * self.count_close_corner_coint((player+1%2), state) \
                + -1 * self.W_NEXT_EMPTY * self.count_frontier_discs(player, state) \
                +  1 * self.W_NEXT_EMPTY * self.count_frontier_discs((player+1)%2, state) \
                +  1 * self.W_COINS * self.count_coins(player, state) \
                + -1 * self.W_COINS * self.count_coins((player+1)%2, state) \
                +  1 * self.W_MOVES * self.count_possible_moves(player, state) \
                + -1 * self.W_MOVES * self.count_possible_moves((player+1%2), state)
        print(eval)
        return eval

    def count_possible_moves(self, player, state):
        return len(self.possible_moves(state, player))

    def count_coins(self, player, state):
        if player == 1:
            return state.count(1)
        return state.count(0)

    def count_corner_coin(self, player, state):  # advantage
        return int(state[0] == player) + int(state[7] == player) + int(state[55] == player) + int(state[63] == player)

    def count_close_corner_coint(self, player, state):  # disavantage
        close_to_corner = [1, 8, 9, 6, 14, 15, 48, 49, 57, 54, 55, 62]

        tot = 0
        for i in close_to_corner:
            if state[i] == player: #tot += int(state[i] == player) pour le faire à la Roggeman
                tot += 1
        return -tot #Delete le -1 ??

    def count_frontier_discs(self, player, state):  # try to minimize number of discs adjacent to empty square

        tot = 0
        for i in state:
            if i == player:
                if self.is_adjecent_empty(player, state):
                    tot += 1

        return tot

    def is_adjecent_empty(self, pos, state):

        for adj in [-1, -9, -8, -7, 1, 9, 8, 7]:
            if 0 <= pos + adj <= 63:
                if not state[pos + adj]: # adjacent square == None
                    return True
        return False

    def has_won(self, player, state) :
        if state.count(None) == 0 :
            if state.count(player) > state.count((player+1)%2) :
                return True
        return False
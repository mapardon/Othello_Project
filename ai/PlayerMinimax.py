import random

from game.Player import Player

infinity = 100000

class PlayerMinimax(Player):
    def __init__(self, role, agent_parameters):
        print("PlayerMinimax : ", role, agent_parameters)
        super(PlayerMinimax, self).__init__(role)
        self.early_hits = agent_parameters["ehits"]
        self.eps = agent_parameters["eps"]
        self.max_depth = 5

    def make_move(self, game):
        """ :returns None if no play is available """

        if not game.player_has_move(self.role) :
            return None
        else:  # TODO minimax
            v, move = self.minimax(game.get_board, self.max_depth, True)
            return move


    def minimax(self, state, depth, player) : #without prunning
        if depth == 0 :#or game over
            v = self.evaluate_state(state) #gives a numeric evaluation of this state
            return v, state
        if player : #max
            max_eval = -infinity
            moves = self.possible_moves(state)
            best_move = None
            for m in moves :
                v, n_s = self.minimax(m, depth-1, (player+1)%2) #next_state is not use, unless for the last return (root)
                if v > max_eval :
                    max_eval = v
                    best_move = m
            return max_eval, best_move
        else : #min
            min_eval = infinity
            moves = self.possible_moves(state)
            best_move = None
            for m in moves :
                v, n_s = self.minimax(m, depth - 1, (player + 1) % 2)
                if v < min_eval :
                    min_eval = v
                    best_move = m
            return min_eval, best_move

    def possible_moves(self, state): #TODO
        return [None, None, None, None, None, None, None, None, None, None, None, None, 1, None, None, None, None, None, None, None, 1, 1, None, None, None, None, None, 1, 1, 0, 0, 0, None, None, None, 1, 1, None, None, 1, None, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, 1, None, None, None, None, None, None, 1, 1, None, None, None, None, None, 1, 1, 0, 0, 0, None, None, None, 1, 1, None, None, 1, None, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1, 1, 1, None, None, None, None, None, 1, 1, 0, 0, 0, None, None, None, 1, 1, None, None, 1, None, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0, 1, 1, None, None, None, None, 1, 1, 1, 0, 0, None, None, None, 1, 1, None, None, 1, None, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0, 1, None, 1, None, None, None, 1, 1, 0, 0, 1, None, None, None, 1, 1, None, None, 1, None, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0, 1, None, None, None, None, None, 1, 1, 1, 0, 0, None, None, None, 1, 1, 1, None, 1, None, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0, 1, None, None, None, None, None, 1, 1, 0, 0, 0, None, None, None, 1, 1, None, None, 1, None, None, 1, 0, 0, None, None, None, None, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0, 1, None, None, None, None, None, 1, 1, 0, 0, 0, None, None, None, 1, 1, None, None, 1, None, None, 0, 1, 0, None, None, None, None, None, 1, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0, 1, None, None, None, None, None, 1, 1, 0, 0, 0, None, None, None, 1, 1, None, None, 1, None, None, 0, 1, 0, None, None, None, None, None, None, 1, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0, 1, None, None, None, None, None, 1, 1, 0, 0, 0, None, None, None, 1, 1, None, None, 1, None, None, 0, 0, 1, None, None, None, None, None, None, None, 1, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0, 1, None, None, None, None, None, 1, 1, 0, 0, 0, None, None, None, 1, 1, None, None, 1, None, None, 0, 0, 1, None, None, None, None, None, None, None, None, 1, None, None, None, None, None, None, None, None, None, None]


    def evaluate_state(self, state): #TODO
        return 0
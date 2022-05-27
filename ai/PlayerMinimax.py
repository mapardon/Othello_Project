import random

from game.Player import Player
from game.OthelloGame import OthelloGame

infinity = 100000


class PlayerMinimax(Player):
    def __init__(self, role, agent_parameters):
        # Weight : #TODO in UI : let user choose the weights of the heuristic
        self.W_CORNER = 100
        self.W_CLOSE_CORNER = 2
        self.W_NEXT_EMPTY = 2
        self.W_COINS = 1/3
        self.W_MOVES = 1
        super(PlayerMinimax, self).__init__(role)
        self.max_depth = agent_parameters["ehits"]  # check that depth > 0
        self.eps = agent_parameters["eps"]


    def make_move(self, game):
        """ :returns None if no play is available """

        best_move = None
        if not game.player_has_move(self.role):
            print("minimax no moves", game.player_has_move(self.role))
        else:
            if self.max_depth == 0 :
                return random.choice(game.playable_moves(self.role))
            max_eval = -(infinity + 1000)
            for move in game.playable_moves(self.role) :
                v = self.minimax(move, self.max_depth-1, self.role, -infinity, infinity)
                if v > max_eval:
                    max_eval = v
                    best_move = move
        return best_move

    def minimax(self, state, depth, player, alpha, beta):
        if depth == 0 or len(self.possible_moves(state, player)) == 0 :
            state_eval = self.evaluate_state(state)  # gives a numeric evaluation of this state
            return state_eval
        if player:  # max
            max_eval = -(infinity + 1000)
            moves = self.possible_moves(state, player)
            for m in moves:
                state_eval = self.minimax(m, depth - 1, (player + 1) % 2, alpha, beta)  # next_state is not used, except for the last return (which is played)
                max_eval = max(max_eval, state_eval)
                alpha = max(alpha, state_eval)
                if beta <= alpha :
                    return max_eval
            return max_eval
        else:  # min
            min_eval = (infinity + 1000)
            moves = self.possible_moves(state, player)
            for m in moves:
                state_eval = self.minimax(m, depth - 1, (player + 1) % 2, alpha, beta)
                min_eval = min(min_eval, state_eval)
                beta = min(beta, state_eval)
                if beta <= alpha :
                    return min_eval
            return min_eval

    def possible_moves(self, state, player):
        board = OthelloGame()
        board.swap_states(state)
        return board.playable_moves(player)

    def evaluate_state(self, state):
        """Evaluate the state, return a numerical value.
        The evaluation depends on differents strategies, each is weighted by a parameter.
        The strategies are the following :
        eval =      +the player has won - the other player has won
                    +the number of corner owned by the player - corners owned by other player
                    -the number of pawns next to a corner + pawns of the other player next to a corner
                    (this one is not very important, because if, because of a pawn next to a corner, a corner can be taken, it will be weighted at the next state)
                    - there are a lot of empty squares next the player'pawns + same for the other player
                    + the number of pawn of the player - the number of pawns of the other player
                    + the number of possible moves - possible moves of the other player
        other things that can be added :
            - number of pawns along the side (except corner and next-to-corner)
                    """
        player = self.role
        return     1 * infinity * self.has_won(player, state) \
                + -1 * infinity * self.has_won((player+1)%2, state) \
                +  1 * self.W_CORNER * self.count_corner_coin(player, state) \
                + -1 * self.W_CORNER * self.count_corner_coin((player+1)%2, state) \
                +  1 * self.W_CLOSE_CORNER * self.count_close_corner_coint(player, state) \
                + -1 * self.W_CLOSE_CORNER * self.count_close_corner_coint((player+1)%2, state) \
                +  1 * self.W_NEXT_EMPTY * self.count_frontier_discs(player, state) \
                + -1 * self.W_NEXT_EMPTY * self.count_frontier_discs((player+1)%2, state) \
                +  1 * self.W_COINS * self.count_coins(player, state) \
                + -1 * self.W_COINS * self.count_coins((player+1)%2, state) \
                +  1 * self.W_MOVES * self.count_possible_moves(player, state) \
                + -1 * self.W_MOVES * self.count_possible_moves((player+1)%2, state)

    def count_possible_moves(self, player, state):
        return len(self.possible_moves(state, player))

    def count_coins(self, player, state):
        if player == 1:
            return state.count(1)
        return state.count(0)

    def count_corner_coin(self, player, state):  # advantage
        return int(state[0] == player) + int(state[7] == player) + int(state[55] == player) + int(state[63] == player)

    def count_close_corner_coint(self, player, state):  # disavantage
        #do not take into account if he corner is already taken by one of the 2 player
        close_to_corner = [1, 8, 9, 6, 14, 15, 48, 49, 57, 54, 55, 62]

        tot = 0
        for i in close_to_corner:
            if state[i] == player: #tot += int(state[i] == player) pour le faire à la Roggeman
                tot += 1
        return - tot

    def count_frontier_discs(self, player, state):  # try to minimize number of discs adjacent to empty square

        tot = 0
        for i in state:
            if i == player:
                if self.is_adjecent_empty(player, state):
                    tot += 1

        return -tot

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
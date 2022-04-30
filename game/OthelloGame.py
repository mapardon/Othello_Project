import copy
import numpy as np


class OthelloGame:
    """ Implementation of the mechanisms of the game: contains parameter board (representation of the board of the game)
    and implements several operations related to the game (apply move, verify if a move is valid, if the game is
    finished...). When players need to be taken into account, 0 is black player, 1 is white. """

    def __init__(self):
        self.board = None
        self.array = None  # store array equivalent to avoid computing it twice if possible
        self.init_board()

    def init_board(self):
        """ Create 1d list and set center boxes to initial values. 1d lists is motivated by its
        performances on binary vector conversion and copy operations. """

        self.board = [None] * 64
        self.board[3 * 8 + 3] = self.board[4 * 8 + 4] = True
        self.board[3 * 8 + 4] = self.board[4 * 8 + 3] = False

    def get_board(self):
        return self.board

    def swap_states(self, new_state):
        """ Setter for parameter self.board. """

        if len(new_state) == 64:
            self.board = new_state
        else:  # under the form of binary vector, conversion required
            self.array = new_state
            for i in range(64):
                if new_state[i] == 1:
                    self.board[i] = 0
                elif new_state[i+64] == 1:
                    self.board[i] = 1
                else:
                    self.board[i] = None

    # Game related operations #

    def is_valid_move(self, player, move):
        """ Checks if placing a piece in given coordinates is a rules-friendly move.

        :param player: integer symbol of player attempting the move
        :param move: tuple of non-negatives numbers representing the indices
        :returns game state (type of _board) after playing specified move if it is valid """

        adjacent = (player + 1) % 2
        leads = list()
        x, y = move  # /!\ x is line index, represents the "height"

        # targeted box is already used
        if self.board[x * 8 + y] is not None:
            return None

        # look for adjacent pieces around box
        if x > 1:  # upper line
            self.board[(x - 1) * 8 + y] == adjacent and leads.append((-1, 0))
            if y > 1:
                self.board[(x - 1) * 8 + y - 1] == adjacent and leads.append((-1, -1))
            if y < 6:
                self.board[(x - 1) * 8 + y + 1] == adjacent and leads.append((-1, 1))

        if y > 1:  # left
            self.board[x * 8 + y - 1] == adjacent and leads.append((0, -1))

        if y < 6:  # right
            self.board[x * 8 + y + 1] == adjacent and leads.append((0, 1))

        if x < 6:  # lower line
            self.board[(x + 1) * 8 + y] == adjacent and leads.append((1, 0))
            if y > 1:
                self.board[(x + 1) * 8 + y - 1] == adjacent and leads.append((1, -1))
            if y < 6:
                self.board[(x + 1) * 8 + y + 1] == adjacent and leads.append((1, 1))

        if not leads:
            # at this point, no explorable direction means piece is either isolated or has no opponent adjacent
            return None

        # search for peer piece in alignments (discard non-conclusive leads)
        usable = list()
        for d in leads:
            dx, dy = move[0] + d[0], move[1] + d[1]
            found = False
            while not found and 0 <= dx < 8 and 0 <= dy < 8 and self.board[dx * 8 + dy] is not None:
                found = self.board[dx * 8 + dy] == player
                dx += d[0]
                dy += d[1]
            found and usable.append(d)

        if not usable:  # there was no usable adjacent
            return None

        return self.play_move(player, move, usable)

    def play_move(self, player, move, leads):
        """ Returns copy of game state if provided move was played (set of afterstates is required for ai agents).
        Parameter move is supposed valid.

        :param move: move to play, tuple of integers
        :param leads: list of directions to update, used to avoid re-verifying "updatable directions" considering
        is_valid_move already executes these verifications
        :param player: color making the move """

        after_state = copy.copy(self.board)
        for d in leads:
            dx, dy = move[0] + d[0], move[1] + d[1]
            while after_state[dx * 8 + dy] != player:
                after_state[dx * 8 + dy] = player
                dx += d[0]
                dy += d[1]
        # finally : update box where move is played
        after_state[move[0] * 8 + move[1]] = player
        return after_state

    def playable_moves(self, player):
        """ Test all positions and store playable moves for current player.

        :parameter player (0, 1) - indicates whether moves are searched for black or white.
        :returns list of boards representing game if related move is played. """

        moves = list()
        for i in range(64):
            new_move = self.is_valid_move(player, divmod(i, 8))
            if new_move is not None:
                moves.append(new_move)
        return moves

    def player_has_move(self, player):
        """ Check if current player has at least 1 option (otherwise he will not be able to play this turn). """

        return len(self.playable_moves(player)) > 0

    def all_tiles_used(self):
        """ :returns boolean indicating if all boxes are used (and then game is over).
        NB: complete board is not the only possible endstate but mutual blocking is tested in gameloop. """

        return self.board.count(None) == 0

    def white_victory(self):
        """ :returns boolean indicating if white player has won (counts occurrences of True) """

        return self.board.count(True) > (64 - self.board.count(None)) // 2

    def to_array(self, board):
        """ Converts attribute or given board in boolean vector state. Destination type is numpy 1d array.
        N*N first bits represent board with presence of black piece, N*N next same for white pieces.
        :parameter board: if None, checks if self.array is already initialized. Otherwise, convert self.board """
        if board is None:
            if self.array is not None:
                return self.array
            source = self.board
        else:
            source = board

        v = np.zeros(128)
        for i in range(64):
            p = source[i]
            if p is not None:
                v[64 * p + i] = 1
        return v

    def __repr__(self):
        """ Custom representation for terminal """
        b = self.board
        out = "   " + "  ".join([str(i + 1) for i in range(8)]) + '\n'

        for i in range(8):
            for j in range(-1, 8):
                out += str(i + 1) if j == -1 else "-" if b[i * 8 + j] is None else "B" if not b[i * 8 + j] else "W"
                out += '  ' * (j != 8 - 1)
            out += '\n'

        return out

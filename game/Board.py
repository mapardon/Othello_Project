import copy

class Board :
    def __init__(self, board):
        self.board = board

    def __getitem__(self, item):
        return self.board[item]

    def __setitem__(self, key, value):
        self.board[key] = value

    def get_board(self):
        return self.board

    """def playable_moves(self, player):
        "" Test all positions and store playable moves for current player.

        :parameter player (0, 1) - indicates whether moves are searched for black or white.
        :returns list of boards representing game if related move is played. ""

        moves = list()
        for i in range(64):
            new_move = self.is_valid_move(player, divmod(i, 8))
            if new_move is not None:
                moves.append(new_move)
        return moves"""


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
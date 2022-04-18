import random

from ai.Player import Player


class PlayerMinimax(Player):
    def __init__(self, role):
        super(PlayerMinimax, self).__init__(role)

    # TODO: implement minimax algorithm
    def make_move(self, board):
        """ :returns None if no play is available """
        options = board.playable_moves(self._role)
        if not len(options):
            return None
        return random.choice(options)

import random

from game.Player import Player


class PlayerRandom(Player):
    def __init__(self, role):
        super(PlayerRandom, self).__init__(role)

    def make_move(self, board):
        """ :returns None if no play is available """
        options = board.playable_moves(self._role)
        if not len(options):
            return None
        return random.choice(options)

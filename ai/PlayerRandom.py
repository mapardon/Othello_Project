import random

from game.Player import Player


class PlayerRandom(Player):
    def __init__(self, role):
        super(PlayerRandom, self).__init__(role)

    def make_move(self, game):
        """ :returns None if no play is available """
        # TODO ability to make random move
        options = game.playable_moves(self.role)
        if not len(options):
            return None
        return random.choice(options)

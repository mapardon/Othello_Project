import random

from game.Player import Player


class PlayerMinimax(Player):
    def __init__(self, role, agent_parameters):
        super(PlayerMinimax, self).__init__(role)
        self.early_hits = agent_parameters["ehits"]
        self.eps = agent_parameters["eps"]

    # TODO: implement minimax algorithm (here or in another ai_utils)
    def make_move(self, game):
        """ :returns None if no play is available """
        options = game.playable_moves(self.role)
        if not len(options):
            return None
        return random.choice(options)

from game.Player import Player
from ai.ml_utils import makeMove, endGame


class PlayerML(Player):

    def __init__(self, role, network, l_strat, eps):
        """ :param role : important because whole implementation is considered from the point of view of black player.
         Knowing we play the whites implies we must search the least advantageous move. """
        # TODO: initialize agent from scratch HERE

        super().__init__(role)
        self.network = network
        self.strat = l_strat
        self.eps = eps

    def make_move(self, board):
        """ :returns None if no play is available """
        ops = board.playable_moves(self._role)
        if not len(ops):
            return None
        return makeMove([board.to_array(b) for b in ops], board.to_array(None), self._role, self.network, self.eps, self.strat)

    def end_game(self, board, victory):
        endGame(board.to_array(None), victory, self.network, self.strat)

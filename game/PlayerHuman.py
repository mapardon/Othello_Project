from game.Player import Player


class PlayerHuman(Player):
    def __init__(self, role, ui_reference):
        super().__init__(role)
        self.ui_reference = ui_reference  # player move consists in an input request

    def make_move(self, board):
        """ Input request, interaction with ui (GameTab) """

        if not board.playable_moves(self._role):  # checks if at least 1 move is playable
            return None

        after_state = None
        played = False
        while not played:
            move = self.ui_reference.input_request()
            after_state = board.is_valid_move(self._role, tuple(int(i) - 1 for i in move.split(" ")[:2]))
            if after_state is not None:
                played = True
            else:
                print("Move incorrect, send ui feedback message?")

        return after_state

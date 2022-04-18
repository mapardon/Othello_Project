from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, role):
        self._role = role

    def get_role(self):
        return self._role

    def switch_role(self):
        self._role = (self._role + 1) % 2

    @abstractmethod
    def make_move(self, board):
        pass

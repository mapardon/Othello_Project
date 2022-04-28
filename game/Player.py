from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, role):
        self.role = role

    def get_role(self):
        return self.role

    def switch_role(self):
        self.role = (self.role + 1) % 2

    @abstractmethod
    def make_move(self, game):
        pass

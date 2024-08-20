from ..Strategy import Strategy

import random


class ChildStrategy(Strategy):
    def __init__(self):
        super().__init__()

    def decide(self, information):
        self.l_shift = random.uniform(0, 1)
        self.r_shift = random.uniform(0, 1)
        self.risk = random.uniform(0.2, 1)
        self.bluff = random.uniform(0, 1)

        self.initialise(information)

        return self.move


strategy = ChildStrategy()


def decide(state):
    return strategy.decide(state)
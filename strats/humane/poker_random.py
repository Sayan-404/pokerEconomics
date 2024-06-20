# Based on the changing style strategy
# Changes playing style randomly if there's a profitable environment

from ..Strategy import Strategy
import random


class PokerRandom(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)
        self.style = random.randrange(0, 2)

    def decide(self, information):
        self.style = random.randrange(0, 2)
        self.initialise(information)

        if (self.signal is True) or (self.signal is None):
            if self.style == 1:
                return self.defectiveMove

            return self.cooperativeMove

        return self.surrenderMove


strategy = PokerRandom("PokerRandom")


def decide(state):
    return strategy.decide(state)

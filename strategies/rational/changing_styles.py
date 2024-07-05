# Based on the changing style strategy
# Changes playing style randomly if there's a profitable environment

import random

from ..Strategy import Strategy


class ChangingStyles(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)
        self.style = random.randrange(0, 2)

    def decide(self, information):
        self.style = random.randrange(0, 2)
        self.initialise(information, 0)

        if (self.signal is True) or (self.signal is None):
            if self.style == 1:
                return self.prodigalMove

            return self.frugalMove

        return self.surrenderMove


strategy = ChangingStyles("ChangingStyles")


def decide(state):
    return strategy.decide(state)

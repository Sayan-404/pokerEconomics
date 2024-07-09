# Based on the changing style strategy
# Changes playing style randomly if there's a profitable environment

import random

from ..Strategy import Strategy


class ChangingStyles(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)
        self.style = random.randrange(0, 2)

    def decide(self, information):
        self.initialise(information, -2)

        if self.round == 0:
            if self.signal < -0.8:
                return self.surrenderMove

            return random.choice([self.frugalMove, self.prodigalMove])

        if self.round == 1 or self.round == 2:
            if self.signal[0] <= -0.5:
                return self.surrenderMove

            return random.choice([self.frugalMove, self.prodigalMove])

        if self.round == 3:
            if self.signal <= 0.25:
                return self.surrenderMove

            return random.choice([self.frugalMove, self.prodigalMove])


strategy = ChangingStyles("ChangingStyles")


def decide(state):
    result = strategy.decide(state)

    # if strategy.round == 1 or strategy.round == 2:
    #     if (strategy.)S
    #     raise Exception(
    #         f"{strategy.round} {strategy.ehs} {strategy.showdownOdds} {result}")

    return result

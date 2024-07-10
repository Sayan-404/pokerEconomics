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

        r = None

        if self.t_determiner > 0:
            r = random.uniform(self.range[0], self.range[1])

            if random.choice([True, False]):
                r = self.range[0]
        
        if self.t_determiner < 0:
            if self.strength > 0.85 and self.round in [2, 3]:
                r = random.uniform(self.range[0], 1.5)
            else:
                r = self.range[0]

        if r:
            return self.strategicMove(r, information)
        
        return "f", -1


strategy = ChangingStyles("ChangingStyles")


def decide(state):
    result = strategy.decide(state)

    # if strategy.round == 1 or strategy.round == 2:
    #     if (strategy.)S
    #     raise Exception(
    #         f"{strategy.round} {strategy.ehs} {strategy.showdownOdds} {result}")

    return result

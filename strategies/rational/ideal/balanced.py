from ...Strategy import Strategy
from poker_metrics import *


class Ideal(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)

    def decide(self, information):
        self.initialise(information)

        move = ("f", -1)

        if self.t_determiner > 0:
            # In the money
            if self.betAmt != 0:
                move = prodigalMove(information, betAmt=(self.betAmt - self.callValue))
            else:
                move = frugalMove(information)
        if self.t_determiner <= 0:
            # Out of money
            if self.x_privateValue > 0.55:
                move = frugalMove(information)

        return move


strategy = Ideal("Ideal")


def decide(state):
    return strategy.decide(state)

from ...Strategy import Strategy
from poker_metrics import *


class Ideal(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)
        self.l_shift = 2

    def decide(self, information):
        self.initialise(information)

        # if self.move[0] == "b":
        #     raise Exception(f"{self.round} {self.move} {self.holeCards} {self.callValue} {self.pot} {self.y_handEquity} {self.information} ")

        return self.move


strategy = Ideal("Ideal")


def decide(state):
    return strategy.decide(state)

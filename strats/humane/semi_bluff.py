# Based on the semi-bluff strategy
# Bluffs aggressively if there's a signal for good hand
# Else folds

from ..Strategy import Strategy


class SemiBluff(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)

    def decide(self, information):
        self.initialise(information)

        if (self.signal is True):
            return self.defectiveMove

        if (self.signal is None):
            return self.cooperativeMove

        return self.surrenderMove


strategy = SemiBluff("Semi-Bluff")


def decide(state):
    return strategy.decide(state)

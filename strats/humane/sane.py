from ..Strategy import Strategy


class Sane(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)

    def decide(self, information):
        self.initialise(information)

        if (self.signal is True) or (self.signal is None):
            if self.style == 1:
                return self.defectiveMove

            return self.cooperativeMove

        return self.surrenderMove


strategy = Sane("PokerRandom")


def decide(state):
    return strategy.decide(state)

from ..Strategy import Strategy


class Sane(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)

    def decide(self, information):
        self.initialise(information)

        if self.signal is True:
            return self.defectiveMove
        elif self.signal is None:
            return self.cooperativeMove
        else:
            return self.surrenderMove


def decide(state):
    strategy = Sane("Sane")
    return strategy.decide(state)

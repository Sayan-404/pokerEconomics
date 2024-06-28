from ...Strategy import Strategy


class Ideal(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)

    def decide(self, information):
        self.initialise(information, tightness=3)

        if (self.signal is True):
            return self.prodigalMove

        if (self.signal is None):
            return self.frugalMove

        return self.surrenderMove


strategy = Ideal("Ideal")


def decide(state):
    return strategy.decide(state)

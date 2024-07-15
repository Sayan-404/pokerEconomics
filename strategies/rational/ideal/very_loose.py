from ...Strategy import Strategy


class Ideal(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)
        self.r_shift = 8

    def decide(self, information):
        self.initialise(information)

        return self.move


strategy = Ideal("Ideal")


def decide(state):
    return strategy.decide(state)

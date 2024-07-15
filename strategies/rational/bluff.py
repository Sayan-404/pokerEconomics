from ..Strategy import Strategy


class Bluff(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)
        self.r_shift = 5
        self.risk = 1.5

    def decide(self, information):
        self.initialise(information)

        return self.move


strategy = Bluff("Bluff")


def decide(state):
    return strategy.decide(state)

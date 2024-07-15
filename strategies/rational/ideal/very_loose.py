from ...Strategy import Strategy


class ChildStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.r_shift = 1

    def decide(self, information):
        self.initialise(information)

        return self.move


strategy = ChildStrategy()


def decide(state):
    return strategy.decide(state)

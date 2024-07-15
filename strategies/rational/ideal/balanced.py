from ...Strategy import Strategy


class ChildStrategy(Strategy):
    def __init__(self):
        super().__init__()

    def decide(self, information):
        self.initialise(information)

        return self.move


strategy = ChildStrategy()


def decide(state):
    return strategy.decide(state)

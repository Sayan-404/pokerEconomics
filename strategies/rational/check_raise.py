# In a single round, if taking the first action, check first
# Only if it's known that opponent will call

from ..Strategy import Strategy


class CheckRaise(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)
        self.totalNumberOfOpponentActions = 0
        self.totalOpponentRaises = 0
        self.probabilityOpponentRaise = 0

    def decide(self, information):
        self.initialise(information, tightness=0)

        if self.signal is True:
            if self.round == 0:
                # Opponent played the first action
                if not self.roundFirstAction:
                    if self.callValue != 0:
                        self.calculateProbability(opponentRaise=True)
                        return self.prodigalMove

                    self.calculateProbability()

                    if self.probabilityOpponentRaise > 0.5:
                        return self.frugalMove

                    return self.prodigalMove

                # When player is the small blind and takes the first action
                if self.roundFirstAction:
                    if self.probabilityOpponentRaise > 0.5:
                        return self.frugalMove

                    return self.prodigalMove

            # When it is not pre-flop
            elif self.callValue > 0:
                self.calculateProbability(opponentRaise=True)

                if self.probabilityOpponentRaise > 0.5:
                    return self.frugalMove

                return self.prodigalMove
            else:
                if not self.roundFirstAction:
                    self.calculateProbability()
                    return self.prodigalMove

        if self.signal is None:
            return self.frugalMove

        return self.surrenderMove

    def calculateProbability(self, opponentRaise=False):
        if opponentRaise:
            self.totalOpponentRaises += 1

        self.totalNumberOfOpponentActions += 1

        self.probabilityOpponentRaise = self.totalOpponentRaises / \
            self.totalNumberOfOpponentActions


strategy = CheckRaise("CheckRaise")


def decide(state):
    return strategy.decide(state)

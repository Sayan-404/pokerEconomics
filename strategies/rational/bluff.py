# Bluff if opponent has a higher probability of calling

# TODO Implement roundFirstAction

from poker_metrics.utils import prodigalMove
from ..Strategy import Strategy


class Bluff(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)
        self.raised = 0
        self.opponentFavCalls = 0
        self.opponentTotalActions = 0
        self.probabilityOppCalls = 0

    def decide(self, information):
        self.initialise(information, 0)

        if self.signal is True:
            if self.callValue == 0:
                if self.raised:
                    self.calculateProbability(calls=True)

                self.calculateProbability()

            self.raised = True
            return self.prodigalMove

        if self.signal is None:
            if self.roundFirstAction:
                if self.probabilityOppCalls >= 0.55:
                    self.raised = 1
                    return self.prodigalMove
            elif self.callValue == 0:
                if self.raised:
                    self.calculateProbability(calls=True)

                self.calculateProbability()

                if self.probabilityOppCalls >= 0.55:
                    self.raised = 1
                    return self.prodigalMove

            self.calculateProbability()
            self.raised = 0
            return self.frugalMove

        if self.probabilityOppCalls >= 0.55:
            if self.raised:
                self.calculateProbability(calls=True)

            self.calculateProbability()

            # Raise aggressively to sway away the opponent
            # Theoretically, by changing their pot odds and changing their signal
            self.raised = 1
            return prodigalMove(information, betAmt=(self.betAmt + (0.2 * information["player"]["bankroll"])))

        self.raised = 0
        return self.surrenderMove

    def calculateProbability(self, calls=False):
        if calls:
            self.opponentFavCalls += 1
        self.opponentTotalActions += 1

        self.probabilityOppCalls = self.opponentFavCalls/self.opponentTotalActions


strategy = Bluff("Bluff")


def decide(state):
    return strategy.decide(state)

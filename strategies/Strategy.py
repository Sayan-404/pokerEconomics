from poker_metrics.utils import (
    frugalMove, privateValue, prodigalMove, ir)
from poker_metrics.simple_hand_potential import potential as potentialPrivateValue


class Strategy:
    def __init__(self, strategyName):
        self.strategy = strategyName

        self.holeCards = []
        self.communityCards = []
        self.round = -1
        self.callValue = -1
        self.playerBetAmt = -1
        self.pot = 0
        self.betAmt = 0
        self.roundFirstAction = None

        self.signal = None
        self.prodigalMove = None
        self.frugalMove = None
        self.surrenderMove = ("f", -1)

        self.ehs = None
        self.showdownOdds = None

    def initialise(self, information, tightness=0):
        """
            Takes the information state and initialises all the variables before making an action.
        """
        tightnessRanges = {
            -2: -0.5,
            -1: -0.25,
            0: 0,
            1: 0.25,
            2: 0.5
        }

        self.roundFirstAction = information["roundFirstAction"]

        self.callValue = information["call_value"]
        self.adjustedCallValue = (
            self.callValue * tightnessRanges[tightness]) + self.callValue

        if self.adjustedCallValue < 0:
            self.adjustedCallValue = 0

        self.playerBetAmt = information["player"]["betamt"]
        self.pot = information["pot"]

        self.betAmt = 10
        self.adjustedBetAmt = (
            (self.betAmt * tightnessRanges[tightness]) + self.betAmt) if self.callValue != 0 else self.betAmt

        self.holeCards = information["player"]["hand"]
        self.communityCards = information["community_cards"]

        self.round = information["round"]

        self.signal = self.signalFn(tightnessRanges[tightness])

        self.prodigalMove = prodigalMove(information, betAmt=self.betAmt)
        self.frugalMove = frugalMove(information)

    def decide(self, information):
        # This function should be `initialised` so that it can use class variables
        raise NotImplementedError(
            f"The decide function is not implemented by {self.strategy}")

    def signalFn(self, tightnessFactor):

        # For pre-flop
        if self.round == 0:
            incomeRate = ir(self.holeCards)
            incomeRate += ((-1)*tightnessFactor)*incomeRate

            return incomeRate

        # Signal on the flop
        if self.round == 1:
            pv = privateValue(self.holeCards, self.communityCards)
            potPV = potentialPrivateValue(self.holeCards, self.communityCards)

            # Calculating Effective hand strength' with thesis formula (6.4) on page 37
            self.ehs = pv + (1 - pv)*potPV[0] - pv*potPV[1]

            # Calculated with formula 6.7 on page 40 of thesis
            self.showdownOdds = (self.adjustedCallValue + (4*self.adjustedBetAmt)) / \
                (self.pot + self.adjustedCallValue + (8*self.adjustedBetAmt))

            positiveEhs = self.ehs + pv*potPV[1]

            return (self.ehs - self.showdownOdds), (positiveEhs - self.showdownOdds)

        # Signal on the turn
        if self.round == 2:
            pv = privateValue(self.holeCards, self.communityCards)
            potPV = potentialPrivateValue(self.holeCards, self.communityCards)

            # Calculating Effective hand strength' with thesis formula (6.4) on page 37
            self.ehs = pv + (1 - pv)*potPV[0] - pv*potPV[1]

            if (self.ehs == 1.0):
                print(self.ehs)
                print(pv)
                print(potPV)
                print()
                exit()

            # Calculated with formula 6.7 on page 40 of thesis
            self.showdownOdds = (self.adjustedCallValue + self.adjustedBetAmt) / \
                (self.pot + self.adjustedCallValue + (2*self.adjustedBetAmt))

            positiveEhs = self.ehs + pv*potPV[1]

            return (self.ehs - self.showdownOdds), (positiveEhs - self.showdownOdds)

        # Signal on the river
        if self.round == 3:
            pv = privateValue(self.holeCards, self.communityCards)
            pv += ((-1)*tightnessFactor)*pv

            return pv

    def __str__(self):
        return f"{self.strategy}"

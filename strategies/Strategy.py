from poker_metrics.chen import get_score
from poker_metrics.utils import (
    frugalMove, privateValue, prodigalMove, systemResponse)
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
            # Gets the score by Chen's formula
            score = get_score(self.holeCards) + (tightnessFactor*(-10))

            if self.callValue == 0:
                # 4 was found to be the average score of all hands
                # Rationale: A hand needs to be better than average
                if score > 4:
                    if score > 12:
                        return True

                    return None

            if self.callValue != 0:
                # If score greater than or equal to 12 then raise/re-raise
                # If score greater than or equal to 10 but less than 12 then call to raises
                if score > 10:
                    if score > 12:
                        return True

                return None

        if self.round == 1:
            # Signal on the flop
            pv = privateValue(self.holeCards, self.communityCards)
            potPV = potentialPrivateValue(self.holeCards, self.communityCards)

            ehs = pv + (1 - pv)*potPV[0] - pv*potPV[1]

            showdownOdds = (self.adjustedCallValue + (4*self.adjustedBetAmt)) / \
                (self.pot + self.adjustedCallValue + (8*self.adjustedBetAmt))

            if (ehs > showdownOdds):
                positiveEhs = ehs + pv*potPV[1]

                if (positiveEhs >= showdownOdds):
                    return True

                return None

        if self.round == 2:
            # Signal on the turn
            pv = privateValue(self.holeCards, self.communityCards)
            potPV = potentialPrivateValue(self.holeCards, self.communityCards)

            # Calculating Effective hand strength' with thesis formula (6.4) on page 37
            ehs = pv + (1 - pv)*potPV[0] - pv*potPV[1]

            # Calculated with formula 6.7 on page 40 of thesis
            showdownOdds = (self.adjustedCallValue + self.adjustedBetAmt) / \
                (self.pot + self.adjustedCallValue + (2*self.adjustedBetAmt))

            if (ehs > showdownOdds):
                positiveEhs = ehs + pv*potPV[1]

                if (positiveEhs >= showdownOdds):
                    return True

                return None

        if self.round == 3:
            # Signal on the river
            pv = privateValue(self.holeCards, self.communityCards)

            if (pv > (0.55 + tightnessFactor)):
                return True

            if ((pv > (0.3 + tightnessFactor)) and (pv < (0.55 + tightnessFactor))):
                return None

        return self.surrenderMove

    def __str__(self):
        return f"{self.strategy}"

from poker_metrics.chen import get_score
from poker_metrics.utils import (
    frugalMove, privateValue, prodigalMove, systemResponse)
from poker_metrics.simple_hand_potential import potential as potentialPrivateValue


class Strategy:
    def __init__(self, strategyName):
        self.strategy = strategyName
        self.environment = None
        self.privateValue = None

        # Potential private value is the probabilistic calculation of the chance events of getting a better hands
        # (or being in a better situation in future, game-theoretically speaking)
        self.potentialPrivateValue = 0

        # CostToRisk is the cost of playing a hand
        # CostToWinnings is the pot odds - the opportunity cost of a hand
        self.costToRisk = 0
        self.costToWinnings = 0

        self.holeCards = []
        self.communityCards = []
        self.round = -1
        self.callValue = -1
        self.playerBetAmt = -1
        self.pot = 0
        self.betAmt = 0
        self.rank_data = {}

        # Here the potential variables are probabilistic calculation of chance events
        self.potentialCostToRisk = 0
        self.potentialCostToWinnings = 0

        self.signal = None
        self.prodigalMove = None
        self.frugalMove = None
        self.surrenderMove = ("f", -1)

    def initialise(self, information, tightness):
        """
            Takes the information state and initialises all the variables before making an action.
        """

        self.callValue = information["call_value"]
        self.playerBetAmt = information["player"]["betamt"]
        self.pot = information["pot"]
        self.betAmt = 10

        self.holeCards = information["player"]["hand"]
        self.communityCards = information["community_cards"]
        self.round = information["round"]

        self.environment = systemResponse(information)

        if self.callValue != 0:
            # Here costToWinnings is the pot odds
            self.costToWinnings = self.callValue / (self.callValue + self.pot)

            # Here costToRisk is the amount a player is expected to lose if they make the call
            self.costToRisk = self.callValue / \
                (self.callValue + self.playerBetAmt)

            # Here potential cost to winnings is implied odds (Page 13 of thesis)
            # "hitting your hand means you very likely will win"
            # "and additionally your opponent is likely play to the showdown"
            # "If you hit you can expect to make an extra bet (from opponent)"
            self.potentialCostToWinnings = self.callValue / \
                ((self.callValue*2) + self.pot)

            # Here potential cost to risk is the amount a person is expected to loss if they hti
            self.potentialCostToRisk = self.betAmt / \
                (self.betAmt + self.playerBetAmt)
        else:
            # Here potential cost to winnings is implied odds (Page 13 of thesis)
            # Here it is modified to use bet instead of callValue
            self.potentialCostToWinnings = self.betAmt / \
                ((self.betAmt*2) + self.pot)

            # Here potential cost to risk is the amount a person is expected to loss if they hit
            # Is controversial cause it does not factor in other player's contribution
            self.potentialCostToRisk = self.betAmt / \
                (self.betAmt + self.playerBetAmt)

        self.signal = self.signalFn(tightness=tightness)

        self.prodigalMove = prodigalMove(information, betAmt=self.betAmt)
        self.frugalMove = frugalMove(information)

    def decide(self, information):
        # This function should be `initialised` so that it can use class variables
        raise NotImplementedError(
            f"The decide function is not implemented by {self.strategy}")

    def signalFn(self, tightness=2):
        tightnessUpperRanges = [0.02, 0.04, 0.06, 0.08, 0.1]
        tightnessFactor = tightnessUpperRanges[tightness]

        # For pre-flop
        if self.round == 0:
            # Gets the score by Chen's formula
            score = get_score(self.holeCards)

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

            showdownOdds = (self.callValue + 4*self.betAmt) / \
                (self.pot + self.callValue + 8*self.betAmt)

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
            showdownOdds = (self.callValue + (4 * self.betAmt)) / \
                (self.pot + self.callValue + (8*self.betAmt))

            if (ehs > showdownOdds):
                positiveEhs = ehs + pv*potPV[1]

                if (positiveEhs >= showdownOdds):
                    return True

                return None

        if self.round == 3:
            # Signal on the river
            pv = privateValue(self.holeCards, self.communityCards)

            if self.callValue != 0:
                if (pv > self.costToWinnings):
                    # Maximise the probable payout by making the pv almost equal to cost to winnings
                    # Formula mathematically calculated
                    # Profit maximisation and only suitable if strategy wants to defect
                    self.betAmt = (pv*(self.callValue + self.pot) -
                                   self.callValue)/(1 - 2*pv)

                    return True

                elif (self.costToWinnings - pv) <= tightnessFactor:
                    return None

            if self.callValue == 0:
                if (pv >= (self.potentialCostToWinnings + tightnessFactor)):
                    return True

                if (pv >= (self.potentialCostToWinnings - tightnessUpperRanges[4 - tightnessUpperRanges.index(tightnessFactor)])):
                    return None

        return self.surrenderMove

    def __str__(self):
        return f"{self.strategy}"

from .utils import privateValue, ir, potentialPrivateValue, systemResponse, prodigalMove, frugalMove


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

    # def signalFn(self, tightness=1):
    #     """
    #         Analyses the information and gives signal.\n
    #         Based on the logic given in page 12 of the thesis.\n
    #         Returns: True, False, None
    #     """

    #     # These values must be re-calculated statistically
    #     defectionMin = 0.3
    #     cooperationMin = 0.4

    #     if tightness == 0:
    #         defectionMin = 0.1
    #         cooperationMin = 0.2

    #     if tightness == 2:
    #         defectionMin = 0.5
    #         cooperationMin = 0.60

    #     # This is direct implementation of the logic of Page 12 of the thesis
    #     if self.potentialPrivateValue != 0:
    #         if self.potentialPrivateValue[0] >= self.costToWinnings:
    #             # Profitable scenario if one has the chance to beat at least defectionMin% of the hands
    #             if (self.privateValue >= defectionMin):
    #                 return True

    #             return None
    #         # Calculation based on NPOT to be added |>

    #     # If there's a chance of beating at least cooperationMin% of hands then cooperate
    #     if (self.privateValue >= cooperationMin):
    #         return None

    #     return False

    def signalFn(self, tightness=2):
        tightnessUpperRanges = [0.02, 0.04, 0.06, 0.08, 0.1]
        tightnessFactor = tightnessUpperRanges[tightness]

        if self.round == 0:
            # Signal on the pre-flop
            pv = privateValue(self.holeCards)
            incomeRate = ir(self.holeCards)
            irp = (incomeRate + 351)/1055

            # Big Blind's action if callValue is 0
            if self.callValue == 0:
                if irp >= pv:
                    if pv >= self.potentialCostToWinnings:
                        return True

                    return None

            if self.callValue != 0:
                # When it's small blind's action
                if self.callValue == self.playerBetAmt:
                    if irp >= pv:
                        if pv >= self.costToWinnings:
                            return True

                    return None
                else:
                    # If the prodigal factor is satisfied then defect
                    if pv >= (self.costToWinnings + tightnessFactor):
                        return True

                    if pv >= self.costToWinnings:
                        return None

        if self.round == 1:
            # Signal on the flop
            potentialPV = potentialPrivateValue(
                self.holeCards, self.communityCards, self.rank_data)
            self.rank_data = potentialPV[2]
            metric = 0

            if self.callValue != 0:
                metric = self.costToWinnings

            if self.callValue == 0:
                metric = self.potentialCostToWinnings

            if potentialPV[0] >= metric:
                if potentialPV[0] >= (metric + tightnessFactor):
                    return True

                return None

        if self.round == 2:
            # Signal on the turn
            pv = privateValue(self.holeCards, self.communityCards)
            potPV = potentialPrivateValue(self.holeCards, self.communityCards, self.rank_data)
            self.rank_data = potPV[2]
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

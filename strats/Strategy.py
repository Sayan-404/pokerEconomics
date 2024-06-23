from .utils import privateValue, potentialPrivateValue, systemResponse, prodigalMove, frugalMove


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

        callValue = information["call_value"]
        playerBetAmt = information["player"]["betamt"]
        pot = information["pot"]
        bet = 10

        self.holeCards = information["player"]["hand"]
        self.communityCards = information["community_cards"]
        self.round = information["round"]

        self.privateValue = privateValue(
            self.holeCards, self.communityCards)

        if self.communityCards:
            self.potentialPrivateValue = potentialPrivateValue(
                self.holeCards, self.communityCards)

        self.environment = systemResponse(information)

        self.prodigalMove = prodigalMove(information, betAmt=bet)
        self.frugalMove = frugalMove(information)

        if callValue != 0:
            # Here costToWinnings is the pot odds
            self.costToWinnings = callValue / (callValue + pot)

            # Here costToRisk is the amount a player is expected to lose if they make the call
            self.costToRisk = callValue / (callValue + playerBetAmt)

            # Here potential cost to winnings is implied odds (Page 13 of thesis)
            # "hitting your hand means you very likely will win"
            # "and additionally your opponent is likely play to the showdown"
            # "If you hit you can expect to make an extra bet (from opponent)"
            self.potentialCostToWinnings = callValue / ((callValue*2) + pot)

            # Here potential cost to risk is the amount a person is expected to loss if they hti
            self.potentialCostToRisk = bet / (bet + playerBetAmt)
        else:
            # Here potential cost to winnings is implied odds (Page 13 of thesis)
            # Here it is modified to use bet instead of callValue
            self.potentialCostToWinnings = bet / ((bet*2) + pot)

            # Here potential cost to risk is the amount a person is expected to loss if they hti
            self.potentialCostToRisk = bet / (bet + playerBetAmt)

        self.signal = self.signalFn(tightness=tightness)

    def decide(self, information):
        # This function should be `initialised` so that it can use class variables
        raise NotImplementedError(
            f"The decide function is not implemented by {self.strategy}")

    def signalFn(self, tightness=1):
        """
        Analyses the information and gives signal.\n
        Based on the logic given in page 12 of the thesis.\n
        Returns: True, False, None
        """

        # These values must be re-calculated statistically
        defectionMin = 0.3
        cooperationMin = 0.4

        if tightness == 0:
            defectionMin = 0.1
            cooperationMin = 0.2

        if tightness == 2:
            defectionMin = 0.5
            cooperationMin = 0.60

        # This is direct implementation of the logic of Page 12 of the thesis
        if self.potentialPrivateValue != 0:
            if self.potentialPrivateValue[0] >= self.costToWinnings:
                # Profitable scenario if one has the chance to beat at least defectionMin of the hands
                if (self.privateValue >= defectionMin):
                    return True

                return None

        # If there's a chance of beating at least 40% of hands then cooperate
        if (self.privateValue >= cooperationMin):
            return None

        return False

    def __str__(self):
        return f"{self.strategy}"

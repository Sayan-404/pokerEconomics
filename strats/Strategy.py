from .utils import privateValue, potentialPrivateValue, systemResponse, defectiveMove, cooperativeMove


class Strategy:
    def __init__(self, strategyName):
        self.strategy = strategyName
        self.environment = None
        self.privateValue = None
        self.potentialPrivateValue = None
        self.costToRisk = 0
        self.costToWinnings = 0
        self.potentialCostToRisk = 0
        self.potentialCostToWinnings = 0
        self.signal = None
        self.defectiveMove = None
        self.cooperativeMove = None
        self.surrenderMove = ("f", -1)

    def initialise(self, information):
        """
        Takes the information state and initialises all the variables before making an action.
        """

        callValue = information["call_value"]
        playerBetAmt = information["player"]["betamt"]
        pot = information["pot"]
        bet = 10

        self.privateValue = privateValue(
            information["player"]["hand"], information["community_cards"])
        self.potentialPrivateValue = potentialPrivateValue(
            information["player"]["hand"])

        self.environment = systemResponse(information)

        self.defectiveMove = defectiveMove(information, betAmt=bet)
        self.cooperativeMove = cooperativeMove(information)

        if callValue != 0:
            # Here costToWinnings is the pot odds
            self.costToWinnings = callValue / (callValue + pot)

            # Here costToRisk is the amount a player is expected to lose if they make the call
            self.costToRisk = callValue / (callValue + playerBetAmt)
        else:
            self.potentialCostToWinnings = bet / (bet + pot)
            self.potentialCostToRisk = bet / (bet + playerBetAmt)

        self.signal = self.signalFn()

    def decide(self, information):
        # This function should be `initialised` so that it can use class variables
        raise NotImplementedError(
            f"The decide function is not implemented by {self.strategy}")

    def signalFn(self):
        """
        Analyses the information and gives signal.\n
        Returns: True, False, None
        """

        noneCondition = (self.potentialCostToWinnings <=
                         self.potentialCostToRisk)

        if self.costToRisk is not None:
            noneCondition = (self.costToWinnings < self.costToRisk)

        # Final None Condition
        # noneCondition = ((self.potentialPrivateValue - self.costToWinnings)
        #                  > 0.10) and (self.costToWinnings < self.costToRisk)

        if ((self.privateValue - self.costToWinnings)) > 0.10:
            # Margin of positive 10 gap between the two metrics
            return True
        elif noneCondition:
            # Margin of positive 10 gap between the two metrics
            return None
        else:
            return False

    def __str__(self):
        return f"{self.strategy}"

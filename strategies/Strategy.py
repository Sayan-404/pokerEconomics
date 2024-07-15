from poker_metrics import frugalMove, privateValue, prodigalMove, ir, odds, potential

import math


class Strategy:
    def __init__(self, strategyName):
        """
            Initialises all the required variables for easy access by children classes.
        """
        self.strategy = strategyName

        self.information = {}

        self.holeCards = []
        self.communityCards = []

        # Initialised to -1 for distinction
        self.round = -1
        self.prevActionRound = -1
        self.callValue = -1

        # This is the total amount that the player has bet in a give hand (pre-flop to present round)
        self.playerBetAmt = -1

        self.pot = 0
        self.initialPot = 0     # Required for limiting pot

        # This is the additional amount that the player will bet/raise
        self.betAmt = 0

        # This variable is True if the current action is the round's first action
        self.roundFirstAction = None

        self.bigBlind = 0

        # Metrics for decision making and placing bets
        self.x_privateValue = -1  # x
        self.y_handEquity = -1    # y
        self.z_potOdds = -1       # z
        self.t_determiner = -1    # t
        self.range = ()         # A tuple containing the lower and upper limit of the range
        self.monetaryValue = -1  # monetary_range
        self.strength = -1      # x or y depending on the situation
        self.potShare = -1      # Share of pot of a specific player

        self.r_shift = 0
        self.l_shift = 0
        self.risk = 0

        self.move = ()

    def initialise(self, information):
        """
            Takes the information state and initialises all the variables before making an action.
        """

        self.information = information

        self.holeCards = information["player"]["hand"]
        self.communityCards = information["community_cards"]

        self.round = information["round"]
        self.bigBlind = information["blinds"]["bb"]["amt"]

        self.callValue = information["call_value"]

        self.playerBetAmt = information["player"]["betamt"]
        self.pot = information["pot"]

        self.setInitialPot()

        self.reason()
        self.setBet()
        self.limiter()
        self.setMove()

    def decide(self, information):
        # This function should be `initialised` so that it can use class variables
        raise NotImplementedError(
            f"The decide function is not implemented by {self.strategy}")

    def reason(self):
        self.x_privateValue = privateValue(self.holeCards, self.communityCards)

        try:
            if self.round == 0 or self.round == 3:
                self.strength = self.x_privateValue
            else:
                self.y_handEquity = potential(
                    self.holeCards, self.communityCards)[0]
                self.strength = self.y_handEquity
        except:
            raise Exception(
                f"{self.round} {self.holeCards} {self.communityCards}")

        self.z_potOdds = (self.callValue/(self.pot + self.callValue))
        self.t_determiner = self.strength - self.z_potOdds
        self.t2_determiner = (self.strength + self.risk) - self.z_potOdds

    def setBet(self):
        if self.t_determiner > 0:
            r = odds(self.z_potOdds, self.strength, self.x_privateValue,
                     self.risk, self.l_shift, self.r_shift)
            self.betAmt = self.toBlinds(math.floor((r*self.pot)/(1 - r)))
        elif self.t_determiner <= 0:
            if self.t2_determiner > 0:
                r = odds(self.z_potOdds, self.strength, self.x_privateValue,
                         self.risk, self.l_shift, self.r_shift)
                self.betAmt = self.toBlinds(math.floor((r*self.pot)/(1 - r)))
            else:
                if self.callValue == 0:
                    # Explicitly check
                    self.betAmt = -1
                else:
                    # Explicitly fold
                    self.betAmt = -2

    def setMove(self):
        if self.betAmt == -1:
            # raise Exception(f"Working -1")
            self.move = ("ch", -1)
        elif self.betAmt == -2:
            # raise Exception(f"Working -2")
            self.move = ("f", -1)
        elif self.betAmt == 0 or self.betAmt == self.callValue:
            # raise Exception(f"Working 0")
            self.move = frugalMove(self.information)
        elif self.betAmt > self.callValue:
            # raise Exception(f"Working pr")
            self.move = prodigalMove(
                self.information, betAmt=(self.betAmt - self.callValue))
        elif self.betAmt < self.callValue:
            # TODO This scenario should be handled by the odds function - modify
            self.move = ("f", -1)
        else:
            raise Exception(f"Invalid bet amount: {self.betAmt}")

    def setInitialPot(self):
        # Only applicable for heads-up
        if (self.round == 0) and (self.prevActionRound == -1):
            self.initialPot = self.pot

        elif self.prevActionRound < self.round:
            self.initialPot = self.pot - self.callValue

        self.prevActionRound = self.round

    def limiter(self):
        if (self.callValue + self.betAmt + self.playerBetAmt) >= (3*self.initialPot):
            if (self.playerBetAmt + self.callValue) == (3*self.initialPot):
                self.betAmt = 0
            elif (self.playerBetAmt + self.callValue) > (3*self.initialPot):
                if self.callValue == 0:
                    self.betAmt = -1
                else:
                    self.betAmt = -2
            elif (self.playerBetAmt + self.callValue) < (3*self.initialPot):
                excess = self.pot - (self.playerBetAmt + self.callValue)
                self.betAmt = self.toBlinds(excess)

    def toBlinds(self, amt):
        """
            Convert the monetary value to nearest big blind multiple.
        """
        return round(amt/self.bigBlind) * self.bigBlind

    def __str__(self):
        return f"{self.strategy}"

from poker_metrics import frugalMove, privateValue, prodigalMove, ir, odds, potential

import math


class Strategy:
    def __init__(self, strategyName):
        """
            Initialises all the required variables for easy access by children classes.
        """
        self.strategy = strategyName

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


    def initialise(self, information):
        """
            Takes the information state and initialises all the variables before making an action.
        """

        self.holeCards = information["player"]["hand"]
        self.communityCards = information["community_cards"]

        self.round = information["round"]
        self.bigBlind = information["blinds"]["bb"]["amt"]

        self.callValue = information["call_value"]

        self.playerBetAmt = information["player"]["betamt"]
        self.pot = information["pot"]

        self.setInitialPot()

        self.reason()

    def decide(self, information):
        # This function should be `initialised` so that it can use class variables
        raise NotImplementedError(
            f"The decide function is not implemented by {self.strategy}")

    def reason(self):
        self.x_privateValue = privateValue(self.holeCards, self.communityCards)

        if round in [0, 3]:
            self.strength = self.x_privateValue
        else:
            self.y_handEquity = potential(self.holeCards, self.communityCards)[0]
            self.strength = self.y_handEquity

        self.z_potOdds = (self.callValue/(self.pot + self.callValue))
        self.t_determiner = self.strength - self.z_potOdds

    def setBet(self):
        r = 0
        if self.round in [1, 2]:
            if self.z_potOdds < self.y_handEquity:
                r = odds(self.z_potOdds, self.y_handEquity, self.x_privateValue, self.risk, self.l_shift, self.r_shift)
                self.betAmt = self.toBlinds((r*self.pot)/(1 - r))


    def setInitialPot(self):
        # Only applicable for heads-up
        if (self.round == 0) and (self.prevActionRound == -1):
            self.initialPot = self.pot

        elif self.prevActionRound < self.round:
            self.initialPot = self.pot - self.callValue

        self.prevActionRound = self.round

    def toBlinds(self, amt):
        """
            Convert the monetary value to nearest big blind multiple.
        """
        return round(amt/self.bigBlind) * self.bigBlind

    def __str__(self):
        return f"{self.strategy}"

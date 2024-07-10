from poker_metrics.utils import frugalMove, privateValue, prodigalMove, ir
from poker_metrics.simple_hand_potential import potential

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
        self.callValue = -1

        # This is the total amount that the player has bet in a give hand (pre-flop to present round)
        self.playerBetAmt = -1

        self.pot = 0

        # This is the additional amount that the player will bet/raise
        self.betAmt = 0

        # This variable is True if the current action is the round's first action
        self.roundFirstAction = None

        self.signal = None

        # Metrics for decision making and placing bets
        self.x_privateValue = -1  # x
        self.y_handEquity = -1    # y
        self.z_potOdds = -1       # z
        self.t_determiner = -1    # t
        self.range = ()         # A tuple containing the lower and upper limit of the range
        self.monetaryRange = -1  # monetary_range
        self.strength = -1      # x or y depending on the situation
        self.potShare = -1      # Share of pot of a specific player

    def initialise(self, information):
        """
            Takes the information state and initialises all the variables before making an action.
        """

        self.roundFirstAction = information["roundFirstAction"]

        self.callValue = information["call_value"]

        self.playerBetAmt = information["player"]["betamt"]
        self.pot = information["pot"]

        self.betAmt = 10

        self.holeCards = information["player"]["hand"]
        self.communityCards = information["community_cards"]

        self.round = information["round"]

        self.reason()

    def decide(self, information):
        # This function should be `initialised` so that it can use class variables
        raise NotImplementedError(
            f"The decide function is not implemented by {self.strategy}")

    def reason(self):
        self.strength = -1

        self.x_privateValue = privateValue(self.holeCards, self.communityCards)

        if self.round in [0, 3]:
            self.strength = self.x_privateValue
        else:
            lookahead = 1 if self.round == 2 else 2
            self.y_handEquity = potential(
                self.holeCards, self.communityCards, lookahead)
            self.strength = self.y_handEquity[0]

        if self.callValue > 0:
            self.z_potOdds = (self.callValue/(self.pot + self.callValue))
            self.t_determiner = self.strength - self.z_potOdds
            self.range = (self.z_potOdds, self.strength)
        else:
            # When call value is 0 determine rationality with pot share
            self.z_potOdds = -1
            self.potShare = self.playerBetAmt/self.pot
            self.t_determiner = self.strength - self.potShare
            self.range = (0, self.strength)

    def __str__(self):
        return f"{self.strategy}"

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

    def initialise(self, information):
        """
            Takes the information state and initialises all the variables before making an action.
        """

        self.roundFirstAction = information["roundFirstAction"]

        self.callValue = information["call_value"]

        self.playerBetAmt = information["player"]["betamt"]
        self.pot = information["pot"]

        if self.roundFirstAction:
            if round == 0:
                self.initialPot = 3
            else:
                self.initialPot = self.pot
        else:
            self.initialPot = self.pot - self.callValue

        self.holeCards = information["player"]["hand"]
        self.communityCards = information["community_cards"]

        self.round = information["round"]
        self.bigBlind = information["blinds"]["bb"]["amt"]

        self.reason()
        self.setBet()

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

        self.z_potOdds = (self.callValue/(self.pot + self.callValue))
        self.t_determiner = self.strength - self.z_potOdds
        self.range = (self.z_potOdds, self.strength)


    def getOdds(self):
        l_shift_adjusted = (self.strength/3)*self.l_shift
        r_shift_adjusted = (self.strength/3)*self.r_shift

        try:
            if self.z_potOdds < self.strength:
                return odds(self.z_potOdds, self.strength, self.x_privateValue, l_shift_adjusted, r_shift_adjusted)
            else:
                return odds(self.strength, self.z_potOdds, self.x_privateValue, l_shift_adjusted, r_shift_adjusted)
        except:
            pass
            raise Exception(f"{self.round} {self.holeCards if self.holeCards else []} {self.communityCards if self.communityCards else []} {self.callValue} {self.z_potOdds} {self.strength} {self.x_privateValue} {l_shift_adjusted} {r_shift_adjusted}")

    def setBet(self):
        r = self.getOdds()
        bet = round(((r*self.pot)/(1-r))/self.bigBlind) * self.bigBlind

        if bet > (3*self.initialPot):
            if self.callValue == 0:
                self.betAmt = 0
            else:
                if (self.callValue + self.pot) == (3*self.initialPot):
                    self.betAmt = 0

                self.betAmt = round((3*self.initialPot)/self.bigBlind) * self.bigBlind

    def __str__(self):
        return f"{self.strategy}"

from poker_metrics import frugalMove, privateValue, prodigalMove, odds, potential

import math
import random


class Strategy:
    def __init__(self, strategyName):
        """
            Initialises all the required variables for easy access by children classes.
        """
        self.strategy = strategyName
        self.seed = None

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
        self.range = ()             # A tuple containing the lower and upper limit of the range
        self.monetaryValue = -1     # monetary_range
        self.strength = -1          # x or y depending on the situation
        self.potShare = -1          # Share of pot of a specific player

        self.r_shift = 0            # A number defining the "prodigalness" of a strategy
        self.l_shift = 0            # A number defining the "frugalness" of a strategy
        self.risk = 0               # A number defining the risk capacity of a strategy

        self.bluff = False          # If true then bluff

        self.move = ()

    def initialise(self, information):
        """
            Takes the information state and initialises all the variables before making an action.
        """

        self.information = information
        if information["seed"]:
            self.seed = round(information["seed"])

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

        # Bluff if true
        if self.bluff:
            self.bluffer()

        if self.round == 0 or self.round == 3:
            self.strength = self.x_privateValue
        else:
            self.y_handEquity = potential(
                self.holeCards, self.communityCards)[0]
            self.strength = self.y_handEquity

        self.z_potOdds = (self.callValue/(self.pot + self.callValue))
        self.t_determiner = self.strength - self.z_potOdds
        self.t2_determiner = (self.strength + self.risk) - self.z_potOdds

    def setBet(self):
        """Decides bet based on the mathematical logic"""

        if self.t2_determiner > 0:
            # When t' > 0 then strategy is in the money

            # Get odds from the odds function and then derive the bet amount
            # The odd is decided randomly from player's playing range

            r = odds(self.z_potOdds, self.strength, self.x_privateValue,
                     self.risk, self.l_shift, self.r_shift, seed=self.seed)
            self.betAmt = math.floor((r*self.pot)/(1 - r))

        elif self.t2_determiner <= 0:
            # When t' <= 0 then strategy is out of money

            if self.callValue == 0:
                # Explicitly check
                self.betAmt = -1

            else:
                # Explicitly fold
                self.betAmt = -2

    def setMove(self):
        """Sets an appropriate move based on bet amount"""

        if self.betAmt == -1:
            # Check when explicitly -1
            self.move = ("ch", -1)
        elif self.betAmt == -2:
            # Fold when explicitly -2
            self.move = ("f", -1)
        elif self.betAmt == 0 or self.betAmt == self.callValue:
            # Frugal move when bet amount is explicitly 0 or call value
            self.move = frugalMove(self.information)
        elif self.betAmt > self.callValue:
            # Prodigal move when bet amount is more than call value
            self.move = prodigalMove(
                self.information, betAmt=(self.betAmt - self.callValue))
        elif self.betAmt < self.callValue:
            # This scenario should not happen so raise an exception
            raise Exception("Bet amt can't be less")
        else:
            raise Exception(f"Invalid bet amount: {self.betAmt}")

    def setInitialPot(self):
        """Sets initial pot as round's first pot value"""

        # Only applicable for heads-up
        if (self.round == 0) and (self.prevActionRound == -1):
            self.initialPot = self.pot

        elif self.prevActionRound < self.round:
            self.initialPot = self.pot - self.callValue

        self.prevActionRound = self.round

    def limiter(self):
        """Limit the bet amount to 3 times initial pot"""

        if self.betAmt == -1 or self.betAmt == -2:
            # Ignore limit when explicitly check or fold
            pass
        else:
            return self.toBlinds(3*self.initialPot if self.betAmt > 3*self.initialPot else self.betAmt)

    def toBlinds(self, amt):
        """Convert the monetary value to nearest big blind multiple"""

        return round(amt/self.bigBlind) * self.bigBlind

    def bluffer(self):
        # Inverses a strategy's hand strength to turn weak hand to strong

        if self.x_privateValue < 0.55:
            if 1 == random.randint(0, 2):
                self.x_privateValue = 1 - self.x_privateValue

    def __str__(self):
        return f"{self.strategy}"

from poker_metrics import frugalMove, privateValue, prodigalMove, odds
from poker_metrics.potential.potential import potential

import random


class Strategy:
    def __init__(self):
        """
            Initialises all the required variables for easy access by children classes.
        """
        # If eval True then strategy is being used for automated data generation
        self.eval = False

        # Variables for initial limit
        self.iniLimit = False
        self.iniLimitMultiplier = 0

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
        self.bigBlind = 0

        # Metrics for decision making and placing bets
        self.hs = -1
        self.sp = -1
        self.po = -1
        self.t_determiner = -1
        self.effectivePotential = -1          # hs or sp depending on the situation

        # A number defining the "prodigalness" of a strategy
        self.r_shift = 0

        # A number defining the "frugalness" of a strategy
        self.l_shift = 0

        # A number defining the risk capacity of a strategy
        self.risk = 0

        self.bluff = 0                    # If true then bluff

        self.move = ()

        self.limit = 100000

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

        if self.iniLimit:
            if self.round == 0:
                self.limit = self.iniLimitMultiplier*self.initialPot
            else:
                self.limit = 100000

        self.reason()
        self.setBet()
        self.limiter()
        self.toBlinds()
        self.setMove()

        if (self.betAmt > self.limit):
            raise Exception(f"{self.betAmt} {self.initialPot}")

        self.prevActionRound = self.round

    def decide(self, information):
        # This function should be `initialised` so that it can use class variables
        if self.eval:
            if information == {}:
                pass
            else:
                self.initialise(information)
                return self.move
        else:
            raise NotImplementedError(
                f"The decide function is not implemented by {self.strategy}")

    def reason(self):
        self.hs = privateValue(self.holeCards, self.communityCards)

        # Bluff if true
        if self.bluff > 0:
            self.bluffer()

        self.sp = potential(self.holeCards, self.communityCards) if self.round in [1, 2] else 0
        self.effectivePotential = self.hs if self.round in [0, 3] else self.sp

        self.po = (self.callValue/(self.pot + self.callValue))

        self.ll = self.po/(1 - self.po)
        # If strength is 1 then instead of collapsing, return the strength
        # self.ul2 = (self.effectivePotential/(1 - self.effectivePotential)) + \
        #     self.risk if self.effectivePotential != 1 else self.effectivePotential
        self.ul2 = self.sp + self.hs

        self.t_determiner = self.ul2 - self.ll

    def setBet(self):
        """Decides bet based on the mathematical logic"""

        if self.t_determiner > 0:
            # When t' > 0 then strategy is in the money

            # Get odds from the odds function and then derive the bet amount
            # The odd is decided randomly from player's playing range

            self.r = odds(self.ll, self.ul2, self.hs, self.risk,
                          self.l_shift, self.r_shift, self.seed)

            self.monValue = round(self.pot*self.r)
            self.betAmt = self.monValue

        elif self.t_determiner == 0:
            # When t' == 0 then strategy is in balanced position
            # Only Call/Check (return 0 as bet amount)
            self.betAmt = 0

        elif self.t_determiner <= 0:
            # When t' <= 0 then strategy is out of money
            # Explicitly check/fold (return -1 as bet amount)
            self.betAmt = -1

    def setMove(self):
        """Sets an appropriate move based on bet amount"""

        if self.betAmt == -1:
            # Check/Fold when explicitly -1
            if self.callValue == 0:
                self.move = ("ch", -1)
            else:
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
            raise Exception(
                f"Bet amount can't be less: {self.betAmt} >! {self.callValue}")

        else:
            raise Exception(f"Invalid bet amount: {self.betAmt}")

    def setInitialPot(self):
        """Sets initial pot as round's first pot value"""

        # Only applicable for heads-up
        if (self.round == 0) and ((self.prevActionRound != 0)):
            initialPot = self.bigBlind + (self.bigBlind/2)
            self.initialPot = round(initialPot/self.bigBlind) * self.bigBlind

        elif self.prevActionRound < self.round:
            initialPot = (self.pot - self.callValue)

            # Converting to blinds
            self.initialPot = round(initialPot/self.bigBlind) * self.bigBlind

    def limiter(self):
        """Limit the bet amount to 3 times initial pot"""

        if self.betAmt in [-1, 0]:
            # Ignore limit when explicitly check or fold
            pass
        else:
            tcb = self.betAmt + self.playerBetAmt

            if tcb > self.limit:
                req = self.callValue + self.playerBetAmt

                if req > self.limit:
                    # Limit passed
                    # Forcefully call
                    self.betAmt = 0

                else:
                    self.betAmt = self.limit - self.playerBetAmt

    def toBlinds(self, amt=-1):
        """Convert the monetary value to nearest big blind multiple"""
        if self.betAmt in [-1, 0]:
            # Explicitly check/fold or call scenario
            pass
        else:
            bet = self.betAmt - self.callValue
            bet = round(bet/self.bigBlind) * self.bigBlind
            self.betAmt = bet + self.callValue

    def bluffer(self):
        # Inverses a strategy's hand strength to turn weak hand to strong

        if self.hs < 0.55:
            if 1 == random.randint(1, self.bluff):
                self.hs = 1 - self.hs

    def __str__(self):
        return f"{self.strategy}"

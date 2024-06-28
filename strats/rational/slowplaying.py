# Plays a strong hand weakly to suck people in for later bets and then raises
from ..Strategy import Strategy


class SlowPlaying(Strategy):
    def __init__(self, strategyName):
        super().__init__(strategyName)
        self.weakHandRound = -1

    def decide(self, information):
        self.initialise(information, 2)

        # Initialises the weakHandRound memory for each hand
        if self.round == 0:
            self.weakHandRound = -1

        if (self.signal is True):
            # If weak hand round is -1 then initialise the weak hand round for recall and frugal move
            # Frugal move if it is in the same round
            if (self.weakHandRound == -1) or (self.round == self.weakHandRound):
                self.weakHandRound = self.round
                return self.frugalMove
            # If weak hand round previously occurred then defect if the signal is still true
            elif self.weakHandRound < self.round:
                return self.prodigalMove

        if (self.signal is None):
            return self.frugalMove

        return self.surrenderMove

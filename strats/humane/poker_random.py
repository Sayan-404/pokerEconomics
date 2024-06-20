# Based on the changing style strategy
# Changes playing style randomly if there's a profitable environment

from Strategy import Strategy


class PokerRandom(Strategy):
    def __init__(self):
        super().__init__("poker_random")

import random
import time

from components.Card import Card


class Deck:
    def __init__(self, seed=None):
        self.cards = []
        self.create_deck()
        self.seed = seed
        if not seed:
            self.seed = time.time()
        random.seed(self.seed)

    def flush(self):
        """
        Reshuffles and create a new deck.
        """
        self.create_deck()
        self.shuffle()

    def create_deck(self):
        """
        Create a new deck.
        """
        suits = ["h", "d", "c", "s"]
        ranks = ["2", "3", "4", "5", "6", "7",
                 "8", "9", "T", "J", "Q", "K", "A"]
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        """
        Shuffle all the cards in a deck.
        """
        random.shuffle(self.cards)

    def deal_card(self):
        """
        Deal a card.
        """
        return self.cards.pop()

    def __str__(self):
        return f"{self.cards}"

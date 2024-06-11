# Utilities for testing

import sys
import os

sys.path.append(os.getcwd())

from Game import Game
from Logger import Logger

from strats.utils import cooperativeMove


# Mock classes
class MockPlayer:
    def __init__(self, id, bankroll, hand, strategy_name="", strategy=None):
        self.id = id
        self.hand = hand
        self.bankroll = bankroll
        self.betamt = 0
        self.ingame = 1
        self.decide = strategy
        self.strategy_name = strategy_name

    def package_state(self):
        """
        Returns the required information regarding a single player.
        """

        return {
            "id": self.id,
            "hand": [card.to_dict() for card in self.hand],
            "bankroll": self.bankroll,
            "betamt": self.betamt,
            "ingame": self.ingame,
            "strategy": self.strategy_name,
        }

    def flush(self):
        """
        Resets a player's variables (hand, ingame and betamt).
        """

        self.hand = []
        self.ingame = 1
        self.betamt = 0

    def receive_card(self, card):
        """
        Receives card but does not do anything.
        """
        pass

    def bet(self, amt):
        """
        Bet function, updates the total bet amount for the round and the bankroll.
        Returns the amount if successful, else returns False for invalid bet amount.
        """

        # Error checking so that bankroll does not go negative
        if amt > self.bankroll:
            return False

        self.bankroll -= amt
        self.betamt += amt

        return amt

    def __str__(self):
        return f"{self.id}: {self.hand} {self.bankroll}"


class MockCard:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def to_dict(self):
        return {"rank": self.rank, "suit": self.suit}

    def __str__(self):
        return f"{self.rank}{self.suit}"


def test_scenario(players, logger, community_cards, expect="", number_of_hands=100000):
    """
    ### Tests a specific scenario.\n\n

    `players`: List of mock players with pre-defined hands.
    `logger`: The logger object.
    `community_cards`: The list of mock cards that deck will have.
    `expect`: A list of dictionary of expected values.
    `number_of_hands`: Number of hands to run. Default - 100000.
    """

    class MockDeck:
        def __init__(self, seed):
            # Minimum of 5 cards are required
            self.cards = community_cards
            self.playerCards = [players[0].hand + players[1].hand]
            self.seed = seed
            self.create_deck()

        def flush(self):
            """
            Does not reshuffle and and make a new deck.
            """
            pass

        def create_deck(self):
            """
            Dose not create a new deck.
            """
            pass

        def shuffle(self):
            """
            Does not shuffle all the cards in a deck.
            """
            pass

        def deal_card(self):
            """
            Deal a card.
            """
            if self.playerCards:
                return self.playerCards.pop()

            return self.cards.pop()

        def __str__(self):
            return f"{self.cards}"

    gameObj = Game(players, logger, deck=MockDeck, number_of_hands=number_of_hands)

    data = []

    for i in range(number_of_hands):
        if not gameObj.sub_play(i):
            break
        else:
            data.append(gameObj.internal_data())

    for i in range(len(data)):
        roundData = data[i]
        expectData = expect[i]

        for key, value in roundData:
            if key in expectData.keys():
                assert expectData[key] == value


def decideCooperate(state):
    return cooperativeMove(state)

class Player:
    def __init__(self, id, bankroll, strategy_name="", strategy=None):
        self.id = id
        self.hand = []
        self.bankroll = bankroll
        self.betamt = 0
        self.ingame = 1
        self.decide = strategy # this points to the decide function in every strategy file, this function has the signature decide(state)
        self.strategy_name = strategy_name  
        # it takes the state and returns two values: move, bet
        # moves could be: c, ch, b, r, f
        # b and r are accompanied with a non-negative bet value
        # others return -1 as bet

    def package_state(self):
        return {
            "id": self.id,
            "hand": self.hand,
            "bankroll": self.bankroll,
            "betamt": self.betamt,
            "ingame": self.ingame,
            "strategy": self.strategy_name
        }

    def to_dict(self):
        return {
            "id": self.id,
            "hand": self.hand,
            "bankroll": self.bankroll,
            "betamt": self.betamt,
            "ingame": self.ingame,
        }

    def flush(self):
        self.hand = []
        self.ingame = 1
        self.betamt = 0

    def receive_card(self, card):
        self.hand.append(str(card))

    def bet(self, amt):
        self.bankroll -= amt
        self.betamt += amt
        return amt

    def __str__(self):
        return f"{self.id}: {self.hand} {self.bankroll}"

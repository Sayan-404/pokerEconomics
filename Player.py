class Player:
    def __init__(self, id, bankroll, strategy_name="", strategy=None):
        self.id = id
        self.hand = []
        self.bankroll = bankroll
        self.betamt = 0
        self.ingame = 1
        self.decide = strategy  # this points to the decide function in every strategy file, this function has the signature decide(state)
        self.strategy_name = strategy_name
        # it takes the state and returns two values: move, bet
        # moves could be: c, ch, b, r, f
        # b and r are accompanied with a non-negative bet value
        # others return -1 as bet

    def package_state(self):
        """
        Returns the required information regarding a single player.
        """

        return {
            "id": self.id,
            "hand": self.hand,
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
        Appends a single card to the player's hand. Raises an exception if duplicates are present.
        """
        if card in self.hand:
            raise ValueError("Hand contains duplicate cards.")

        self.hand.append(str(card))

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

    def to_dict(
        self,
        include_vars=["id", "hand", "betamt", "ingame", "bankroll", "strategy_name"],
    ):
        """
        Returns a dictionary representation of the Player object with selected variables.

        Args:
            include_vars (list, optional): A list of variable names to include in the dictionary.
                Defaults to ["id", "bankroll", "strategy_name"].

        Returns:
            dict: A dictionary containing the selected player attributes.
        """
        return {var: getattr(self, var) for var in include_vars}

class Player:
    def __init__(self, name, bankroll):
        self.name = name
        self.hand = []
        self.bankroll = bankroll
        self.betamt=0
        self.ingame=1
    def flush(self):
        self.hand = []
        self.ingame=1
        self.betamt=0
        
    def receive_card(self, card):
        self.hand.append(str(card))
    
    def bet(self, amt):
        self.bankroll -= amt
        self.betamt+=amt
        return amt
        
    def __str__(self):
        return f'{self.name}: {self.hand} {self.bankroll}'

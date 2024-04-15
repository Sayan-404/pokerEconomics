class Player:
    def __init__(self, name, bankroll):
        self.name = name
        self.hand = []
        self.bankroll = bankroll

    def receive_card(self, card):
        self.hand.append(card)
    
    def bet(self,unit):
        self.bankroll -= unit
        return unit
    
    def __str__(self):
        return f'{self.name}: {self.hand} {self.bankroll}'

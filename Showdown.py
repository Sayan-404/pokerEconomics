from Player import Player
from phevaluator.evaluator import evaluate_cards

class Showdown:
    def __init__(self, player1, player2, communitycards):
        # self.player1=player1
        # self.player2=player2
        self.handP1=[]
        self.handP2=[]
        for i in range(2):
            self.handP1.append(player1.hand[i].strval())
            self.handP2.append(player2.hand[i].strval())
        self.communitycards=communitycards

    def p1rank(self):
        self.handP1 = self.handP1 + self.communitycards
        p1 = evaluate_cards(*self.handP1)
        print(f"rank: {p1}")
        return p1
    
    def p2rank(self):
        self.handP2 = self.handP2 + self.communitycards
        p2 = evaluate_cards(*self.handP2)
        print(f"rank: {p2}")
        return p2
    
    def winner(self):   
        if self.p1rank() < self.p2rank():
            return 0
        else:
            return 1
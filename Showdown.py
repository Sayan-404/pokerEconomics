from phevaluator.evaluator import evaluate_cards

class Showdown:
    def __init__(self, community_cards, *players):
        self.player_hands = {
        }
        for i in range(len(players)):
            self.player_hands[f'player{i}'] = players[i].hand
        self.community_cards = community_cards

    def rank(self, player_number):
        hand = self.player_hands[f'player{player_number}'] + self.community_cards
        r = evaluate_cards(*hand)
        print(f"rank: {r}")
        return r
    
    def winner(self): # returns index of winning player, 0-indexed
        flag = 0
        for i in range(len(self.player_hands) - 1):
            if self.rank(i) < self.rank(i+1):
                flag = i
            else:
                flag = i+1
        return flag
    
    def __str__(self):
        return f'{self.player_hands} {self.community_cards}'
from phevaluator.evaluator import evaluate_cards

class Showdown:
    def __init__(self, community_cards, players):
        self.player_hands = {
        }
        self.players = players
        for i in range(len(players)):
            if players[i].ingame == 1:
                self.player_hands[f'player{i}'] = players[i].hand
        self.community_cards = community_cards

    def rank(self, player_number):
        hand = self.player_hands[f'player{player_number}'] + self.community_cards
        r = evaluate_cards(*hand)
        return r
    
    def get_next_player(self, i):
        for j in range(i+1, len(self.players)):
            if self.players[j].ingame:
                return j

    def winner(self): # returns index of winning player, 0-indexed
        flag = 0
        for i in range(len(self.player_hands) - 1):
            if self.rank(i) < self.rank(self.get_next_player(i)):
                flag = i
            else:
                flag = i + 1
        return flag
    
    def __str__(self):
        return f'{self.player_hands} {self.community_cards}'
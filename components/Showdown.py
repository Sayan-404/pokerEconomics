from hand_evaluator.evaluate_cards import evaluate_cards


class Showdown:
    def __init__(self, community_cards, players):
        self.player_hands = []
        self.players = players
        for i in range(len(players)):
            if players[i].ingame == 1:
                self.player_hands.append(players[i])
        self.community_cards = community_cards

    def rank(self, player):
        hand = player.hand + self.community_cards
        r = evaluate_cards(*hand)
        return r

    def winner(self):  # returns index of winning player, 0-indexed
        max_rank = 999999
        max_index = 0
        for i in range(len(self.player_hands)):
            if self.rank(self.player_hands[i]) < max_rank:
                max_rank = self.rank(self.player_hands[i])
                max_index = i
        return max_index

    def __str__(self):
        return f'{self.player_hands} {self.community_cards}'

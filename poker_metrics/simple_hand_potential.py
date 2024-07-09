import os
import sys
from itertools import combinations

sys.path.append(os.getcwd())
from hand_evaluator.evaluate_cards import evaluate_cards

# from phevaluator.evaluator import evaluate_cards

def potential(deck, hole_cards, community_cards, type_lookahead = 1):
    # 1 type_lookahead is 1 card look ahead
    # 2 type_lookahead is 2 card look ahead only applicable for flop
    # this function should only be used post flop
    
    current_hand = hole_cards + community_cards
    current_rank = evaluate_cards(*current_hand)
    ahead = 0
    inconsequential = 0
    possible_combinations = list(combinations(deck, type_lookahead))
    for cards in possible_combinations:
        full_hand = hole_cards + community_cards + list(cards)
        rank = evaluate_cards(*full_hand)
        if rank < current_rank:
            ahead += 1
        elif rank == current_rank:
            inconsequential += 1
    total = ahead + inconsequential
    return ahead/total, inconsequential/total


if __name__ == "__main__":
    rank = "23456789TJQKA"
    suit = "csdh"
    deck = [r+s for r in rank for s in suit]
    comm_cards = ["As", "Ad", "Ac"]
    hole = ["9s", "9c"]
    hand = hole + comm_cards
    _deck = [card for card in deck if card not in hand]
    # print(_deck)
    print(potential(_deck, hole, comm_cards, 2))

import os
import sys
from itertools import combinations

sys.path.append(os.getcwd())
from poker_metrics.utils import get_rank_category

def potential(hole_cards, community_cards, type_lookahead = 1):
    # 1 type_lookahead is 1 card look ahead
    # 2 type_lookahead is 2 card look ahead only applicable for flop
    # this function should only be used post flop
    rank = "23456789TJQKA"
    suit = "csdh"
    deck = [r+s for r in rank for s in suit]

    hole_cards = list(hole_cards)
    community_cards = list(community_cards)
    hand = hole_cards + community_cards

    deck = [card for card in deck if card not in hand]

    current_rank_category = get_rank_category(hand)[0]
    ahead = 0
    inconsequential = 0
    possible_combinations = list(combinations(deck, type_lookahead))
    for cards in possible_combinations:
        full_hand = hole_cards + community_cards + list(cards)
        future_rank_category = get_rank_category(full_hand)[0]
        if future_rank_category < current_rank_category:
            ahead += 1
        elif future_rank_category == current_rank_category:
            inconsequential += 1
    total = ahead + inconsequential
    return ahead/total, inconsequential/total

# from outs import *

# def potential(hole, board, type_lookahead=1):
#     outs = 0
#     _pair = pair(hole,board)
#     _twopair = twopair(hole,board)
#     _trips = trips(hole,board)
#     _boat = boat(hole,board)
#     _quads = quads(hole,board)
#     _straight = straight(hole+board)
#     _flush = flush(hole+board) 
#     if _pair == 1:
#         outs+= _twopair if (_twopair!=1) else 0
#         outs += _trips if (_trips!=1) else 0
#         outs += _boat if (_boat!=1) else 0
#         outs += _quads if (_quads!=1) else 0
#     else:
#         outs += _pair

#     outs += _straight if _straight!=1 else 0
#     outs += _flush if _flush!=1 else 0

#     return outs, 1-outs

# from poker_metrics.potential.potential import potential as pot

# def potential(hole, board, lookahead=1):
#     return pot(hole, board), 0.00

if __name__ == "__main__":
    hole=['2d', '3c']

    board = ['3h', '9d', 'Qh']


    print(potential(hole, board, 2))
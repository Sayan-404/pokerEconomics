from phevaluator.evaluator import evaluate_cards
import numpy as np
from itertools import combinations
from .rank import rank

def potential(hole_cards, community_cards, rank_data):
    community_cards = set(community_cards)
    if len(community_cards) < 3 | len(community_cards) == 5:
        return -1 # only plausible for flop, and turn
    hole_cards = set(hole_cards)
    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = set([r+s for r in ranks for s in suits])
    deck = deck - hole_cards
    deck = deck - community_cards
    opp_cards = list(combinations(deck, 2))
    w = {card: 1/len(opp_cards) for card in opp_cards}
    hp = np.zeros((3, 3))
    hp_total = np.zeros(3)
    t = hole_cards | community_cards
    current_rank5, rank_data = rank(*t, rank_data=rank_data)
    ahead, tied, behind = 0, 1, 2
    for opp_hole_cards in opp_cards:
        t = set(opp_hole_cards) | community_cards
        opp_rank, rank_data = rank(*t, rank_data=rank_data)

        if current_rank5 > opp_rank:
            index = ahead
        elif current_rank5 == opp_rank:
            index = tied
        else:
            index = behind
        future_community_cards = deck - set(opp_hole_cards)
        future_community_cards = list(combinations(future_community_cards, 1)) # only implements one card look-ahead
        for future_cards in future_community_cards:

            hp_total[index] += w[opp_hole_cards]

            future_board = community_cards | set(future_cards)
            t = hole_cards | future_board
            current_rank6, rank_data = rank(*t, rank_data=rank_data)

            t = set(opp_hole_cards) | future_board
            opp_rank, rank_data = rank(*t, rank_data=rank_data)

            if current_rank6 > opp_rank:
                hp[index][ahead] += w[opp_hole_cards]
            elif current_rank6 == opp_rank:
                hp[index][tied] += w[opp_hole_cards]
            else:
                hp[index][behind] += w[opp_hole_cards]
    ppot1 = (hp[behind][ahead] + hp[behind][tied]/2 + hp[tied][ahead]/2) / (hp_total[behind] + hp_total[tied]/2)
    npot1 = (hp[ahead][behind] + hp[ahead][tied]/2 + hp[tied][behind]/2) / (hp_total[ahead] + hp_total[tied]/2)
    return ppot1, npot1, rank_data
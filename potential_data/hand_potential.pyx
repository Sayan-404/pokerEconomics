# potential.pyx

from rank import rank
import numpy as np
from itertools import combinations
cimport cython
from libc.math cimport ceil

@cython.boundscheck(False)
@cython.wraparound(False)
def potential(deck, hole_cards, community_cards):
    cdef int len_community = len(community_cards)
    if len_community < 3 or len_community == 5:
        return -1  # only plausible for flop, and turn

    cdef list opp_cards = list(combinations(deck, 2))
    cdef dict w = {card: 1 / len(opp_cards) for card in opp_cards}

    hp = np.zeros((3, 3), dtype=np.float64)
    hp_total = np.zeros(3, dtype=np.float64)
    cdef dict rank_data = {}
    cdef list t = [*hole_cards, *community_cards]
    cdef int current_rank5
    current_rank5, rank_data = rank(*t, rank_data=rank_data)
    
    cdef int ahead = 0
    cdef int tied = 1
    cdef int behind = 2
    cdef int index
    cdef list future_community_cards
    cdef list future_board
    cdef int current_rank6, opp_rank

    for opp_hole_cards in opp_cards:
        t = [*opp_hole_cards, *community_cards]
        opp_rank, rank_data = rank(*t, rank_data=rank_data)

        if current_rank5 > opp_rank:
            index = ahead
        elif current_rank5 == opp_rank:
            index = tied
        else:
            index = behind
        future_community_cards = [card for card in deck if card not in opp_hole_cards]
        future_community_cards = list(combinations(future_community_cards, 1))  # only implements one card look-ahead

        for future_cards in future_community_cards:
            hp_total[index] += w[opp_hole_cards]

            future_board = [*future_cards, *community_cards]
            t = [*hole_cards, *future_board]
            current_rank6, rank_data = rank(*t, rank_data=rank_data)

            t = [*opp_hole_cards, *future_board]
            opp_rank, rank_data = rank(*t, rank_data=rank_data)

            if current_rank6 > opp_rank:
                hp[index][ahead] += w[opp_hole_cards]
            elif current_rank6 == opp_rank:
                hp[index][tied] += w[opp_hole_cards]
            else:
                hp[index][behind] += w[opp_hole_cards]
    
    cdef double ppot1 = (hp[behind][ahead] + hp[behind][tied] / 2 + hp[tied][ahead] / 2) / (hp_total[behind] + hp_total[tied] / 2)
    cdef double npot1 = (hp[ahead][behind] + hp[ahead][tied] / 2 + hp[tied][behind] / 2) / (hp_total[ahead] + hp_total[tied] / 2)
    return ppot1, npot1, rank_data

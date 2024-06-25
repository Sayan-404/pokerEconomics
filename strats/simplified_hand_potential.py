from itertools import combinations
from phevaluator.evaluator import evaluate_cards

def potential(deck, hole_cards, community_cards, type_lookahead=1):
    # 1 type_lookahead is 1 card look ahead
    # 2 type_lookahead is 2 card look ahead only applicable for flop
    # this function should only be used post flop
    
    current_hand = hole_cards + community_cards
    current_rank = evaluate_cards(*current_hand)
    ahead = 0
    behind = 0
    possible_combinations = list(combinations(deck, type_lookahead))
    for cards in possible_combinations:
        full_hand = hole_cards + community_cards + cards
        rank = evaluate_cards(*full_hand)
        if rank >= current_rank:
            ahead += 1
        else:
            behind += 1
    total = ahead + behind
    return ahead/total, behind/total
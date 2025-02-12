import os
import sys

sys.path.append(os.getcwd())

def get_score(cards):
    from hand_evaluator.evaluate_cards import evaluate_cards
    from poker_metrics.math_utils import inverse_range, scale

    score = evaluate_cards(*cards)
    if len(cards) == 5:
        score = inverse_range(score, 1, 7462)
        score = scale(score, 1, 7462)
    elif len(cards) == 6:
        score = inverse_range(score, 1, 7450)
        score = scale(score, 1, 7450)
    elif len(cards) == 7:
        score = inverse_range(score, 1, 7414)
        score = scale(score, 1, 7414)
    return score


if __name__ == "__main__":
    from tqdm import tqdm
    from itertools import combinations
    from poker_metrics.math_utils import kde_plot

    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = [r+s for r in ranks for s in suits]
    cards = list(combinations(deck, 5))
    scores = []
    for j in tqdm(range(len(cards))):
        scores.append((cards[j], get_score(cards[j])))
    one_d_scores = [score[1] for score in scores]
    kde_plot(one_d_scores)
    print(f"max: {max(one_d_scores)} min: {min(one_d_scores)}")
    # 5 cards: 1 to 7462
    # 6 cards: 1 to 7450
    # 7 cards: 1 to 7414

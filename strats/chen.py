import pickle
import math
import statistics

from tqdm import tqdm
from .math_utils import scale, kde_plot
from itertools import combinations
# IMPORTANT: the score in chen are not uniformly distributed, ie pairs of cards are not equally distributed for each given score range
# therefore a mean understanding does not suffice and a mode understanding is necessary
# run this file to see a distribution and infer strategies

SCORES = []


def get_score(cards):
    if len(cards) != 2:
        raise ValueError("Number of cards have to be 2.")
    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    rank_scores = {str(i): i/2 for i in range(2, 10)}
    rank_scores.update({
        "T": 5,
        "J": 6,
        "Q": 7,
        "K": 8,
        "A": 10
    })
    card_ranks = [card[0] for card in cards]
    card_suits = [card[1] for card in cards]

    def card_rank_value(rank):
        return ranks[rank]
    sorted_card_ranks = sorted(card_ranks, key=card_rank_value, reverse=True)

    score = rank_scores[sorted_card_ranks[0]]
    # pair
    if len(set(sorted_card_ranks)) == 1:
        score = max(5, score*2)

    # suited
    if len(set(card_suits)) == 1:
        score += 2

    # gap
    gap = ranks[sorted_card_ranks[0]] - ranks[sorted_card_ranks[1]] - 1
    if gap == 1:
        score -= 1
    elif gap == 2:
        score -= 2
    elif gap == 3:
        score -= 4
    elif gap >= 4:
        score -= 5

    # adjust gap score
    if ranks[sorted_card_ranks[0]] < 12 and len(set(sorted_card_ranks)) != 1:
        if gap == 0 or gap == 1:
            score += 1

    score = math.ceil(score)
    return score


def generateCache():
    global SCORES

    if not SCORES:
        ranks = "23456789TJQKA"
        suits = "scdh"
        deck = [r+s for r in ranks for s in suits]
        hole_cards = sorted(list(combinations(deck, 2)))

        SCORES = [[sorted(cards), get_score(cards)] for cards in hole_cards]

        with open("./strats/chenCache.bin", "wb") as f:
            pickle.dump(SCORES, f)

        # print("Cache generated and saved to chenCache.bin")


def chenScore(cards):
    global SCORES

    if not SCORES:
        try:
            with open("./strats/chenCache.bin", "rb") as f:
                SCORES = pickle.load(f)
        except FileNotFoundError:
            generateCache()

    cards = sorted(cards)

    for i in range(len(SCORES)):
        if (SCORES[i][0][0] == cards[0]) and (SCORES[i][0][1] == cards[1]):
            return SCORES[i][1]


if __name__ == "__main__":
    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = [r+s for r in ranks for s in suits]
    hole_cards = list(combinations(deck, 2))
    scores = []
    for i in tqdm(range(len(hole_cards))):
        scores.append((hole_cards[i], get_score(hole_cards[i])))
    one_d_scores = [score[1] for score in scores]
    print(f"max: {max(one_d_scores)} min: {min(one_d_scores)}")

    print("Mean: ", statistics.mean(sorted(one_d_scores)))
    print("Median: ", statistics.median(sorted(one_d_scores)))
    print("Mode: ", statistics.mode(sorted(one_d_scores)))

    kde_plot([score[1] for score in scores])

import os, sys

sys.path.append(os.getcwd())

# from phevaluator.evaluator import evaluate_cardss
from evaluator.evaluate_cards import evaluate_cards as evaluate_cards

def rank(cards, rank_data):
    cards = list(cards)
    cards.sort()
    if tuple(cards) in rank_data:
        return rank_data[tuple(cards)], rank_data
    else:
        score = evaluate_cards(*cards)
        rank_data.update({
            tuple(cards): score
        })
        return score, rank_data
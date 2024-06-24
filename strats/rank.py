from phevaluator.evaluator import evaluate_cards

def rank(*cards, rank_data):
    cards = list(cards)
    cards.sort()
    if str(cards) in rank_data:
        return rank_data[str(cards)], rank_data
    else:
        score = evaluate_cards(*cards)
        rank_data.update({
            str(cards): score
        })
        return score, rank_data
from poker_metrics.simplified_hand_potential.potential import \
    potential2 as potentialPrivateValue

print(potentialPrivateValue(("Ad", "As"), ("2d", "3s", "4s")))

# from hand_evaluator.evaluate_cards import evaluate_cards

# print(evaluate_cards("As", "Ad", "Ac", "9d", "Ks"))

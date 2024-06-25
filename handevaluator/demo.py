import phevaluator_bindings as p

cards = ["9c", "4c", "4s", "9d", "4h", "Qc", "6c"]
rank = p.evaluate_cards(cards)
print(f"Rank: {rank}")

from phevaluator.evaluator import evaluate_cards
from itertools import combinations
import random
import time
rank = "23456789TJQKA"
suit = "csdh"
deck = [r+s for r in rank for s in suit]
possible_combinations = list(combinations(deck, 5))
total_time = 0
runs = 100000
for _ in range(runs):
    a = time.time()
    t = possible_combinations[random.randint(0, len(possible_combinations)-1)]
    _ = evaluate_cards(*t)
    b = time.time()
    total_time += b-a
print(f"Total time: {total_time}")
print(f"Average time for each process: {total_time/runs}")
# pheval(python): .69 seconds

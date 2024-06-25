from phevaluator.evaluator import evaluate_cards
from strats.hand_potential import potential
from itertools import combinations
import random
import time
from tqdm import tqdm
rank = "23456789TJQKA"
suit = "csdh"
deck = [r+s for r in rank for s in suit]
possible_combinations = list(combinations(deck, 5))
total_time = 0
runs = 100
for _ in tqdm(range(runs), desc="Processing..."):
    t = possible_combinations[random.randint(0, len(possible_combinations)-1)]
    a = time.time()
    _ = evaluate_cards(*t)
    # _ = potential(t[:2], t[2:], {})
    b = time.time()
    total_time += b-a
print(f"Total time: {total_time}")
print(f"Average time for each process: {total_time/runs}")
# pheval(python): .88 seconds
# base level potential optimisation (tuple and DP): 26000 seconds
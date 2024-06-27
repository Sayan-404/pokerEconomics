from phevaluator.evaluator import evaluate_cards
from evaluator.evaluate_cards import evaluate_cards as c_evaluate_cards
from strats.hand_potential import potential
from strats.simplified_hand_potential import potential as simple_pot
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
    t_deck = [card for card in deck if card not in t]
    a = time.time()
    # _ = evaluate_cards(*t)
    # _ = c_evaluate_cards(*t)
    # _ = potential(t_deck, t[:2], t[2:], {})
    _ = simple_pot(t_deck, t[:2], t[2:], 2)
    b = time.time()
    total_time += b-a
print(f"Total time: {total_time}")
print(f"Average time for each process: {total_time/runs}")
# pheval(python): .55 seconds
# pheval(c): .27 seconds
# base level potential optimisation (tuple and DP and python eval): 20688 seconds
# base level potential optimisation (tuple and DP and c eval): 15700 seconds
# simple potential 1 card look ahead (python eval): 29 seconds
# simple potential 2 card look ahead (python eval): 730 seconds
# simple potential 1 card look ahead (c eval): 14.4 seconds
# simple potential 2 card look ahead (c eval): 362 seconds

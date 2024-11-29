from hand_evaluator.evaluate_cards import evaluate_cards as c_evaluate_cards
from poker_metrics import odds
from poker_metrics.utils import privateValue
# from poker_metrics.ogpotential import potential
# from poker_metrics.outs import equity
from poker_metrics.potential.potential import potential as cpotential
from poker_metrics.hand_strength.shs import handStrength
from itertools import combinations
import random
import time
from tqdm import tqdm

rank = "23456789TJQKA"
suit = "csdh"
deck = [r+s for r in rank for s in suit]
possible_combinations = list(combinations(deck, 5))
total_time = 0
runs = 100000

deviation = []

for _ in tqdm(range(runs), desc="Processing..."):
    t = possible_combinations[random.randint(0, len(possible_combinations)-1)]
    t_deck = [card for card in deck if card not in t]
    a = time.time()
    # print(t[:2],t[2:])
    _ = cpotential(t[:2], t[2:])
    # _ = handStrength(hole=t[:2], board=t[2:])
    # _ = equity(t[:2], t[2:])
    # _ = odds(0.3, 0.7, 0.6, 0, 0.2)
    # _ = evaluate_cards(*t)
    # _ = c_evaluate_cards(*t)
    # _ = potential(t[:2], t[2:])
    # _ = simple_pot(t_deck, t[:2], t[2:], 2)
    # _ = equity(t[:2], t[2:])
    # _ = privateValue(t[:2], t[2:])
    b = time.time()
    total_time += b-a

print(f"Total time: {total_time}")
print(f"Average time for each process: {total_time/runs}")

# pheval(python): .55 seconds
# pheval(c): .27 seconds
# base level potential optimisation (tuple and DP and python eval): 20688 seconds
# base level potential (1 card look ahead) optimisation (tuple and DP and c eval): 15700 seconds
# base level potential (2 card look ahead) optimisation (tuple and DP and c eval): 332638 seconds
# simple potential 1 card look ahead (c eval): 15.5 seconds
# simple potential 2 card look ahead (c eval): 39700 seconds
# hand equity (flop): 5227 seconds
# hand equity (turn): 235 seconds
# hand equity (river): 0.399 seconds
# Hand equity by outs.py: 4.13 seconds
# Odds Total time: 57.63293266296387
# Odds Average time for each process: 0.0005763293266296387
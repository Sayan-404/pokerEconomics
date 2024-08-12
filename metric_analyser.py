from poker_metrics.potential import potential
from poker_metrics.outs import equity
from poker_metrics.hand_strength.shs import handStrength
from poker_metrics.utils import privateValue
from poker_metrics.utils import get_rank_category
from itertools import combinations
import numpy as np
import random
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style = 'whitegrid')   

rank = "23456789TJQKA"
suit = "csdh"
deck = [r+s for r in rank for s in suit]
possible_combinations = list(combinations(deck, 5))
total_time = 0
runs = 10000

deviation = []
outlier_category = {0.2: [], 0.15: [], 0.1: [], 0.05: [], 0.0: []} # abs(dev) > 

for _ in tqdm(range(runs), desc="Processing..."):
    t = possible_combinations[random.randint(0, len(possible_combinations)-1)]
    a = time.time()

    combination_equity = potential(t[:2], t[2:])
    
    b = time.time()
    total_time += b-a

    if(combination_equity >= 1 or combination_equity < 0):
        print(get_rank_category(t))
        print(t[:2], t[2:])

    enumeration_equity = equity(t[:2], t[2:])
    dev = enumeration_equity - combination_equity
    if abs(dev) > 0.2:
        outlier_category[0.2].append((get_rank_category(t), t))
    elif abs(dev) > 0.15:
        outlier_category[0.15].append((get_rank_category(t), t))
    elif abs(dev) > 0.1:
        outlier_category[0.1].append((get_rank_category(t), t))
    elif abs(dev) > 0.05:
        outlier_category[0.05].append((get_rank_category(t), t))
    elif abs(dev) > 0.0:
        outlier_category[0.0].append((get_rank_category(t), t))
    
    deviation.append(dev)

print(f"Total time: {total_time}")
print(f"Average time for each process: {total_time/runs}")


print(f"Range: {max(deviation) - min(deviation)}")

bin_edges = np.arange(-1, 1.05, 0.05)
hist, bin_edges = np.histogram(deviation, bins=bin_edges)

for i in range(len(hist)):
    print(f"Range {bin_edges[i]:.2f} to {bin_edges[i+1]:.2f}: {hist[i]}")

print(f"Outlier categories: {outlier_category}")

plt.figure(figsize=(10, 6))
sns.histplot(deviation, bins=bin_edges, kde=False)
plt.xlabel('Deviation')
plt.ylabel('Frequency')
plt.title('Histogram of Deviation')
plt.show()

sns.stripplot(x=deviation, jitter=True)
plt.show()
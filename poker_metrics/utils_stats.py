from utils import ir
from tqdm import tqdm
from itertools import combinations

import statistics

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import matplotlib

# Use PyQt5 backend for interactive mode
matplotlib.use('Qt5Agg')

def irStats():
    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = [r+s for r in ranks for s in suits]
    hole_cards = list(combinations(deck, 2))
    scores = []
    for i in tqdm(range(len(hole_cards))):
        scores.append((hole_cards[i], ir(hole_cards[i])))
    one_d_scores = [score[1] for score in scores]
    print(f"max: {max(one_d_scores)} min: {min(one_d_scores)}")

    print("Mean: ", statistics.mean(sorted(one_d_scores)))
    print("Median: ", statistics.median(sorted(one_d_scores)))
    print("Mode: ", statistics.mode(sorted(one_d_scores)))

    data = one_d_scores

    # Plot the KDE
    sns.kdeplot(data, fill=True)
    plt.title('Kernel Density Estimation')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.show()

    # Calculate KDE
    kde = gaussian_kde(data)

    # Generate a range of values to evaluate the KDE
    x = np.linspace(min(data), max(data), 1000)
    kde_values = kde(x)

    # Calculate the first derivative (slope) of the KDE
    slopes = np.gradient(kde_values, x)

    # Adjust slopes to make them more visible
    slope_factor = 10  # Increase this factor to make slopes more visible
    adjusted_slopes = slopes * slope_factor

    # Find points where the slope changes sign
    sign_changes = np.where(np.diff(np.sign(slopes)))[0]
    change_points = x[sign_changes]

    print("Points where the slope changes sign:")
    for point in change_points:
        print(point)

    # Plot the KDE and its slope
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Value')
    ax1.set_ylabel('Density', color=color)
    ax1.plot(x, kde_values, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Slope', color=color)
    ax2.plot(x, adjusted_slopes, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Kernel Density Estimation and Slope')
    plt.show()


if __name__ == "__main__":
    irStats()

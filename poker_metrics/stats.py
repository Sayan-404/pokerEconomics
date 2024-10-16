from tqdm import tqdm
from itertools import combinations

import statistics
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


def irStats():
    from utils import ir
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


def odds(lower_limit, upper_limit, hand_strength, risk, shift):
    from scipy.stats import truncnorm

    # Pot limit can never be less than 0 theoretically
    if lower_limit < 0:
        raise Exception("Lower limit can never be less than 0.")

    sigma = upper_limit/3
    mean = lower_limit + hand_strength*(risk + shift)

    t_lower = (lower_limit - mean) / sigma
    t_upper = (upper_limit - mean) / sigma
    dist = truncnorm(t_lower, t_upper, loc=mean, scale=sigma)

    # Plot the PDF of the truncated normal distribution
    x = np.linspace(lower_limit, upper_limit, 1000)
    pdf = dist.pdf(x)
    plt.plot(x, pdf, 'r-', lw=2, label='PDF of truncated normal distribution')

    ymin, ymax = plt.ylim()

    plt.vlines(lower_limit, ymin, ymax, colors='b',
               linestyles='--', label=f'Pot Odds {lower_limit}')
    plt.text(lower_limit, ymin,
             f' Pot Odds ({lower_limit})', color='b', verticalalignment='top')

    plt.vlines(lower_limit, ymin, ymax, colors='b',
               linestyles='--', label=f'Lower Limit {lower_limit}')
    plt.text(lower_limit, ymin,
             f' Lower Limit ({lower_limit})', color='b', verticalalignment='center')

    plt.vlines(upper_limit, ymin, ymax, colors='b',
               linestyles='--', label=f'Upper Limit {upper_limit}')
    plt.text(upper_limit, ymin,
             f' Upper Limit ({upper_limit})', color='b', verticalalignment='bottom')

    # plt.vlines(sigma, ymin, ymax, colors='b', linestyles='--', label=f'Sigma {sigma}')
    # plt.text(sigma, ymin, f' Sigma ({sigma})', color='b', verticalalignment='bottom')

    plt.vlines(mean, ymin, ymax, colors='b',
               linestyles='--', label=f'Mean {mean}')
    plt.text(mean, ymin, f' Mean ({mean})',
             color='b', verticalalignment='baseline')

    # Add labels and title
    plt.xlabel('Value')
    plt.ylabel('Probability Density')
    plt.title('Truncated Normal Distribution')
    plt.legend(loc='best')

    print(dist.rvs())

    # Show the plot
    plt.savefig("odds.png")


if __name__ == "__main__":
    # irStats()
    odds(0.8, 1, 0.9, 0, 0)

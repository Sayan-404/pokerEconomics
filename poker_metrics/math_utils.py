from itertools import combinations
from scipy.stats import truncnorm, norm

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def create_probabilistic_score(hole_cards, community_cards=[]):
    from . import chen, ph_score
    hole_cards = set(hole_cards)
    community_cards = set(community_cards)

    ranks = "23456789TJQKA"
    suits = "scdh"
    deck = set([r+s for r in ranks for s in suits])
    deck = deck - hole_cards
    deck = deck - community_cards
    opp_cards = list(combinations(deck, 2))

    w = {card: 1/len(opp_cards) for card in opp_cards}
    ahead = tied = behind = 0.0

    def get_score(cards):
        return chen.get_score(cards) if len(cards) == 2 else ph_score.get_score(cards)
    current_rank = get_score(hole_cards | community_cards)
    for cards in opp_cards:
        rank = get_score(set(cards) | community_cards)
        if rank < current_rank:
            ahead += w[cards]
        elif rank == current_rank:
            tied += w[cards]
        else:
            behind += w[cards]
    # *100 is the percentage of hands that we beat or at least tie given the input
    return ((ahead + tied/2) / (ahead + tied + behind))


def inverse_range(value, min_value, max_value):
    return (max_value + min_value) - value


def scale(value, old_min, old_max, new_min=0.0, new_max=10.0):
    return ((value - old_min) * (new_max - new_min) / (old_max - old_min)) + new_min


def kde_plot(scores):
    # Plot a KDE plot of the scores
    plt.figure(figsize=(10, 6))
    sns.kdeplot(scores, fill=True, color='blue')

    # Add titles and labels
    plt.title('Kernel Density Estimation of Poker Hole Card Scores')
    plt.xlabel('Score')
    plt.ylabel('Density')

    # Show the plot
    plt.grid(True)
    plt.show()


def odds(lower_limit, upper_limit, mean, std=0.5):

    lower_limit_trunc, upper_limit_trunc = (
        lower_limit - mean)/std, (upper_limit - mean)/std

    dist = truncnorm(lower_limit_trunc, upper_limit_trunc, loc=mean, scale=std)

    # return dist.rvs()

    # Plot the PDF of the truncated normal distribution
    x = np.linspace(lower_limit, upper_limit, 1000)
    pdf = dist.pdf(x)
    plt.plot(x, pdf, 'r-', lw=2, label='PDF of truncated normal distribution')

    # Add labels and title
    plt.xlabel('Value')
    plt.ylabel('Probability Density')
    plt.title('Truncated Normal Distribution')
    plt.legend(loc='best')

    print(dist.rvs())

    # Show the plot
    plt.show()


if __name__ == "__main__":
    odds(0, 5, 0, 0.575)
    # odds(0, 5, 0, 0.6)
    # odds(0, 5, 0, 0.675)
    # odds(0, 5, 0, 0.65)

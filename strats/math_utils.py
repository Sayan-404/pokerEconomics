import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

def create_probabilistic_score(hole_cards, community_cards=[]):
    from strats import ph_score
    from strats import chen
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
        if rank > current_rank:
            ahead += w[cards]
        elif rank == current_rank:
            tied += w[cards]
        else:
            behind += w[cards]
    return 1 - ((ahead + tied/2) / (ahead + tied + behind))

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
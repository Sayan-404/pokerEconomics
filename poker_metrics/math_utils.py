def create_probabilistic_score(hole_cards, community_cards=[]):
    from itertools import combinations
    from poker_metrics.ph_score import get_score
    
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
    from seaborn import kdeplot
    import matplotlib.pyplot as plt

    # Plot a KDE plot of the scores
    plt.figure(figsize=(10, 6))
    kdeplot(scores, fill=True, color='blue')

    # Add titles and labels
    plt.title('Kernel Density Estimation of Poker Hole Card Scores')
    plt.xlabel('Score')
    plt.ylabel('Density')

    # Show the plot
    plt.grid(True)
    plt.show()


def odds(lower_limit, upper_limit, hand_strength, risk, left_shift, r_shift, seed=None):
    from scipy.stats import truncnorm

    if seed:
        from numpy.random import seed as sd
        sd(seed)

    # Pot limit can never be less than 0 theoretically
    if lower_limit < 0:
        raise Exception("Lower limit can never be less than 0.")

    sigma = upper_limit/3
    mean = lower_limit + hand_strength*(r_shift + risk - left_shift)

    t_lower = (lower_limit - mean) / sigma
    t_upper = (upper_limit - mean) / sigma
    dist = truncnorm(t_lower, t_upper, loc=mean, scale=sigma)

    # Comment the return while viewing the distribution
    return dist.rvs()

if __name__ == "__main__":
    odds(0.8, 1, 0.8, 2, 0, 0)

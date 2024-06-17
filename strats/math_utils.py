import matplotlib.pyplot as plt
import seaborn as sns

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
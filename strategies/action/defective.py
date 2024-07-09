# Motive: Always return a prodigal move (raise/bet)

from poker_metrics.utils import prodigalMove


def decide(state):
    return prodigalMove(state)

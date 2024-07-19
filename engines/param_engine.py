import os
import sys

sys.path.append(os.getcwd())

import importlib
import json

# from checks.compare_test import compare_test
from components.Logger import Logger
from components.Player import Player
from Game import Game

from strategies.Strategy import Strategy

def initialise_run(id=0, benchmark=False, test=False):
    data = {}

    # Create a fully balanced strategy for comparison
    balanced_strat = Strategy()
    balanced_strat.eval = True

    test_strat = Strategy()
    test_strat.eval = True

    def test_decide(info):
        return test_strat.decide(info)

    def base_decide(info):
        return balanced_strat.decide(info)

    # Create players
    player1 = Player("base", 100000000, "base", getattr(balanced_strat, "decide"))
    player2 = Player("test", 100000000, "test", getattr(test_strat, "decide"))
    
    players = [player1, player2]

    seed = None
    if "seed" in data:
        seed = data["seed"]

    num = 100
    logger = Logger(log_hands=False, benchmark=benchmark, strategies=[player.strategy_name for player in players], number_of_hands=num)
    game = Game(
        players,
        logger,
        number_of_hands=num,
        simul=True,
        seed=seed,
        id=id,
        config=data,
        test=test,
    )
    return game


if __name__ == "__main__":
    # config = input("Enter name of config: ")
    game = initialise_run()
    game.play()
    # ch = input("Run compare test? (y/n): ")
    # if ch == "y" or ch == "yes":
    #     compare_test(f"{game.logger.path}/games.csv")

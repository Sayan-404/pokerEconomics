from multiprocessing import Pool
import os
import sys

sys.path.append(os.getcwd())

from Game import Game
from components.Player import Player
from components.Logger import Logger
from engines.utils import rationalStrat

# from checks.compare_test import compare_test
# from strategies.Strategy import Strategy

def initialise_run_param(obsVar, value, id=0, benchmark=False, test=False):
    data = {}
    limit = 100000

    # Create a fully balanced strategy for comparison

    balanced_strat = rationalStrat(limit)
    balanced_strat.eval = True

    test_strat = rationalStrat(limit)
    test_strat.eval = True

    if obsVar == "r_shift":
        test_strat.r_shift = value
    elif obsVar == "l_shift":
        test_strat.l_shift = value
    elif obsVar == "risk":
        test_strat.risk = value
    else:
        raise Exception("Invalid parameter given for evaluation.")

    # Create players
    player1 = Player("base", 100000000, "base",
                     getattr(balanced_strat, "decide"))
    player2 = Player(f"{obsVar}_{value}", 100000000,
                     "test", getattr(test_strat, "decide"))

    players = [player1, player2]

    seed = None
    if "seed" in data:
        seed = data["seed"]

    num = 100
    logger = Logger(log_hands=False, benchmark=benchmark, strategies=[
                    player.strategy_name for player in players], number_of_hands=num)

    retries = 0
    while True:
        try:
            game = Game(
                players,
                logger,
                number_of_hands=num,
                simul=True,
                seed=seed,
                id=id,
                config=data,
                test=False,
            )
            break
        except:
            retries += 1
            print("An error occurred while creating the Game object. Retrying...")

            if retries == 5:
                print("Simulation failed.")
                break
    return game


def run_game_auto(data):
    obs_var, c_val = data
    retries = 0
    while True:
        try:
            game = initialise_run_param(obs_var, c_val)
            game.play()
            break
        except:
            retries += 1
            print("An error occurred while executing game.play(). Retrying...")

            if retries == 5:
                print("Simulation failed.")
                break


if __name__ == "__main__":
    obs_var = input(
        "Enter variable under observation (1: r_shift; 2: l_shift; 3: risk, 4: limit): ")
    min_range = float(input("Enter minimum value to observe: "))
    max_range = float(input("Enter maximum value to observe: "))
    step = float(input("Enter the step value: "))

    match obs_var:
        case "1":
            obs_var = "r_shift"
        case "2":
            obs_var = "l_shift"
        case "3":
            obs_var = "risk"
        case "4":
            obs_var = "limit"
        case _:
            print("Invalid variable given. Exiting...")
            exit()

    params = []

    c_val = min_range
    while c_val < max_range:
        value = c_val + step
        params.append([obs_var, c_val])
        c_val = value

    with Pool(len(params)) as p:
        p.map(run_game_auto, params)

    print("Eval Completed")

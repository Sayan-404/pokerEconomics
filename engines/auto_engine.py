from multiprocessing import Pool
import os
import sys
import csv


sys.path.append(os.getcwd())

from Game import Game
from components.Player import Player
from components.Logger import Logger
from engines.utils import rationalStrat

# from checks.compare_test import compare_test
# from strategies.Strategy import Strategy

def strategies(configFile):
    strategies = []

    with open(f"configs/{configFile}.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            strategies.append(list(row))

    return strategies


def initialise_run_auto(limit, strats, iniLimitMultiplier, bankroll=1000000, id=0, benchmark=False, test=False):
    # print(strats)

    # Create a fully balanced strategy for comparison
    strat1 = rationalStrat(limit, r_shift=int(strats[0][1]), l_shift=float(strats[0][2]), risk=float(strats[0][3]), bluff=True if strats[0][4] == "True" else False, iniLimitMultiplier=iniLimitMultiplier)
    strat1.eval = True

    strat2 = rationalStrat(limit, r_shift=float(strats[1][1]), l_shift=float(strats[1][2]), risk=float(strats[1][3]), bluff=True if strats[1][4] == "True" else False, iniLimitMultiplier=iniLimitMultiplier)
    strat2.eval = True

    # Create players
    player1 = Player(f"{strats[0][0]}", bankroll, f"{strats[0][0]}",
                     getattr(strat1, "decide"))
    
    player2 = Player(f"{strats[1][0]}", bankroll, f"{strats[0][0]}",
                     getattr(strat2, "decide"))

    players = [player1, player2]

    seed = None
    # if "seed" in data:
    #     seed = data["seed"]

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
                config={},
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


def run_game_auto(config):
    strats = config["strats"]
    limit = config["limit"]
    iniLimitMul = config["iniLimitMul"]
    bankroll = config["bankroll"]

    retries = 0
    while True:
        try:
            game = initialise_run_auto(limit, strats, iniLimitMul, bankroll=bankroll)
            game.play()
            break
        except:
            retries += 1
            print("An error occurred while executing game.play(). Retrying...")

            if retries == 5:
                print("Simulation failed.")
                break


if __name__ == "__main__":
    configFile = input("Enter config file: ")
    limit = float(input("Enter overall limit: "))
    iniLimitMul = int(input("Enter initial round limit multiplier (-1 for none): "))
    bankroll = float(input("Enter bankroll of all players: "))
    
    if iniLimitMul == -1:
        iniLimitMul = None

    strats = strategies(configFile)
    
    print("\nList of strategies defined:")

    for i in range(len(strats)):
        print(f"{i}: {strats[i][0]}")

    i = int(input("Enter first strategy index: "))
    j = int(input("Enter second strategy index: "))

    eval_strats = []
    eval_strats.append(strats[i])
    eval_strats.append(strats[j])

    config = {
        "limit": limit,
        "iniLimitMul": iniLimitMul,
        "strats": eval_strats,
        "bankroll": bankroll
    }

    run_game_auto(config)
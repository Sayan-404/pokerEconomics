import os
import sys

sys.path.append(os.getcwd())

import importlib
import json

# from checks.compare_test import compare_test
from components.Logger import Logger
from components.Player import Player
from Game import Game

from engines.utils import *


if __name__ == "__main__":
    print("\nSingle-threaded Simulator\n\n0: For config based simulation\n1: For automatic simulation based on rational properties\n")

    while True:
        mode = int(input("Enter option: "))

        match mode:
            case 0:
                config = input("Enter name of config: ")
                game = initialise_run(config)
                game.play()
                break
            case 1:
                configFile = input("Enter config file: ")
                bankroll = float(input("Enter bankroll of all players: "))
                limit = float(input("Enter overall limit: "))
                iniLimitMul = int(input("Enter initial round limit multiplier (-1 for none): "))
                
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

                break

            case _:
                continue
    # ch = input("Run compare test? (y/n): ")
    # if ch == "y" or ch == "yes":
    #     compare_test(f"{game.logger.path}/games.csv")

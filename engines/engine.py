import os
import sys

sys.path.append(os.getcwd())

# from checks.compare_test import compare_test
from components import Inspector
from engines.utils import *


"""
    Runs a single-threaded simulator for a poker game. Provides two options:
    0. Run a simulation based on a configuration file.
    1. Run a manual simulation based on user input for game properties.

    The simulation can be configured with a rational configuration file (.csv) and
    various game parameters such as bankroll, limit, and initial round limit
    multiplier. The available strategies are listed, and the user can select two
    strategies to evaluate.

    The simulation is run using the `run_game_auto()` function.
"""
if __name__ == "__main__":
    print("\nSingle-threaded Simulator\n\n0: For config based simulation\n1: For manual simulation based on input of game properties\n")

    while True:
        mode = int(input("Enter option: "))

        match mode:
            case 0:
                """
                    In this mode, a config.json file is given as input.

                    The config.json file has all the parameters of game simulation.

                    The engine then runs the simulation based on the parameters in config.json.
                """

                # This configuration file contains all the parameters for simulation
                # The file is a .json file
                # For format, check the README
                config = input("Enter name of config: ")

                # This configuration file is the name of the rational config file
                # The "rational config file" contains the parameters for each strategies
                # The file is a .csv file
                # For format, check the README
                ratConfig = input("Enter name of rational config file (.csv): ")

                inspector = None

                if 'y' in input("Run inspector? (y/n): "):
                    inspector = Inspector()

                # Get a configured game object by calling `initialise_run_config`
                game = initialise_run_config(config, rat_config=ratConfig, inspector=inspector)

                # Play the game & exit
                game.play()

                inspector.joinAndLog(['Sourjya', 'Sayan'])

                if inspector:
                    while 'y' not in input('Press "y" to stop inspector: '):
                        continue

                    inspector.stop_server()


                break

            case 1:
                # This configuration file is the name of the rational config file
                # The "rational config file" contains the parameters for each strategies
                # The file is a .csv file
                # For format, check the README
                configFile = input("Enter name of rational config file (.csv): ")

                # Bankroll for all the players
                bankroll = float(input("Enter bankroll of all players: "))

                # This is the default limit for rounds other than pre-flop
                # Again, this is for all the players
                limit = float(input("Enter overall limit: "))

                # This is the multiplier for initial pot
                # This will be the limit for pre-flop
                # Calculated as `initialPot * iniLimitMul`
                # Same for all the players
                iniLimitMul = int(input("Enter initial round limit multiplier (-1 for none): "))

                # Get the seed
                seed = int(input("Enter seed (-1 for none): "))

                # Get number of hands/runs to play
                runs = int(input("Enter number of hands: "))

                if seed == -1:
                    seed = None

                strats = strategies(configFile)
                
                print("\nList of strategies defined:")

                for i in range(len(strats)):
                    print(f"{i}: {strats[i][0]}")

                # Get the the indexes
                i = int(input("Enter first strategy index: "))
                j = int(input("Enter second strategy index: "))

                # Generate the dictionary file to run the simulation
                eval_strats = []
                eval_strats.append(strats[i])
                eval_strats.append(strats[j])

                config = {
                    "limit": limit,
                    "iniLimitMul": iniLimitMul,
                    "strats": eval_strats,
                    "bankroll": bankroll,
                    "seed": seed,
                    "runs": runs
                }

                run_game_manual(config)

                break

            case _:
                continue
    # ch = input("Run compare test? (y/n): ")
    # if ch == "y" or ch == "yes":
    #     compare_test(f"{game.logger.path}/games.csv")

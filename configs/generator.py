# DEFAULTS:
# bankroll = 1000000000
# id and strategy names are kept the same
# simulation = True
import json
import re
import os

def create_single_config():
    filename = input("Enter config name: ")
    filename = f"configs/{filename}.json"
    runs = int(input("Enter number of runs: "))
    log_hands = True if input("Enter y to log individual hand data: ") == "y" else False
    strat1 = input("Enter strategy(type.name) for player 1: ")
    strat2 = input("Enter strategy(type.name) for player 2: ")
    seed = input("Enter seed if present: ")
    create_config_file(filename, log_hands, runs, strat1, strat2, seed)

def generate_round_robin_strategy_configs():
    strats = []
    types = ["action", "value"]
    for ty in types:
        files = os.listdir(f"strats/{ty}/")
        for strat in files:
            x = re.search(".py$", strat)
            if x:
                y = f"{ty}.{x.string.split('.')[0]}"
                strats.append(y)
    enum_strats = {i:strats[i] for i in range(len(strats))}
    print("Enter the numbers (separated by spaces) corresponding to the strategies according to the list below: ")
    for key in enum_strats:
        print(f"{key}: {enum_strats[key]}")
    keys = input().split()
    strats = []
    for key in keys:
        key = int(key)
        if key not in enum_strats:
            print(f"Key: {key} not found, skipping.")
        else:
            strats.append(enum_strats[key])

    log_hands = True if input("Enter y to log individual hands: ") == "y" else False
    runs = int(input("Enter number of runs: "))
    seed = input("Enter seed if present: ")
    for i in range(len(strats)):
        for j in range(i+1, len(strats)):
            s1 = strats[i]
            s2 = strats[j]
            create_config_file(f"configs/{s1}_vs_{s2}", log_hands, runs, s1, s2, seed)


def create_config_file(filename, log_hands, runs, strat1, strat2, seed=None):
    with open(f"{filename}.json", "w") as f:
        json.dump({
            "log_hands": log_hands,
            "runs": runs,
            "simulation": True,
            "player1": {"id": strat1, "bankroll": 1000000000, "strategy": strat1},
            "player2": {"id": strat2, "bankroll": 1000000000, "strategy": strat2},
            "seed": seed if seed else None
        }, f, indent=4)

if __name__ == "__main__":
    ch = input("Enter 1 to generate single config and 2 to generate configs for multiple strategy pairs: ")
    if ch == "1":
        create_single_config()
    elif ch == "2":
        generate_round_robin_strategy_configs()
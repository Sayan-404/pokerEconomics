# DEFAULTS:
# bankroll = 1000000000
# id and strategy names are kept the same
# simulation = True
import json
import os
import re
import sys
import time

sys.path.append(os.getcwd())


def create_single_config():
    filename = input("Enter config name: ")
    filename = f"configs/{filename}"
    runs = int(input("Enter number of runs: "))
    log_hands = True if input(
        "Enter y to log individual hand data: ") == "y" else False
    strat1 = input("Enter strategy(type.name) for player 1: ")
    strat2 = input("Enter strategy(type.name) for player 2: ")
    seed = input("Enter seed if present: ")
    if (not seed) :
        seed = None
    limit = int(input("Enter limit: "))
    iniLimit = int(input("Enter iniLimit: "))
    create_config_file(
        filename=filename, 
        log_hands=log_hands, 
        runs=runs, 
        bankroll=100000000000,
        strat1=strat1, 
        strat2=strat2, 
        limit=limit, 
        initlimit=iniLimit, 
        seed=seed)


def generate_round_robin_strategy_configs():
    strats = []
    # types = ["action", "rational"]
    # for ty in types:
    #     files = os.listdir(f"strategies/{ty}/")
    #     for strat in files:
    #         x = re.search(".py$", strat)
    #         if x:
    #             y = f"{ty}.{x.string.split('.')[0]}"
    #             strats.append(y)
    
    import csv

    with open(f"configs/config.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            strats.append(row[0])

    enum_strats = {i: strats[i] for i in range(len(strats))}
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

    log_hands = True if input(
        "Enter y to log individual hands: ") == "y" else False
    runs = int(input("Enter number of runs: "))
    seed = int(input("Enter seed if present: "))
    if not seed:
        seed = time.time()
    bankroll = int(input("Enter bankroll (-1 for default of 1000000000): "))
    bankroll = bankroll if bankroll != -1 else 100000000000
    
    limit = int(input("Enter limit (-1 for default of 5000): "))
    limit = limit if limit != -1 else 5000

    initlimit = int(input("Enter iniLimitMul (-1 for default of 100): "))
    initlimit = initlimit if initlimit != -1 else 100

    for i in range(len(strats)):
        for j in range(i+1, len(strats)):
            s1 = strats[i]
            s2 = strats[j]
            # Replace / with _
            filename = f"configs/{s1.replace('/', '_')}_vs_{s2.replace('/', '_')}"
            create_config_file(
                filename, log_hands, bankroll, runs, s1, s2, limit, initlimit, seed)


def create_config_file(filename, log_hands, bankroll, runs, strat1, strat2, limit, initlimit, seed=None):
    with open(f"{filename}.json", "w") as f:
        json.dump({
            "log_hands": log_hands,
            "runs": runs,
            "simulation": True,
            "player1": {"id": strat1, "bankroll": int(bankroll), "strategy": strat1, "limit": limit, "iniLimitMul": initlimit},
            "player2": {"id": strat2, "bankroll": int(bankroll), "strategy": strat2, "limit": limit, "iniLimitMul": initlimit},
            "seed": seed if seed else None
        }, f, indent=4)


if __name__ == "__main__":
    ch = input(
        "Enter 1 to generate single config and 2 to generate configs for multiple strategy pairs: ")
    if ch == "1":
        create_single_config()
    elif ch == "2":
        generate_round_robin_strategy_configs()

import os, sys

sys.path.append(os.getcwd())

import re
import multiprocessing
from engine import initialise_run

def run_game(data):
    id, config = data
    game = initialise_run(config, id)
    game.play()

if __name__ == "__main__":
    optimal_instances = int(input("Enter optimal number of instances/ processes (run benchmark.py to get optimal number of processes): "))
    if optimal_instances <= 0:
        print("Negative instances not allowed")
        exit(1)
    configs = []
    files = os.listdir("configs/")
    for config in files:
        x = re.search(".json$", config)
        if x:
            y = x.string.split(".")[0]
            if y != "config" and y != "benchmark_config":
                configs.append(x.string.split(".")[0])
    enum_configs = {i:configs[i] for i in range(len(configs))}
    configs = []
    print("Enter numbers (separated by spaces) corresponding to configs according to the list below: ")
    for key in enum_configs:
        print(f"{key}: {enum_configs[key]}")
    keys = input().split()
    for key in keys:
        key = int(key)
        if key not in enum_configs:
            print(f"Key: {key} not found, skipping.")
        else:
            configs.append(enum_configs[key])
    if len(configs) > optimal_instances:
        ch = input(print("Number of configs chosen exceeds optimal number of instances, do you still wish to continue? (y/n): "))
        if ch != "y":
            exit(1)
    print(f"Total number of instances: {len(configs)}.")
    if len(configs) < 1:
        print("quitting ...")
        exit(1)
    payload = enumerate(configs)
    with multiprocessing.Pool(processes=len(configs)) as pool:
        pool.map(run_game, list(payload))
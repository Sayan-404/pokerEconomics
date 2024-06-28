from engine import initialise_run
from multiprocessing import Pool
import json
import os
import sys

sys.path.append(os.getcwd())


def configList():
    List = []

    with open("configs/test_configs.json") as f:
        data = json.load(f)

        for config in data:
            List.append(config)

    return List


def run_game(data):
    id, config = data
    game = initialise_run(config, id=id, test=True)
    game.play()


if __name__ == "__main__":
    configs = configList()

    params = []

    for i in range(len(configs)):
        id = i
        data = [id, configs[i]]
        params.append(data)

    with Pool(len(configs)) as p:
        p.map(run_game, params)

    print("Tests completed successfully.")

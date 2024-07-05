import gc
import os
import re
import sys
import traceback
from multiprocessing import get_context

from aws import shutdownInstance
from engine import initialise_run

sys.path.append(os.getcwd())

def init_pool(configs):
    global shared_configs
    shared_configs = configs

def run_game(data):
    """
    Worker processes for multiprocessing.
    """
    id, config = data
    game = initialise_run(shared_configs[id], id)
    game.play()
    del game
    gc.collect()

def run_configs(configs):
    payload = list(enumerate(configs))
    num_processes = min(len(configs), os.cpu_count() or 1)
    ctx = get_context("spawn")
    with ctx.Pool(processes=num_processes, initializer=init_pool, initargs=(configs,)) as pool:
        results = pool.map(run_game, payload)
        pool.close()
        pool.join()
    gc.collect()

# be a little conservative in choosing the total number of optimal instances
# in reality this multi engine will run an iteration, that is one multi process after another
# one less in the first and one more in the second might actually increase efficiency
# in simple words squeezing too many processes might bot be worth it


if __name__ == "__main__":
    aws = True if input("Is this running on AWS? (y/n): ") == "y" else False

    try:
        configs = []
        batch = input("Enter batch: ")
        directory = f"configs/{batch}" if batch else ""
        files = os.listdir(directory)
        for config in files:
            x = re.search(".json$", config)
            if x:
                y = x.string.split(".")[0]
                if y != "config" and y != "benchmark_config":
                    configs.append(x.string[0:x.string.rfind(".")])

        enum_configs = {i: configs[i] for i in range(len(configs))}
        configs = []
        print("Enter numbers (separated by spaces) corresponding to configs according to the list below (-1 for all): ")
        for key in enum_configs:
            print(f"{key}: {enum_configs[key]}")
        keys = input().split()

        if int(keys[0]) == -1:
            keys = [i for i in range(len(enum_configs))]

        for key in keys:
            key = int(key)
            if key not in enum_configs:
                print(f"Key: {key} not found, skipping.")
            else:
                configs.append(
                    f"{batch}/{enum_configs[key]}" if batch != "" else enum_configs[key])

        run_configs(configs)
    except Exception as e:
        print(f"An error occurred.")
        traceback.print_exc()
    finally:
        # shuts down the instance
        # add an IAM role with ec2:StopInstance permission and add this role to the ec2 instance
        if aws:
            shutdownInstance()

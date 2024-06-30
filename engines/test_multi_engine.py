import multiprocessing
import re
import math
import os
import sys
import traceback
import gc

from engine import initialise_run

sys.path.append(os.getcwd())

from aws import shutdownInstance

def run_game(data):
    id, config = data
    game = initialise_run(config, id)
    game.play()
    gc.collect()


def run_configs(configs):
    payload = enumerate(configs)
    with multiprocessing.Pool(processes=len(configs)) as pool:
        pool.map(run_game, list(payload))


def optimised_run_configs(configs):
    # time.sleep(5)
    payload = enumerate(configs)
    with multiprocessing.Pool(processes=len(configs)) as pool:
        results = pool.imap(run_game, list(payload))
        for result in results:
            # Process each result as it becomes available
            gc.collect()

# be a little conservative in choosing the total number of optimal instances
# in reality this multi engine will run an iteration, that is one multi process after another
# one less in the first and one more in the second might actually increase efficiency
# in simple words squeezing too many processes might bot be worth it


def benchmark():
    configs = []
    batch = "test_batch_2"
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
    keys = [i for i in range(len(enum_configs))]

    for key in keys:
        key = int(key)
        if key not in enum_configs:
            print(f"Key: {key} not found, skipping.")
        else:
            configs.append(
                f"{batch}/{enum_configs[key]}" if batch != "" else enum_configs[key])

    run_configs(configs)

# be a little conservative in choosing the total number of optimal instances
# in reality this multi engine will run an iteration, that is one multi process after another
# one less in the first and one more in the second might actually increase efficiency
# in simple words squeezing too many processes might bot be worth it


if __name__ == "__main__":
    aws = True if input("Is this running on AWS? (y/n): ") == "y" else False

    try:
        optimal_instances = int(input(
            "Enter optimal number of instances/ processes (run benchmark.py to get optimal number of processes): "))
        
        if optimal_instances <= 0:
            print("Negative instances not allowed")
            exit(1)

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
                
        if len(configs) > optimal_instances:
            ch = input(
                "Number of configs chosen exceeds optimal number of instances, do you wish to run in groups? (y/n): ")
            
            if ch.lower() in ["n", "no"]:
                ch = input("WARNING: are you sure? (y/n): ")
                print(f"Total number of instances: {len(configs)}.")
                if len(configs) < 1:
                    print("quitting ...")
                    exit(1)
                run_configs(configs)

            elif ch.lower() in ["y", "yes"]:
                num_groups = math.ceil(len(configs) / optimal_instances)
                print(f"Total groups: {num_groups}")
                config_groups = []
                num_members = len(configs) // num_groups
                for i in range(num_groups-1):
                    t = []
                    for j in range(num_members*i, num_members*i+num_members):
                        t.append(configs[j])
                    config_groups.append(t)
                t = []
                for j in range(num_members*(num_groups-1), len(configs)):
                    t.append(configs[j])
                config_groups.append(t)
                for i in range(len(config_groups)):
                    print(f"RUNNING GROUP #{i}")
                    run_configs(config_groups[i])
        else:
            run_configs(configs)
    except Exception as e:
        print(f"An error occurred.")
        traceback.print_exc()
    finally:
        # shuts down the instance
        # add an IAM role with ec2:StopInstance permission and add this role to the ec2 instance
        if aws:
            shutdownInstance()
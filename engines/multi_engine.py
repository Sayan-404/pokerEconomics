import gc
import os
import re
import sys
import traceback
from multiprocessing import get_context

sys.path.append(os.getcwd())

from aws import shutdownInstance
from engine import initialise_run



def init_pool(configs):
    global shared_configs
    shared_configs = configs


def game_runner(data):
    """
    Worker processes for multiprocessing.
    """
    id, config = data
    game = initialise_run(shared_configs[id], id)
    game.play()
    del game
    gc.collect()

def run(payload, runner, configs={}):
    num_processes = min(len(payload), os.cpu_count() or 1)
    ctx = get_context("spawn")
    with ctx.Pool(processes=num_processes, initializer=init_pool, initargs=(configs if configs else payload,)) as pool:
        results = pool.map(runner, payload)
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
        print("\nSimulation Menu\n\n1: Run simulations with configs\n2: Automate Simulations from config.csv\n3: Evaluate parameters of rational strategies\n0: To exit")


        while True:
            inp = int(input("Enter an appropriate option: "))
            print()

            match inp:
                case 0:
                    break

                # Run simulations with pre-defined configs
                case 1:
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

                    payload = list(enumerate(configs))
                    
                    run(payload, game_runner, configs=configs)
                    
                    print("Simulation is successful.\n")
                    ex = True if input("Exit? (y/n): ") == "y" else False
                    if ex:
                        break
                    print()

                # Evaluate parameters of rational strategies
                case 3:
                    # Lazy loading
                    from param_engine import run_game_auto

                    obs_var = input(
                        "Enter variable under observation (1: r_shift; 2: l_shift; 3: risk, 4: limit): ")
                    min_range = float(input("Enter minimum value to observe: "))
                    max_range = float(input("Enter maximum value to observe: "))
                    step = float(input("Enter the step value: "))

                    while True:
                        match obs_var:
                            case "1":
                                obs_var = "r_shift"
                                break
                            case "2":
                                obs_var = "l_shift"
                                break
                            case "3":
                                obs_var = "risk"
                                break
                            case "4":
                                obs_var = "limit"
                                break
                            case _:
                                obs_var = input(
                                    "Enter variable under observation (1: r_shift; 2: l_shift; 3: risk, 4: limit): ")

                    params = []

                    c_val = min_range
                    while c_val < max_range:
                        value = c_val + step
                        params.append([obs_var, c_val])
                        c_val = value

                    run(params, run_game_auto)

                    print("Evaluation Completed.\n")
                    ex = True if input("Exit? (y/n): ") == "y" else False
                    if ex:
                        break
                    print()
                case _:
                    continue


    except Exception as e:
        print(f"An error occurred.")
        traceback.print_exc()
    finally:
        # shuts down the instance
        # add an IAM role with ec2:StopInstance permission and add this role to the ec2 instance
        if aws:
            shutdownInstance()

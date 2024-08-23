import os
import sys

sys.path.append(os.getcwd())

def run(payload, runner, configs={}):
    from gc import collect
    from engines.utils import init_pool
    from multiprocessing import get_context

    num_processes = min(len(payload), os.cpu_count() or 1)
    ctx = get_context("spawn")
    with ctx.Pool(processes=num_processes, initializer=init_pool, initargs=(configs if configs else payload,)) as pool:
        results = pool.map(runner, payload)
        pool.close()
        pool.join()
    collect()    

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
                    from engines.utils import run_game
                    from re import search

                    configs = []
                    batch = input("Enter batch: ")
                    directory = f"configs/{batch}" if batch else ""
                    files = os.listdir(directory)
                    for config in files:
                        x = search(".json$", config)
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
                    
                    run(payload, run_game, configs=configs)
                    
                    print("Simulation is successful.\n")
                    ex = True if input("Exit? (y/n): ") == "y" else False
                    if ex:
                        break
                    print()

                # Take properties from csv and run simulation
                case 2:
                    from engines.utils import strategies, run_game_auto
                    from itertools import combinations_with_replacement

                    configFile = input("Enter config file: ")
                    bankroll = float(input("Enter initial bankroll of all players: "))
                    limit = float(input("Enter overall limit: "))
                    iniLimitMul = int(input("Enter initial round limit multiplier (-1 for none): "))
                    seed = float(input("Enter seed (-1 for None): "))
                    
                    if iniLimitMul == -1:
                        iniLimitMul = False

                    if seed == -1:
                        seed = None

                    strats = strategies(configFile)
                    
                    print("\nList of strategies defined:")

                    for i in range(len(strats)):
                        print(f"{i}: {strats[i][0]}")

                    indexes = input("Enter all the strategy indexes to pair and run: ").split(" ")
                    indexes = [int(i) for i in indexes]

                    eval_strats = []
                    for i in range(len(strats)):
                        if i in indexes:
                            eval_strats.append(strats[i])

                    pairings = list(combinations_with_replacement(eval_strats, 2))
                    payload = []
                    
                    for pairing  in pairings:
                        config = {
                            "limit": limit,
                            "iniLimitMul": iniLimitMul,
                            "strats": pairing,
                            "bankroll": bankroll,
                            "seed": seed
                        }
                        payload.append(config)

                    run(payload, run_game_auto)

                    print("Simulation Completed.\n")
                    ex = True if input("Exit? (y/n): ") == "y" else False
                    if ex:
                        break
                    print()

                # Evaluate parameters of rational strategies
                case 3:
                    # Lazy loading
                    from engines.utils import run_game_param
                    
                    nums = int(input("Enter runs: "))
                    obs_var = input(
                        "Enter variable under observation (1: r_shift; 2: l_shift; 3: risk, 4: limit): ")
                    min_range = float(input("Enter lower limit of range to observe: "))
                    max_range = float(input("Enter upper limit of range to observe: "))
                    step = float(input("Enter the step value: "))
                    seed = float(input("Enter seed: "))
                    limit = float(input("Enter limit: "))
                    iniLimitMul = float(input("Enter initial round limit: "))

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
                    id = 0
                    while c_val < max_range:
                        value = c_val + step
                        params.append([seed, obs_var, c_val, nums, limit, iniLimitMul, id])
                        c_val = value
                        id += 1
                    run(params, run_game_param)

                    print("Evaluation Completed.\n")
                    ex = True if input("Exit? (y/n): ") == "y" else False
                    if ex:
                        break
                    print()
                case _:
                    continue


    except Exception as e:
        from traceback import print_exc
        print(f"An error occurred.")
        print_exc()
    finally:
        # shuts down the instance
        # add an IAM role with ec2:StopInstance permission and add this role to the ec2 instance
        if aws:
            from engines.utils import shutdownInstance
            shutdownInstance()

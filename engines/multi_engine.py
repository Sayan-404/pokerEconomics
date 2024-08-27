import os 
import sys

# Adds the current working directory to the system path to allow importing modules from the current directory.
sys.path.append(os.getcwd())

def run(payload, runner, configs={}):
    """
    Manages the parallel execution of tasks using multiprocessing.
    
    Args:
        payload (list): List of tasks or configurations to process.
        runner (function): The function that will be run on each item in the payload.
        configs (dict, optional): Configurations passed to the worker pool initializer.
    """
    from gc import collect  
    from engines.utils import init_pool  
    from multiprocessing import get_context

    # Determine the number of processes to use, which is the minimum between the length of the payload and the number of CPU cores.
    num_processes = min(len(payload), os.cpu_count() or 1)
    
    # Create a multiprocessing context using the 'spawn' method, which is safer on some platforms.
    ctx = get_context("spawn")
    
    # Initialize a pool of worker processes with the specified initializer and arguments.
    with ctx.Pool(processes=num_processes, initializer=init_pool, initargs=(configs if configs else payload,)) as pool:
        # Run the runner function on each item in the payload concurrently.
        _ = pool.map(runner, payload)
        pool.close()  # Close the pool to prevent any more tasks from being submitted.
        pool.join()  # Wait for all worker processes to finish.
    
    collect()  # Collect any garbage that might be left after the multiprocessing operations.

if __name__ == "__main__":
    # Ask the user if the script is running on an AWS instance.
    aws = True if input("Is this running on AWS? (y/n): ") == "y" else False

    try:
        print("\nSimulation Menu\n\n1: Run simulations with configs\n2: Automate Simulations from config.csv\n3: Evaluate parameters of rational strategies\n0: To exit")

        while True:
            # Prompt the user to select an option from the menu.
            inp = int(input("Enter an appropriate option: "))
            print()

            match inp:
                case 0:
                    # Exit the loop if the user chooses to quit.
                    break

                case 1:
                    # Run simulations using predefined configurations.
                    from engines.utils import run_game  
                    from re import search  

                    # Prompt for a batch name or identifier.
                    configs = []
                    batch = input("Enter batch: ")  
                    directory = f"configs/{batch}" if batch else ""  
                    files = os.listdir(directory) 
                    
                    # Filter out JSON files that match certain criteria.
                    for config in files:
                        x = search(".json$", config)
                        if x:
                            y = x.string.split(".")[0]
                            if y != "config" and y != "benchmark_config":
                                configs.append(x.string[0:x.string.rfind(".")])

                    # Enumerate the configs for user selection.
                    enum_configs = {i: configs[i] for i in range(len(configs))}
                    configs = []
                    print("Enter numbers (separated by spaces) corresponding to configs according to the list below (-1 for all): ")
                    for key in enum_configs:
                        print(f"{key}: {enum_configs[key]}")
                    keys = input().split()

                    # Allow user to select all configs with -1, or select specific ones.
                    if int(keys[0]) == -1:
                        keys = [i for i in range(len(enum_configs))]

                    # Add selected configs to the list based on user input.
                    for key in keys:
                        key = int(key)
                        if key not in enum_configs:
                            print(f"Key: {key} not found, skipping.")
                        else:
                            configs.append(
                                f"{batch}/{enum_configs[key]}" if batch != "" else enum_configs[key])

                    # Create the payload for processing.
                    payload = list(enumerate(configs))
                    
                    # Run the simulations with the selected configs.
                    run(payload, run_game, configs=configs)
                    
                    print("Simulation is successful.\n")
                    ex = True if input("Exit? (y/n): ") == "y" else False
                    if ex:
                        break
                    print()

                case 2:
                    # Automate simulations based on properties defined in a CSV file.
                    from engines.utils import strategies, run_game_manual  
                    from itertools import combinations_with_replacement 

                    configFile = input("Enter config file (without .csv): ")  # Prompt for the config file name.
                    runs = int(input("Enter number of hands: ")) # Number of hands for which the simulation will be done
                    bankroll = float(input("Enter initial bankroll of all players: "))  # Initial bankroll for players.
                    limit = float(input("Enter overall limit: "))  # Overall limit for the simulation.
                    iniLimitMul = int(input("Enter initial round limit multiplier (-1 for none): "))  # Multiplier for initial round limit.
                    seed = float(input("Enter seed (-1 for None): "))  # Seed for random number generation.

                    if seed == -1:
                        seed = None  # Disable seeding if input is -1.

                    strats = strategies(configFile)  # Load strategies from the config file.
                    
                    print("\nList of strategies defined:")

                    # Display the strategies loaded from the file.
                    for i in range(len(strats)):
                        print(f"{i}: {strats[i][0]}")

                    # Prompt the user to select strategy indexes to pair and run.
                    indexes = input("Enter all the strategy indexes to pair and run: ").split(" ")
                    indexes = [int(i) for i in indexes]

                    eval_strats = []
                    for i in range(len(strats)):
                        if i in indexes:
                            eval_strats.append(strats[i])  # Add selected strategies to the list.

                    # Create pairings of strategies to evaluate.
                    pairings = list(combinations_with_replacement(eval_strats, 2))
                    payload = []
                    
                    # Build the payload for simulation.
                    for pairing in pairings:
                        config = {
                            "runs": runs,
                            "limit": limit,
                            "iniLimitMul": iniLimitMul,
                            "strats": pairing,
                            "bankroll": bankroll,
                            "seed": seed
                        }
                        payload.append(config)

                    # Run the automated simulations with the generated payload.
                    run(payload, run_game_manual)

                    print("Simulation Completed.\n")
                    ex = True if input("Exit? (y/n): ") == "y" else False
                    if ex:
                        break
                    print()

                case 3:
                    # Evaluate parameters for rational strategies based on user inputs.
                    from engines.utils import run_game_param  # Import parameter evaluation function.
                    
                    nums = int(input("Enter runs: "))  # Number of runs for the simulation.
                    obs_var = input("Enter variable under observation (1: shift, 2: risk, 3: bluff): ")  # Variable under observation.
                    min_range = float(input("Enter lower limit of range to observe: "))  # Lower bound of the range.
                    max_range = float(input("Enter upper limit of range to observe: "))  # Upper bound of the range.
                    step = float(input("Enter the step value: "))  # Step value for the range.
                    seed = float(input("Enter seed: "))  # Seed value for random number generation.
                    limit = float(input("Enter limit: "))  # Overall limit.
                    iniLimitMul = float(input("Enter initial round limit: "))  # Initial round limit multiplier.

                    # Validate the user's choice of observation variable.
                    while True:
                        match obs_var:
                            case "1":
                                obs_var = "shift"
                                break
                            case "2":
                                obs_var = "risk"
                                break
                            case "3":
                                obs_var = "bluff"
                                break
                            case _:
                                obs_var = input("Enter variable under observation (1: shift, 2: risk, 3: bluff): ")  # Variable under observation.


                    params = []  # List to hold parameter configurations.

                    # Generate parameter configurations over the specified range.
                    c_val = min_range
                    id = 0
                    while c_val < max_range:
                        value = c_val + step
                        params.append([seed, obs_var, c_val, nums, limit, iniLimitMul, id])
                        c_val = value
                        id += 1

                    # Run the simulations with the generated parameters.
                    run(params, run_game_param)

                    print("Evaluation Completed.\n")
                    ex = True if input("Exit? (y/n): ") == "y" else False
                    if ex:
                        break
                    print()

                case _:
                    continue  # If an invalid option is entered, continue the loop.

    except Exception as e:
        from traceback import print_exc  
        print(f"Exception occurred: {str(e)}")
        print_exc()
        if aws:
            from engines.utils import shutdownInstance  
            shutdownInstance()  # Shut down the AWS instance in case of an error.

        # Force exit with a non-zero status code.
        os._exit(1)

    if aws:
        from engines.utils import shutdownInstance 
        shutdownInstance()  # Shut down the AWS instance.

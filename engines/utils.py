import os
import sys
from dotenv import load_dotenv

# Add the current working directory to the Python path to allow imports from the project.
sys.path.append(os.getcwd())

from components import Player, Logger
from Game import Game

# Load environment variables from a .env file.
load_dotenv()

# Accessing AWS-related environment variables for instance management.
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
aws_instance = os.getenv('AWS_INSTANCE')

def init_pool(configs):
    """
    Initialize a global configuration pool that can be shared across different processes or modules.
    """
    global shared_configs
    shared_configs = configs

def shutdownInstance():
    """
    Shut down an AWS EC2 instance using boto3. The instance ID, access keys, and region are obtained
    from environment variables.
    """
    import boto3
    try:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        ec2 = session.client('ec2')
        ec2.stop_instances(InstanceIds=[aws_instance])
        print(f"Instance {aws_instance} is shutting down.")
    except Exception as e:
        import traceback
        print(f"Failed to shut down instance: \n{traceback.print_exc()}")

def rationalStrat(limit, r_shift=0, l_shift=0, risk=0, bluff=0, iniLimitMultiplier=None):
    """
    Create a rational strategy configuration for a game.

    Parameters:

        - limit - The betting limit.
        - r_shift - Right shift for strategy adjustments.
        - l_shift - Left shift for strategy adjustments.
        - risk - Risk factor in the strategy.
        - bluff - Bluffing factor in the strategy.
        - iniLimitMultiplier - Initial limit multiplier if specified.

    Returns:

        - A configured Strategy object.
    """
    from strategies.Strategy import Strategy

    # Create a strategy object
    strat = Strategy()

    # Give the properties to the strategy
    strat.eval = True
    strat.r_shift = r_shift
    strat.l_shift = l_shift
    strat.risk = risk
    strat.defaultLimit = limit
    strat.bluff = bluff
    strat.iniLimitMultiplier = iniLimitMultiplier

    # Returns the strategy object
    return strat

def strategies(configFile):
    """
    Load strategy configurations from a CSV file.

    Parameters:

        - configFile - The name of the configuration file (without the .csv extension).

    Returns:

        - A list of strategies with properties read from the CSV file.
    """
    import csv
    strategies = []
    
    # Get the properties mentioned in rational strategies' config file
    with open(f"configs/{configFile}.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            strategies.append(list(row))

    return strategies

def get_player_decider(player, rat_config='config'):
    """
    Retrieve the decision-making function for a player based on their strategy.

    Parameters:

        - player - A dictionary containing player information, including strategy.
        - rat_config - The configuration file name for rational strategies.

    Returns:

        - A decision-making function `decide` corresponding to the player's strategy.
    """
    import importlib

    try:
        # Get the actual module from strategies directory if exists
        module = importlib.import_module("strategies.{}".format(player["strategy"]))
        return getattr(module, "decide")
    except ImportError:
        # Get the module from rational config
        strats = strategies(rat_config)
        strat = next((strat for strat in strats if strat[0] == player["strategy"]), None)

        # Raise exception if strategy does not exist
        if strat is None:
            raise Exception(f"Strategy {player['strategy']} does not exist.")
        
        # Set up a strategy object with properties
        strat = rationalStrat(player['limit'], float(strat[1]), float(strat[2]), float(strat[3]), int(strat[4]), player["iniLimitMul"])

        # Return the decide function
        return getattr(strat, "decide")

def initialise_run_config(config, id=0, benchmark=False, test=False, rat_config='config'):
    """
    Initialize and configure a game run based on a JSON configuration file.

    Parameters:

        - config - The name of the JSON configuration file (without the .json extension).
        - id - The ID of the run.
        - benchmark - A boolean indicating whether to enable benchmarking.
        - test - A boolean indicating whether this is a test run.
        - rat_config - The configuration file name for rational strategies.

    Returns:

        - A configured Game object.
    """
    data = {}

    if test:
        data = config
    else:
        # If not test then extract the config.json file
        import json
        with open(f"configs/{config}.json", "r") as f:
            data = json.load(f)

    # Create players
    player1 = Player(
        data["player1"]["id"],
        data["player1"]["bankroll"],
        data["player1"]["strategy"],
        get_player_decider(data["player1"], rat_config),
    )

    player2 = Player(
        data["player2"]["id"],
        data["player2"]["bankroll"],
        data["player2"]["strategy"],
        get_player_decider(data["player2"], rat_config),
    )

    players = [player1, player2]

    seed = None
    if "seed" in data:
        seed = data["seed"]

    # Initialise the game object
    num = data["runs"]
    logger = Logger(log_hands=data["log_hands"], benchmark=benchmark, strategies=[player.strategy_name for player in players], number_of_hands=num)
    game = Game(
        players,
        logger,
        number_of_hands=num,
        simul=data["simulation"],
        seed=seed,
        id=id,
        config=data,
        test=test,
    )

    # Return the configured game object
    return game

def initialise_run_manual(runs, seed, limit, strats, iniLimitMultiplier, bankroll=1000000, id=0, benchmark=False):
    """
    Initialize and configure a game run with automatic player setup.

    Parameters:

        - seed - The seed for random number generation.
        - limit - The betting limit.
        - strats - A list of strategies for the players.
        - iniLimitMultiplier - Initial limit multiplier for the strategies.
        - bankroll - The starting bankroll for each player.
        - id - The ID of the run.
        - benchmark - A boolean indicating whether to enable benchmarking.

    Returns:
        - A configured Game object.
    """

    # Create the strategy objects for both players
    # Equivalent of importing a children strategy module
    strat1 = rationalStrat(
        limit, 
        r_shift=float(strats[0][1]), 
        l_shift=float(strats[0][2]), 
        risk=float(strats[0][3]), 
        bluff=int(strats[0][4]), 
        iniLimitMultiplier=iniLimitMultiplier
    )

    strat2 = rationalStrat(
        limit, 
        r_shift=float(strats[1][1]), 
        l_shift=float(strats[1][2]), 
        risk=float(strats[1][3]), 
        bluff=int(strats[1][4]), 
        iniLimitMultiplier=iniLimitMultiplier
    )

    # Create players
    player1 = Player(f"{strats[0][0]}", bankroll, f"{strats[0][0]}", getattr(strat1, "decide"))
    player2 = Player(f"{strats[1][0]}", bankroll, f"{strats[0][0]}", getattr(strat2, "decide"))

    # Set up parameters of Game object
    players = [player1, player2]
    logger = Logger(log_hands=False, benchmark=benchmark, strategies=[player.strategy_name for player in players], number_of_hands=runs)

    # Create the game object and return it
    game = Game(
        players,
        logger,
        number_of_hands=runs,
        simul=True,
        seed=seed,
        id=id,
        config={},
        test=False,
    )

    return game

def initialise_run_param(seed, obsVar, value, num, limit, iniLimitMul, id=0, benchmark=False, test=False):
    """
        Initialize and configure a game run with parameterized strategies for comparison.

        Parameters:

            - seed - The seed for random number generation.
            - obsVar - The variable to observe (e.g., 'r_shift', 'l_shift', 'risk').
            - value - The value of the observed variable.
            - num - The number of hands to simulate.
            - limit - The betting limit.
            - iniLimitMul - Initial limit multiplier for the strategies.
            - id - The ID of the run.
            - benchmark - A boolean indicating whether to enable benchmarking.
            - test - A boolean indicating whether this is a test run.

        Returns:
        - A configured Game object.
    """

    # Create strategies for comparison
    balanced_strat = rationalStrat(limit=limit, iniLimitMultiplier=iniLimitMul)
    test_strat = rationalStrat(limit=limit, iniLimitMultiplier=iniLimitMul)

    if obsVar == "r_shift":
        test_strat.r_shift = value
    elif obsVar == "l_shift":
        test_strat.l_shift = value
    elif obsVar == "risk":
        test_strat.risk = value
    else:
        raise Exception("Invalid parameter given for evaluation.")

    # Create players
    player1 = Player("base", 1000000000000, "base", getattr(balanced_strat, "decide"))
    player2 = Player(f"test_{obsVar}_{value}", 1000000000000, f"test_{obsVar}_{value}", getattr(test_strat, "decide"))

    # Initialise and return the configured game object
    players = [player1, player2]
    logger = Logger(log_hands=False, benchmark=benchmark, strategies=[player.strategy_name for player in players], number_of_hands=num)
    game = Game(
        players,
        logger,
        number_of_hands=num,
        simul=True,
        seed=seed,
        id=id,
        config={},
        test=test,
    )

    return game


def run_game(data):
    """
    Runs a game simulation with the provided configuration.
    
    Args:
        data (tuple): A tuple containing the game ID and the game configuration.
    
    Returns:
        None
    """
    from gc import collect
    id, config = data
    game = initialise_run_config(shared_configs[id], id)
    game.play()
    del game
    collect()

def run_game_param(data):
    """
    Runs a game simulation with the provided configuration parameters.
    
    Args:
        data (tuple): A tuple containing the following parameters:
            - seed (int): The seed value for the game's random number generator.
            - obs_var (str): The name of the observation variable to be tested.
            - c_val (float): The value of the observation variable to be tested.
            - nums (int): The number of hands to be played in the simulation.
            - limit (int): The limit for the game.
            - iniLimitMul (int): The initial limit multiplier for the game.
            - id (str): The unique identifier for the game.
    
    Returns:
        None
    """
    from gc import collect
    seed, obs_var, c_val, nums, limit, iniLimitMul, id = data

    # Get the game object & play
    game = initialise_run_param(seed, obs_var, c_val, nums, limit, iniLimitMul, id = id)
    game.play()
    del game
    collect()


def run_game_manual(config):
    """
    Runs a game simulation with the provided configuration parameters.
    
    Args:
        config (dict): A dictionary containing the following configuration parameters:
            - strats (list): A list of strategies to be used in the game.
            - limit (int): The limit for the game.
            - iniLimitMul (int): The initial limit multiplier for the game.
            - bankroll (float): The initial bankroll for the game.
            - seed (int): The seed value for the game's random number generator.
    
    Returns:
        - None
    """

    # Get all the simulation attributes from the config dictionary
    strats = config["strats"]
    limit = config["limit"]
    iniLimitMul = config["iniLimitMul"]
    bankroll = config["bankroll"]
    seed = config["seed"]
    runs = config["runs"]

    # Get configured game from `initialise_run_manual` and run the game
    game = initialise_run_manual(runs, seed, limit, strats, iniLimitMul, bankroll=bankroll)
    game.play()


if __name__ == "__main__":
    """
    Test the utility module by creating a game with default parameters.
    """    
    game = initialise_run_param(seed=1, obsVar="r_shift", value=0.5, num=100000, limit=50000, iniLimitMul=100)
    game.play()

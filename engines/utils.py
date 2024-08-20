import os
import sys

from dotenv import load_dotenv

sys.path.append(os.getcwd())

from components import Player, Logger
from Game import Game

load_dotenv()

# Accessing the environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
aws_instance = os.getenv('AWS_INSTANCE')


def init_pool(configs):
    global shared_configs
    shared_configs = configs

def shutdownInstance():
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


def rationalStrat(limit, r_shift=0, l_shift=0, risk=0, bluff=False, iniLimitMultiplier=None):
    from strategies.Strategy import Strategy

    strat = Strategy()
    strat.eval = True
    strat.r_shift = r_shift
    strat.l_shift = l_shift
    strat.risk = risk
    strat.limit = limit

    if iniLimitMultiplier:
        strat.iniLimit = True
        strat.iniLimitMultiplier = iniLimitMultiplier

    return strat

def strategies(configFile):
    import csv
    strategies = []

    with open(f"configs/{configFile}.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            strategies.append(list(row))

    return strategies

def get_player_decider(player):
    import importlib

    try:
        module = importlib.import_module("strategies.{}".format(player["strategy"]))
        return getattr(module, "decide")
    except ImportError:
        strats = strategies('config')
        strat = next((strat for strat in strats if strat[0] == player["strategy"]), None)

        if strat == None:
            raise Exception(f"Strategy {player['strategy']} does not exist.")
        
        strat = rationalStrat(100000, float(strat[1]), float(strat[2]), float(strat[3]), True if strat[4] == "True" else False, 0)

        return getattr(strat, "decide")

def initialise_run(config, id=0, benchmark=False, test=False):
    data = {}

    if test:
        data = config
    else:
        import json
        with open(f"configs/{config}.json", "r") as f:
            data = json.load(f)

    # Create players
    player1 = Player(
        data["player1"]["id"],
        data["player1"]["bankroll"],
        data["player1"]["strategy"],
        get_player_decider(data["player1"]),
    )
    player2 = Player(
        data["player2"]["id"],
        data["player2"]["bankroll"],
        data["player2"]["strategy"],
        get_player_decider(data["player2"]),
    )
    players = [player1, player2]

    seed = None
    if "seed" in data:
        seed = data["seed"]

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
    return game


def initialise_run_auto(limit, strats, iniLimitMultiplier, bankroll=1000000, id=0, benchmark=False, test=False):
    # Create a fully balanced strategy for comparison
    strat1 = rationalStrat(limit, r_shift=float(strats[0][1]), l_shift=float(strats[0][2]), risk=float(strats[0][3]), bluff=True if strats[0][4] == "True" else False, iniLimitMultiplier=iniLimitMultiplier)
    strat1.eval = True

    strat2 = rationalStrat(limit, r_shift=float(strats[1][1]), l_shift=float(strats[1][2]), risk=float(strats[1][3]), bluff=True if strats[1][4] == "True" else False, iniLimitMultiplier=iniLimitMultiplier)
    strat2.eval = True

    # Create players
    player1 = Player(f"{strats[0][0]}", bankroll, f"{strats[0][0]}",
                     getattr(strat1, "decide"))
    
    player2 = Player(f"{strats[1][0]}", bankroll, f"{strats[0][0]}",
                     getattr(strat2, "decide"))

    players = [player1, player2]

    seed = None
    # if "seed" in data:
    #     seed = data["seed"]

    num = 100000
    logger = Logger(log_hands=False, benchmark=benchmark, strategies=[
                    player.strategy_name for player in players], number_of_hands=num)

    retries = 0
    while True:
        try:
            game = Game(
                players,
                logger,
                number_of_hands=num,
                simul=True,
                seed=seed,
                id=id,
                config={},
                test=False,
            )
            break
        except:
            retries += 1
            print("An error occurred while creating the Game object. Retrying...")

            if retries == 5:
                print("Simulation failed.")
                break
    return game

def initialise_run_param(obsVar, value, id=0, benchmark=False, test=False):
    data = {}
    limit = 100000

    # Create a fully balanced strategy for comparison

    balanced_strat = rationalStrat(limit)
    balanced_strat.eval = True

    test_strat = rationalStrat(limit)
    test_strat.eval = True

    if obsVar == "r_shift":
        test_strat.r_shift = value
    elif obsVar == "l_shift":
        test_strat.l_shift = value
    elif obsVar == "risk":
        test_strat.risk = value
    else:
        raise Exception("Invalid parameter given for evaluation.")

    # Create players
    player1 = Player("base", 100000000, "base",
                     getattr(balanced_strat, "decide"))
    player2 = Player(f"{obsVar}_{value}", 100000000,
                     "test", getattr(test_strat, "decide"))

    players = [player1, player2]

    seed = None
    if "seed" in data:
        seed = data["seed"]

    num = 100
    logger = Logger(log_hands=False, benchmark=benchmark, strategies=[
                    player.strategy_name for player in players], number_of_hands=num)

    retries = 0
    while True:
        try:
            game = Game(
                players,
                logger,
                number_of_hands=num,
                simul=True,
                seed=seed,
                id=id,
                config=data,
                test=False,
            )
            break
        except:
            retries += 1
            print("An error occurred while creating the Game object. Retrying...")

            if retries == 5:
                print("Simulation failed.")
                break
    return game


def run_game(data):
    """
    Worker processes for multiprocessing.
    """
    from gc import collect
    id, config = data
    game = initialise_run(shared_configs[id], id)
    game.play()
    del game
    collect()

def run_game_param(data):
    from gc import collect
    obs_var, c_val = data
    retries = 0
    while True:
        try:
            game = initialise_run_param(obs_var, c_val)
            game.play()
            del game
            collect()
            break
        except:
            retries += 1
            print("An error occurred while executing game.play(). Retrying...")

            if retries == 5:
                print("Simulation failed.")
                break

def run_game_auto(config):
    strats = config["strats"]
    limit = config["limit"]
    iniLimitMul = config["iniLimitMul"]
    bankroll = config["bankroll"]

    retries = 0
    while True:
        try:
            game = initialise_run_auto(limit, strats, iniLimitMul, bankroll=bankroll)
            game.play()
            break
        except:
            retries += 1
            print("An error occurred while executing game.play(). Retrying...")

            if retries == 5:
                print("Simulation failed.")
                break
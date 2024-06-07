from Player import Player
from Logger import Logger
from Game import Game
import importlib
import json


def get_player_decider(player):
    module = importlib.import_module("strats.{}".format(player["strategy"]))
    return getattr(module, "decide")


if __name__ == "__main__":
    data = {}
    with open('config.json','r') as f:
        data = json.load(f)

    # Create players
    player1 = Player(data['player1']['id'], data['player1']['bankroll'], data["player1"]["strategy"], get_player_decider(data["player1"]))
    player2 = Player(data['player2']['id'], data['player2']['bankroll'], data["player2"]["strategy"], get_player_decider(data["player2"]))
    players = [player1, player2]
    
    seed = None
    if "seed" in data:
        seed = data["seed"]

    num = data["runs"]
    logger = Logger(log_hands=data["log_hands"])
    game = Game(players, logger, number_of_hands=num, simul=data["simulation"], seed=seed[0])

    # create multiple game objects in an ordered manner according to seeds if present, then start simulation

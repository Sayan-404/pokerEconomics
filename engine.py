from Player import Player
from Logger import Logger
from Game import Game
import importlib
import json

def get_player_decider(player):
    module = importlib.import_module("strats.{}".format(player["strategy"]))
    return getattr(module, "decide")

if __name__ == "__main__":
    players = {}
    with open('players.json','r') as f:
        players = json.load(f)

    # Create players
    player1 = Player(players['player1']['id'], players['player1']['bankroll'], get_player_decider(players["player1"]))
    player2 = Player(players['player2']['id'], players['player2']['bankroll'], get_player_decider(players["player2"]))
    players = [player1, player2]
    
    num = 1000
    logger = Logger()
    logger.log_config(players, num)
    game = Game(players, logger, True)
    game.play(num)
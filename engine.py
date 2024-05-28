from Player import Player
from Game import Game
import importlib
import json

def get_player_decider(player):
    module = importlib.import_module(f"strats.{player["strategy"]}")
    return getattr(module, "decide")

if __name__ == "__main__":
    players = {}
    with open('players.json','r') as f:
        players = json.load(f)

    # Create players
    player1 = Player(players['player1']['name'], players['player1']['bankroll'], get_player_decider(players["player1"]))
    player2 = Player(players['player2']['name'], players['player2']['bankroll'], get_player_decider(players["player2"]))
    player3 = Player("Player3", 100, "strat1")
    players = [player1, player2, player3]
    
    num = 100
    game = Game(players, True)
    game.play(num)
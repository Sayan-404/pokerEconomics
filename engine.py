from Player import Player
from Game import Game
import json

if __name__ == "__main__":
    players = {}
    with open('players.json','r') as f:
        players = json.load(f)

    # Create players
    player1 = Player(players['player1']['name'], players['player1']['bankroll'])
    player2 = Player(players['player2']['name'], players['player2']['bankroll'])
    players = [player1, player2]
    
    num = 2
    game = Game(players)
    game.play(num)
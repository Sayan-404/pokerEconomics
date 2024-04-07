import random
from Deck import Deck
from Card import Card
from Player import Player
from Game import Game
import json
if __name__ == "__main__":
    #importing players
    # players= {
    #     'player1' : {'name':'Player 1', 'bankroll': 100},
    #     'player2' : {'name':'Player 2', 'bankroll': 100}
    # }
    players={}
    with open('players.json','r') as f:
        players=json.load(f)

    # Create players
    player1 = Player(players['player1']['name'], players['player1']['bankroll'])
    player2 = Player(players['player2']['name'], players['player2']['bankroll'])

    # Create deck and shuffle

    # for player in players:
    #     print(f"{player.name}'s cards")
    #     for card in player.hand:
    #         print(f"{card.rank}{card.suit}")

    num=2
    games=[]
    prev=0
    for i in range(num):
        game = Game(player1,player2)
        game.preflop_action(prev)
        prev=(prev+1)%2
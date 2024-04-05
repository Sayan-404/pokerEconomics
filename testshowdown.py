from Deck import Deck
from Player import Player
import json

deck = Deck()
deck.shuffle()

players={}
with open('players.json','r') as f:
    players=json.load(f)

# Create players
player1 = Player(players['player1']['name'], players['player1']['bankroll'])
player2 = Player(players['player2']['name'], players['player2']['bankroll'])

for i in range(2):
    player1.receive_card(deck.deal_card())
    player2.receive_card(deck.deal_card())
    
p1cards = 



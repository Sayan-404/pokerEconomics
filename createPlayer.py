import json 
players= {
        'player1' : {'name':'Sayan', 'bankroll': 100},
        'player2' : {'name':'Player 2', 'bankroll': 100}
    }


with open("players.json","w") as o:
    json.dump(players,o)
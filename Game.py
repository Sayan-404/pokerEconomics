from Deck import Deck
from Player import Player
from Showdown import showdown
class Game:
    def __init__(self,player1,player2):
        self.deck= Deck()
        self.deck.shuffle()
        self.pot=0
        self.player1 = player1
        self.player2 = player2
        # deals cards to players
        for i in range(2):
            player1.receive_card(self.deck.deal_card())
            player2.receive_card(self.deck.deal_card())
    
    # increments the pot by the bet amount whenever a player bets
    def playerBet(self, player, amt):
        self.pot += player.bet(amt)
    
    #displays info at the end of a hand
    def gameover(self):
        print("Hand Ended")
        print(f"player1 stack: {self.player1.bankroll}")
        print(f"player2 stack: {self.player2.bankroll}")
        exit(1)
    
    #showdown
    def display(self,players): 
        #player1 strength
        communitycards=[]
        for i in range(5):
            communitycards.append(self.deck.deal_card().strval())
        #give the pot to the winner
        print(communitycards)
        player1 = players[0]
        player2 = players[1]
        s = showdown(player1, player2,communitycards)
        winner=players[s.winner()]
        print(f"winner: {winner.name}")
        self.gameover()

    #handles the preflop action
    def preflop_action(self,prev):
        betsize = 1
        #decides the dealer according to the prev variable
        if prev in [2, 0]:
            dealer = self.player1
            bb = self.player2
        else:
            dealer = self.player1 
            bb = self.player2
        
        #blinds 
        self.playerBet(dealer,1)
        self.playerBet(bb,2)

        action = ""
        current=dealer
        opp=bb 
        callcount=0
        players=[dealer,bb]
        #printing the cards:
        print(f"{dealer.name}'s cards")
        for card in dealer.hand:
            print(f"{card.strval()}")
        print(f"{opp.name}'s cards")
        for card in opp.hand:
            print(f"{card.strval()}")

        while 1:
            if callcount == 2:
                self.display(players)
            print(f"pot -> {self.pot}")
            action=input(f"{current.name}'s -> c / r / f \n")
            if action == "f":
                print(action)
                opp.bankroll += self.pot
                self.pot = 0
                print(f"{current.name} folds")
                self.gameover()
            if action == "c":
                if betsize >= 1:
                    self.playerBet(current,betsize)
                    print(f"{current.name} calls")
                    players = [self.player1, self.player2]
                    betsize=0
                    callcount+=1
                else:
                    callcount+=1
            if action == "r":
                betsize = int(input("Enter the sizing"))
                self.playerBet(current, betsize)
                print(f"{current.name} raise: {betsize}")
            temp=current
            current=opp
            opp=temp

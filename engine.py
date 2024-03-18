import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        suits = ['H', 'D', 'C', 'S']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]


    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Player:
    def __init__(self, name, bankroll):
        self.name = name
        self.hand = []
        self.bankroll = bankroll

    def receive_card(self, card):
        self.hand.append(card)
    
    def bet(self,unit):
        self.bankroll -= unit
        return unit

# Create players
player1 = Player("Player 1", 100)
player2 = Player("Player 2", 100)

# Create deck and shuffle
deck = Deck()
deck.shuffle()

class Game:
    def __init__(self):
        deck= Deck()
        deck.shuffle()
        self.pot=0
        
        # deals cards to players
        for i in range(2):
            player1.receive_card(deck.deal_card())
            player2.receive_card(deck.deal_card())
    
    # increments the pot by the bet amount whenever a player bets
    def playerBet(self, player, amt):
        self.pot += player.bet(amt)
    
    #displays info at the end of a hand
    def gameover(self):
        print("Hand Ended")
        print(f"player1 stack: {player1.bankroll}")
        print(f"player2 stack: {player2.bankroll}")
        exit(1)
    
    def returnHigherCard(self,card1,card2):
        face_cards = {'J':11, 'Q':12, 'K':13, 'A':14}
        # if card1 in face_cards:
        #     value1 = face_cards[card1]
        # else:
        #     value1 = int(card1)
        value1 = face_cards[card1] if card1 in face_cards else int(card1)
        value2 = face_cards[card2] if card2 in face_cards else int(card2)
        return value1 if value1 >= value2 else value2
    #showdown
    def showdown(self,players): 
        #player1 strength
        face_cards = {'J':11, 'Q':12, 'K':13, 'A':14}
        handstrength = {}
        for player in players:
            if player.hand[0].rank == player.hand[1].rank:
                cardvalue = self.returnHigherCard(player.hand[0].rank,player.hand[0].rank)
                handstrength[player] = [2,cardvalue]
            else:
                cardvalue= self.returnHigherCard(player.hand[0].rank,player.hand[1].rank)
                handstrength[player] = [1,cardvalue]
        # prints the handstrength
        for player in players:
            print(handstrength[player])
            print(handstrength[player][0])
        winner=players[0]

        for player in players:

            for i in range(2):
                if handstrength[player][i] > handstrength[winner][i]:
                    winner = player

        #give the pot to the winner
        winner.bankroll += self.pot
        print(f"{winner.name} wins")
        self.gameover()



        
                    
            
   
    #handles the preflop action
    def preflop_action(self,prev):
        betsize = 1
        #decides the dealer according to the prev variable
        if prev in [2, 0]:
            dealer = player1
            bb = player2
        else:
            dealer = player1 
            bb = player2
        
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
            print(f"{card.rank}{card.suit}")
        print(f"{opp.name}'s cards")
        for card in opp.hand:
            print(f"{card.rank}{card.suit}")

        while 1:
            if callcount == 2:
                self.showdown(players)
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
                    players = [player1, player2]
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

game1=Game()
players=[player1,player2]

# for player in players:
#     print(f"{player.name}'s cards")
#     for card in player.hand:
#         print(f"{card.rank}{card.suit}")

game1.preflop_action(0)
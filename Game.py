from Deck import Deck
from Showdown import Showdown
class Game:
    def __init__(self, *players):
        self.deck = Deck()
        self.deck.shuffle()
        self.pot = 0
        self.players = players
        self.number_of_players = len(players)
        self.community_cards=[]

    def play(self, num):
        # assign the number of games to be played
        for _ in range(num):
            self.preflop_action()
            # Rotates list so as to put the dealer at index 0, starting with dealer at index 0
            self.players = self.players[1:] + self.players[:1]

    # increments the pot by the bet amount whenever a player bets
    def player_bet(self, player, amt):
        self.pot += player.bet(amt)
    
    def betting(self, current, opp, bet_size):
        callcount = 0
        while 1:
            if callcount == 2:
                return
            print(f"pot -> {self.pot}")
            action = input(f"{current.name}'s -> c / r / f \n")
            if action == "f":
                print(action)
                opp.bankroll += self.pot
                self.pot = 0
                print(f"{current.name} folds")
                self.gameover()
            if action == "c":
                if bet_size >= 1:
                    self.playerBet(current,bet_size)
                    print(f"{current.name} calls")
                    players = [self.player1, self.player2]
                    bet_size = 0
                    callcount += 1
                else:
                    callcount += 1
            if action == "r":
                bet_size = int(input("Enter the sizing"))
                self.playerBet(current, bet_size)
                print(f"{current.name} raise: {bet_size}")
            temp = current
            current = opp
            opp = temp
        
    #displays info at the end of a hand
    def gameover(self):
        print("Hand Ended")
        for i in range(self.number_of_players):
            print(f'player{i} stack: {self.players[i].bankroll}')
    
    #showdown
    def showdown(self, players):
        s = Showdown(self.community_cards, *players)
        winner = players[s.winner()]
        winner.bankroll += self.pot
        print(f"winner: {winner.name}")
        self.gameover()

    #handles the preflop action
    def preflop(self):
        print("-------PRE-FLOP------")
        for i in range(self.number_of_players):
            self.players[i].receive_card(self.deck.deal_card())

        bet_size = 1

        #blinds 
        self.playerBet(self.players[0], 1)
        self.playerBet(self.players[1], 2)

        #printing the cards:
        for i in range(self.number_of_players):
            print(f"{self.players[i]}'s cards")
            for card in self.players[i].hand:
                print(card)

        self.betting(self.players[0], self.players[1], bet_size)
        self.flop()

    def flop(self):
        print("-------FLOP------")

        bet_size = 0

        #displaying the flop
        for i in range(3):
            self.community_cards.append(str(self.deck.deal_card()))
        
        print(self.community_cards) 

        self.betting(self.players[1], self.players[0], bet_size)
        self.turn()


    def turn(self):
        print("-------TURN------")
        bet_size = 0
        
        self.community_cards.append(str(self.deck.deal_card()))
        
        print(self.community_cards)

        self.betting(self.players[1], self.players[0], bet_size)
        self.river()

    def river(self):
        print("-------RIVER------")
        bet_size = 0
        
        self.community_cards.append(str(self.deck.deal_card()))
        
        print(self.community_cards)

        self.betting(self.players[1], self.players[0], bet_size)
        self.showdown(self.players)
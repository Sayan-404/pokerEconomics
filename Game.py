from Deck import Deck
from Showdown import Showdown
class Game:
    def __init__(self, players):
        self.deck = Deck()
        self.deck.shuffle()
        self.pot = 0
        self.players = players
        self.number_of_players = len(players)
        self.community_cards=[]

    def flush(self):
        self.deck.flush()
        for player in self.players:
            player.flush()
        self.community_cards = []


    def play(self, number_of_hands):
        for _ in range(number_of_hands):
            print("flushing done")
            self.preflop()
            self.flush()
            # rotates the dealer
            self.players = self.players[-1:] + self.players[0:-1]
            self.pot=0

    # increments the pot by the bet amount whenever a player bets'
    def player_bet(self, player, amt):
        self.pot += player.bet(amt - player.betamt)

    def bettingB(self, players,betsize):
        playing=len(players)
        while 1:
            for player in players:
                if player.ingame == 0:
                    continue
                action=input(f"{player.name}'s action -> call / check / bet / raise / fold")
                if betsize>0:
                    if action == "c":
                        self.player_bet(player,betsize)
                if action == "ch":
                    continue
                if action == "b":
                    betsize = player.betamt + int(input(f"Enter the betsize: "))
                    self.player_bet(player,betsize)
                    print(f"betsize -> {betsize}")
                    print(f"{player.name}'s betamt = {player.betamt}")
                if betsize>0:
                    if action == "r":
                        betsize = player.betamt + int(input(f"Enter the raise: "))
                        self.player_bet(player,betsize)
                if action == "f":
                    player.ingame=0
                    playing -= 1
            if playing == 1:
                players[0].bankroll = self.pot
                self.gameover()
                return 0
           
            #checks if each of the player has bet the betsize
            count=0
            firstplayerBet=players[0].betamt
            for player in players:
                print(f"{player.betamt}")   
                if player.betamt == firstplayerBet:
                    count += 1
            if count == len(players):
                return
                              
    def betting(self,players,betsize):
        
        #the last player where the action finishes
        end=len(players)-1

        playing=len(players)
        i=0

        while 1:
            
            print(f"i -> {i}")
            print(f"end -> {end}")

            player=players[i%len(players)]

            print(f"{player.name}'s bankroll -> {player.bankroll}")
            #check if the player is stil in the current game 
            if player.ingame == 0:
                continue

            action=input(f"{player.name}'s action -> call / check / bet / raise / fold")
            
            if action=="c":
                self.player_bet(player,betsize)
                # else:
                #     print("fucked up")
                #     i=(i+len(players))%len(players)
                #     continue

            if action=="ch":
                self.player_bet(player,betsize)
                
            if action == "b":   
                betsize = player.betamt + int(input(f"Enter the betsize: "))
                self.player_bet(player,betsize)
                end=(i-1)%len(players)
                
            if action=="r":
                betsize = player.betamt + int(input(f"Enter the raise: "))
                self.player_bet(player,betsize)
                end=(i-1)%len(players)#Sets the loop to end on player before this

            if action == "f":
                player.ingame=0
                playing -= 1

            #if there is only one person playing then gameover
            if playing == 1:
                players[0].bankroll += self.pot
                self.gameover()
                return 0
            #exit condtion for the loop when all the players have called
            if i == end:
                break
            i=(i+1)%len(players)
            

    #handles the preflop action
    def preflop(self):
        print("-------PRE-FLOP------")
        for i in range(self.number_of_players):
            self.players[i].receive_card(self.deck.deal_card())
            self.players[i].receive_card(self.deck.deal_card())


        bet_size = 2

        #blinds 
        self.player_bet(self.players[0], 1)
        self.player_bet(self.players[1], 2)
        print("----BLINDS-----")
        print(f"{self.players[0].name}'s blind -> {self.players[0].betamt}")
        print(f"{self.players[1].name}'s blind -> {self.players[1].betamt}")
        #printing the cards:
        for i in range(self.number_of_players):
            print(f"{self.players[i].name}'s cards")
            for card in self.players[i].hand:
                print(card, end=" ")
            print()

        if self.betting(self.players, bet_size) != 0:
            self.flop()

    def flop(self):
        print("-------FLOP------")

        bet_size = 0

        #resetting the betamts
        for player in self.players:
            player.betamt=0

        #displaying the flop
        for i in range(3):
            self.community_cards.append(str(self.deck.deal_card()))
        
        print(self.community_cards) 

        if self.betting(self.players, bet_size) != 0:
            self.turn()
        


    def turn(self):
        print("-------TURN------")
        bet_size = 0
        
        #resetting the betamts
        for player in self.players:
            player.betamt=0

        self.community_cards.append(str(self.deck.deal_card()))
        
        print(self.community_cards)

        if self.betting(self.players, bet_size) != 0:
            self.river()

    def river(self):
        print("-------RIVER------")
        bet_size = 0
        
        #resetting the betamts
        for player in self.players:
            player.betamt=0

        self.community_cards.append(str(self.deck.deal_card()))
        
        print(self.community_cards)

        if self.betting(self.players, bet_size) != 0:
            self.showdown(self.players)

     #displays info at the end of a hand
    def gameover(self):
        print("Hand Ended")
        for i in range(self.number_of_players):
            print(f'{self.players[i].name} stack: {self.players[i].bankroll}')
    
    #showdown
    def showdown(self, players):
        s = Showdown(self.community_cards, players)
        winner = players[s.winner()]
        winner.bankroll += self.pot
        print(f"winner: {winner.name}")
        self.gameover()
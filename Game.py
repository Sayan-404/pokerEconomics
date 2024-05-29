from Deck import Deck
from Showdown import Showdown
import sys
import os
from tqdm import tqdm


# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__
class Game:
    def __init__(self, players, logger, simul = False):
        self.deck = Deck()
        self.deck.shuffle()
        self.pot = 0
        self.players = players
        self.number_of_players = len(players)
        self.community_cards = []
        self.simul = simul
        self.round = 0
        self.logger = logger
        self.hand_number = 0
        # rounds are 0-indexed starting with pre-flop
        # counts the number of players currently in a game [later gets flushed]
        self.playing = len(players)

    def package_state(self, player_index, call_value = -1): # -1 call values indicate no bets being placed before this
        player = self.players[player_index]
        return {
            "player": player.package_state(),
            "call_value": call_value,
            "players_playing": len(self.players),
            "community_cards": self.community_cards,
            "pot": self.pot,
            "round": self.round
            # there should be a position variable indicating the position of the player in the table 
        }

    def flush(self):
        self.deck.flush()
        for player in self.players:
            player.flush()
        self.community_cards = []
        self.round = 0
        self.playing = len(self.players)

    def play(self, number_of_hands = 1):
        if self.simul:
            blockPrint()
            for i in tqdm(range(number_of_hands), desc = "Simulation Progress: "):
                self.hand_number = i
                self.preflop()
                self.flush()
                # rotates the dealer
                self.players = self.players[-1:] + self.players[:-1]
                self.pot = 0
            enablePrint()
        else:
            for i in range(number_of_hands):
                self.hand_number = i
                self.preflop()
                self.flush()
                # rotates the dealer
                self.players = self.players[-1:] + self.players[:-1]
                self.pot = 0

    # increments the pot by the bet amount whenever a player bets'
    def player_bet(self, player, amt):
        self.pot += player.bet(amt - player.betamt)
                        
    def betting(self, players, betsize):
        # the last player where the action finishes
        end = self.playing - 1

        i = 0

        print(f"pot -> {self.pot}", hand_number = self.hand_number)
        while 1:
            player_index = i % len(players)
            player = players[player_index]

            callsize = betsize - player.betamt

            # check if the player is still in the current game 
            if player.ingame == 0:
                i = (i+1) % len(players)
                continue
            
            print(f"{player.name}'s action -> call(c) / check(ch) / bet(b) / raise(r) / fold(f): ", end="", hand_number = self.hand_number)
            if self.simul:
                action, bet = player.decide(self.package_state(player_index))
                print(action, hand_number = self.hand_number)
            else:
                action = input()
                # log input
            
            if action == "c":
                if callsize != 0:
                    self.player_bet(player, betsize)
                else:
                    print("Illegal move", hand_number = self.hand_number)
                    i = (i+len(players)) % len(players)
                    continue
            
            elif action == "ch":
                if callsize == 0:
                    self.player_bet(player, betsize)
                else:
                    print("Illegal move", hand_number = self.hand_number)
                    i = (i+len(players)) % len(players)
                    continue

            elif action == "b":        
                if betsize == 0:
                    print(f"Enter the betsize: ", end="", hand_number = self.hand_number)
                    if self.simul:
                        betsize = bet
                        print(betsize, hand_number = self.hand_number)
                    else:
                        betsize = int(input())
                        # log input
                    betsize += player.betamt
                    self.player_bet(player, betsize)
                    end = (i-1) % len(players)
                else:
                    print("Illegal move", hand_number = self.hand_number)
                    i = (i+len(players)) % len(players)
                    continue

            elif action == "r":
                if betsize > 0:
                    print(f"Enter the raise: ", end="", hand_number = self.hand_number)
                    if self.simul:
                        betsize = bet
                        print(betsize, hand_number = self.hand_number)
                    else:
                        betsize = int(input())
                        # log input
                    betsize += player.betamt
                    self.player_bet(player, betsize)
                    end = (i-1) % len(players) # sets the loop to end on player before this
                else:
                    print("Illegal move", hand_number = self.hand_number)
                    i = (i+len(players)) % len(players)
                    continue

            elif action == "f":
                player.ingame = 0
                self.playing -= 1
                if self.playing == 1:
                    winner = ""
                    for player in players:
                        if player.ingame == 1:
                            winner = player.id
                            player.bankroll += self.pot
                    self.gameover(winner)
                    return 0
                if i == end:
                    end=(i-1) % len(players)
                    print(f"end is -> {end}", hand_number = self.hand_number)
                    break
            else:
                print("invalid Input", hand_number = self.hand_number)
                i = (i+len(players)) % len(players)
                continue
            # if there is only one person playing then gameover
            if self.playing == 1:
                for player in players:
                    winner = ""
                    if player.ingame == 1:
                        winner = player.id
                        player.bankroll += self.pot
                self.gameover(winner)
                return 0
            # exit condtion for the loop when all the players have called
            if i == end:
                break
            i = (i+1) % len(players)
            
    #handles the preflop action
    def preflop(self):
        print("-------PRE-FLOP------", hand_number = self.hand_number)
        for i in range(self.number_of_players):
            self.players[i].receive_card(self.deck.deal_card())
            self.players[i].receive_card(self.deck.deal_card())

        bet_size = 2

        #blinds 
        if len(self.players) > 2:
            self.player_bet(self.players[1%len(self.players)], 1)
            self.player_bet(self.players[2%len(self.players)], 2)
        else:
            self.player_bet(self.players[0], 1)
            self.player_bet(self.players[1], 2)

        print("----BLINDS-----", hand_number = self.hand_number)
        for player in self.players:
            print(f"{player.name}'s blind -> {player.betamt}", hand_number = self.hand_number)


        #printing the cards:
        for i in range(self.number_of_players):
            print(f"{self.players[i].name}'s cards", hand_number = self.hand_number)
            for card in self.players[i].hand:
                print(card, end=" ", hand_number = self.hand_number)
            print("", hand_number = self.hand_number)

        if self.betting(self.players, bet_size) != 0:
            self.flop()

    def flop(self):
        print("-------FLOP------", hand_number = self.hand_number)
        self.round = 1
        bet_size = 0
        #resetting the betamts
        for player in self.players:
            player.betamt=0

        #displaying the flop
        for _ in range(3):
            self.community_cards.append(str(self.deck.deal_card()))
        
        print(self.community_cards, hand_number = self.hand_number) 

        if self.betting(self.players, bet_size) != 0:
            self.turn()

    def turn(self):
        print("-------TURN------", hand_number = self.hand_number)
        self.round = 2
        bet_size = 0
        #resetting the betamts
        for player in self.players:
            player.betamt=0

        self.community_cards.append(str(self.deck.deal_card()))
        
        print(self.community_cards, hand_number = self.hand_number)

        if self.betting(self.players, bet_size) != 0:
            self.river()

    def river(self):
        print("-------RIVER------", hand_number = self.hand_number)
        self.round = 3
        bet_size = 0
        
        #resetting the betamts
        for player in self.players:
            player.betamt=0

        self.community_cards.append(str(self.deck.deal_card()))
        
        print(self.community_cards, hand_number = self.hand_number)

        if self.betting(self.players, bet_size) != 0:
            self.showdown(self.players)

     #displays info at the end of a hand
    def gameover(self, winner):
        print(f"winner: {winner.name}", hand_number = self.hand_number)
        print("Hand Ended", hand_number = self.hand_number)
        bankrolls = {players.id: players.bankroll for players in self.players}
        bankrolls = dict(sorted(bankrolls.items()))
        # sorting is important since order changes after every round but logger should have consistently ordered columns in the csv
        for id in bankrolls:
            print(f'{id} stack: {bankrolls[id]}', hand_number = self.hand_number)
        log_data = {
            "hand_no": self.hand_number,
            "winner": winner,
            "round": self.round,
            "bankrolls": []
        }
        for id in bankrolls:
            log_data["bankrolls"].append(bankrolls[id])
        self.logger.log_result(log_data)
    
    #showdown
    def showdown(self, players):
        s = Showdown(self.community_cards, players)
        winner = players[s.winner()]
        winner.bankroll += self.pot
        self.gameover(winner.name)
from Deck import Deck
from Showdown import Showdown
import sys
import os
from tqdm import tqdm


# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, "w")


# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__


class Game:
    def __init__(
        self, players, logger, number_of_hands=1, simul=False, seed=None, id=0
    ):
        self.id = id
        self.deck = Deck(seed)
        self.deck.shuffle()
        self.pot = 0
        self.players = players
        self.number_of_players = len(players)
        self.community_cards = []
        self.simul = simul
        self.round = 0
        self.logger = logger
        self.hand_number = 0
        self.all_in = 0
        self.number_of_hands = number_of_hands
        # rounds are 0-indexed starting with pre-flop
        # counts the number of players currently in a game [later gets flushed]
        self.playing = len(players)
        logger.log_config(players, number_of_hands, self.deck.seed)

    def get_max_bet(self, player_index):
        current_player = self.players[player_index]
        max_bet = 0
        for i in range(len(self.players)):
            player = self.players[i]
            if player.ingame and i != player_index:
                max_bet = max(max_bet, player.bankroll)
        max_bet = min(max_bet, current_player.bankroll)
        return max_bet

    def package_state(
        self, player_index, call_value=0
    ):  # 0 call values indicate no bets being placed before this
        player = self.players[player_index]
        return {
            "player": player.package_state(),
            "call_value": call_value,
            "players_playing": len(self.players),
            "players": self.players,
            "community_cards": self.community_cards,
            "pot": self.pot,
            "round": self.round,
            "max_bet": self.get_max_bet(player_index),
            # there should be a position variable indicating the position of the player in the table
        }

    def flush(self):
        self.deck.flush()
        for player in self.players:
            player.flush()
        self.community_cards = []
        self.round = 0
        self.playing = len(self.players)
        self.all_in = 0

    def sub_play(self, i):
        """
        Takes hand_number as input and determines whether game ended or not.\n
        Returns 0 if game ended else returns 1.
        """

        self.hand_number = i

        # Determining the number of players available to play
        count = len(self.players)
        for player in self.players:
            if player.bankroll == 0:
                count -= 1

        # Exit the game and return 0 if a winner emerges
        if count == 1:
            print("Insufficient players", hand_number=self.hand_number)
            return 0

        # Keep a track of all the players' bankroll and proceed to preflop
        bankrolls = {player.id: player.bankroll for player in self.players}
        for id in bankrolls:
            print(f"{id}: {bankrolls[id]}", hand_number=self.hand_number)
        self.preflop()

        # Flush and rotate dealer after preflop
        self.flush()
        self.players = self.players[-1:] + self.players[:-1]
        self.pot = 0
        return 1

    def play(self, benchmark=False):
        if benchmark and self.simul:
            blockPrint()
            for i in range(self.number_of_hands):
                if not self.sub_play(i):
                    break
            enablePrint()
        elif self.simul:
            blockPrint()
            for i in tqdm(
                range(self.number_of_hands),
                desc=f"Simulation ##{self.id}: ",
                position=self.id,
            ):
                if not self.sub_play(i):
                    break
            enablePrint()
        else:
            for i in range(self.number_of_hands):
                if not self.sub_play(i):
                    break

    def player_bet(self, player, amt):
        """
        Increments the pot by the bet amount whenever a player bets.\n
        Takes the player object and bet amount as input.
        """

        if player in self.players:
            returnValue = player.bet(amt)

            if returnValue == False:
                return False

            self.pot += returnValue

    def check_stack(self, betsize):
        for j in range(len(self.players)):
            if self.players[j].ingame == 1:
                if betsize > self.players[j].bankroll:
                    print("Effective Stack size exceeded", hand_number=self.hand_number)
                    return 0
        return 1

    def check_betsize(self, betsize, callsize):
        while 1:
            if betsize <= callsize:
                betsize = int(
                    input(
                        "Bet-size cannot be more than or equal to call-size try again:"
                    )
                )
            else:
                return betsize

    def betting(self, players, betsize=0):
        # the last player where the action finishes
        end = self.playing - 1

        i = 0

        while 1:
            print(f"pot -> {self.pot}", hand_number=self.hand_number)
            print(f"playing: {self.playing}", hand_number=self.hand_number)
            print(f"all_in : {self.all_in}", hand_number=self.hand_number)

            player_index = i % len(players)
            player = players[player_index]
            print(
                f"{player.id}'s bankroll : {player.bankroll}",
                hand_number=self.hand_number,
            )
            callsize = betsize - player.betamt
            print(f"player bet amount: {player.betamt}", hand_number=self.hand_number)
            print(f"call size : {callsize}", hand_number=self.hand_number)
            # check if the player is still in the current game
            if player.ingame == 0:
                i = (i + 1) % len(players)
                continue
            if player.bankroll == 0:
                if self.all_in >= self.playing - 1:
                    break
                i = (i + 1) % len(players)
                continue

            print(
                f"{player.id}'s action -> call(c) / check(ch) / bet(b) / raise(r) / fold(f) / all in(a): ",
                end="",
                hand_number=self.hand_number,
            )
            if self.simul:
                action, bet = player.decide(
                    self.package_state(player_index, call_value=callsize)
                )
                print(action, hand_number=self.hand_number)
            else:
                action = input()
                # log input

            if action == "c":
                if callsize != 0:
                    if player.bankroll <= callsize:
                        self.player_bet(player, player.bankroll)
                        self.all_in += 1
                    else:
                        self.player_bet(player, callsize)
                else:
                    print("Illegal move", hand_number=self.hand_number)
                    i = (i + len(players)) % len(players)
                    continue

            elif action == "ch":
                if callsize == 0:
                    self.player_bet(player, betsize)
                else:
                    print("Illegal move", hand_number=self.hand_number)
                    i = (i + len(players)) % len(players)
                    continue

            elif action == "b":
                if player.betamt == 0:
                    print(f"Enter the bet: ", end="", hand_number=self.hand_number)

                    if not self.simul:
                        bet = int(input())

                    if bet <= 0:
                        print("Bet size cannot be less than or equal to zero")
                        i = (i + len(players)) % len(players)
                        continue

                    print(bet, hand_number=self.hand_number)
                    if player.bankroll <= bet:
                        bet = player.bankroll
                        self.all_in += 1
                    if self.check_stack(bet - callsize) == 0:
                        i = (i + len(players)) % len(players)
                        continue

                        # log input
                    betsize = bet + player.betamt
                    self.player_bet(player, bet)

                    print(f"betsize -> {betsize}", hand_number=self.hand_number)
                    end = (i - 1) % len(
                        players
                    )  # sets the loop to end on player before this
                else:
                    print("Illegal move", hand_number=self.hand_number)
                    i = (i + len(players)) % len(players)
                    continue

            elif action == "r":
                if betsize > 0:
                    print(f"Enter the raise: ", end="", hand_number=self.hand_number)

                    if not self.simul:
                        bet = int(input())

                    if bet <= 0:
                        print("Raise size cannot be less than or equal to zero")
                        i = (i + len(players)) % len(players)
                        continue
                    print(bet, hand_number=self.hand_number)

                    if player.bankroll <= bet:
                        bet = player.bankroll
                        self.all_in += 1
                    if self.check_stack(bet - callsize) == 0:
                        i = (i + len(players)) % len(players)
                        continue
                        # log input
                    betsize = bet + player.betamt
                    self.player_bet(player, bet)

                    print(f"betsize -> {betsize}", hand_number=self.hand_number)
                    end = (i - 1) % len(
                        players
                    )  # sets the loop to end on player before this
                else:
                    print("Illegal move", hand_number=self.hand_number)
                    i = (i + len(players)) % len(players)
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
                    end = (i - 1) % len(players)
                    print(f"end is -> {end}", hand_number=self.hand_number)
                    break

            elif action == "a":
                bet = player.bankroll
                betsize = bet + player.betamt
                print(f"betamt -> {bet}", hand_number=self.hand_number)
                self.all_in += 1
                self.player_bet(player, bet)
                end = (i - 1) % len(players)

            else:
                print("invalid Input", hand_number=self.hand_number)
                i = (i + len(players)) % len(players)
                continue
            # if there is only one person playing then gameover
            if self.playing == 1:
                winner = ""
                for player in players:
                    if player.ingame == 1:
                        winner = player.id
                        player.bankroll += self.pot
                self.gameover(winner)
                return 0
            # exit condtion for the loop when all the players have called
            if i == end:
                break
            i = (i + 1) % len(players)

    # handles the preflop action
    def preflop(self):
        for player in self.players:
            if player.bankroll == 0:
                player.ingame = 0

        print("-------PRE-FLOP------", hand_number=self.hand_number)
        for i in range(self.number_of_players):
            self.players[i].receive_card(self.deck.deal_card())
            self.players[i].receive_card(self.deck.deal_card())

        bet_size = 2

        # blinds
        bb_player = self.players[1]
        sb_player = self.players[0]
        sb_amt = min(1, sb_player.bankroll)
        bb_amt = min(2*sb_amt, bb_player.bankroll)
        if sb_player.bankroll == sb_amt:
            self.all_in += 1
        if bb_player.bankroll == bb_amt:
            self.all_in += 1
        self.player_bet(bb_player, bb_amt)
        self.player_bet(sb_player, sb_amt)


        print("----BLINDS-----", hand_number=self.hand_number)
        for player in self.players:
            print(
                f"{player.id}'s blind -> {player.betamt}", hand_number=self.hand_number
            )

        # printing the cards:
        for i in range(self.number_of_players):
            print(f"{self.players[i].id}'s cards", hand_number=self.hand_number)
            for card in self.players[i].hand:
                print(card, end=" ", hand_number=self.hand_number)
            print("", hand_number=self.hand_number)

        if self.betting(self.players, bet_size) != 0:
            self.flop()

    def flop(self):
        print("-------FLOP------", hand_number=self.hand_number)
        self.round = 1
        # resetting the betamts
        for player in self.players:
            player.betamt = 0

        # displaying the flop
        for _ in range(3):
            self.community_cards.append(str(self.deck.deal_card()))

        print(self.community_cards, hand_number=self.hand_number)

        if self.all_in >= self.playing - 1:
            self.turn()
        else:
            if self.betting(self.players) != 0:
                self.turn()

    def turn(self):
        print("-------TURN------", hand_number=self.hand_number)
        self.round = 2
        # resetting the betamts
        for player in self.players:
            player.betamt = 0

        self.community_cards.append(str(self.deck.deal_card()))

        print(self.community_cards, hand_number=self.hand_number)

        if self.all_in >= self.playing - 1:
            self.river()
        else:
            if self.betting(self.players) != 0:
                self.river()

    def river(self):
        print("-------RIVER------", hand_number=self.hand_number)
        self.round = 3

        # resetting the betamts
        for player in self.players:
            player.betamt = 0

        self.community_cards.append(str(self.deck.deal_card()))

        print(self.community_cards, hand_number=self.hand_number)
        if self.all_in >= self.playing - 1:
            self.showdown(self.players)
        else:
            if self.betting(self.players) != 0:
                self.showdown(self.players)

    # displays info at the end of a hand
    def gameover(self, winner):
        print(f"winner: {winner}", hand_number=self.hand_number)
        print("Hand Ended", hand_number=self.hand_number)
        bankrolls = {player.id: player.bankroll for player in self.players}
        bankrolls = dict(sorted(bankrolls.items()))
        # sorting is important since order changes after every round but logger should have consistently ordered columns in the csv
        log_data = {
            "hand_no": self.hand_number,
            "winner": winner,
            "round": self.round,
            "bankrolls": [],
        }
        for id in bankrolls:
            print(f"{id} stack: {bankrolls[id]}", hand_number=self.hand_number)
            log_data["bankrolls"].append(bankrolls[id])
        self.logger.log_result(log_data)

    # showdown
    def showdown(self, players):
        s = Showdown(self.community_cards, players)
        winner = players[s.winner()]
        winner.bankroll += self.pot
        self.gameover(winner.id)

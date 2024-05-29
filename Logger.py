# config.txt
# 	- player configs
# 	- number of games
# 	- simulation starting time
# hand*.txt
# 	- print statement logs
# games.csv
# 	- each row corresponds to one hand
# 	- columns: bankroll at the end of the hand for each player, winner of the hand, round the hand ended on
# 	- first row does not refer to any hand, it gives the: initial bankrolls of the players, null winner and -1 as hand ending round

import os
import datetime
import time
import json
import builtins
import csv

class Logger:
    def __init__(self):
        folder = f"{datetime.date.today()}_{str(time.time())}"
        self.path = f"{os.path.abspath(os.getcwd())}/data/{folder}"
        os.makedirs(self.path)
        self.config_file = f"{self.path}/config.txt"
        self.hand_file = f"{self.path}/hand_"
        self.games_file = f"{self.path}/games.csv"
        original_print = builtins.print
        def custom_print(*args, **kwargs):
            hand_number = -1
            if kwargs["hand_number"]:
                hand_number = kwargs.pop("hand_number", "")
            original_print(*args)
            self.log_hand(*args, hand_number = hand_number)
        builtins.print = custom_print

    def log_config(self, players, num):
        with open(self.config_file, "w") as f:
            for player in players:
                f.write(json.dumps(player.package_state(), indent=4))
            f.write(f"Number of hands: {num}")
            f.write(f"Simulation starting time: {datetime.datetime.now()}")
        # initiating games csv
        with open(self.games_file, "w", newline='') as f:
            writer = csv.writer(f)
            row = ["hand_no"] + [p.package_state()["id"] for p in players] + ["winner", "ending_round"]
            writer.writerow(row)
            row = [0] + [p.package_state()["bankroll"] for p in players] + ["", -1]
            writer.writerow(row)

    def log_hand(self, data, hand_number):
        if hand_number == -1:
            return
        with open(f"{self.hand_file}{hand_number}.txt", "a") as f:
            f.write(f"{data}\n")
        
    def log_result(self, data):
        with open(self.games_file, "a", newline="") as f:
            writer = csv.writer(f)
            row = [data["hand_no"]] + [p for p in data["bankrolls"]] + [data["winner"], data["round"]]
            writer.writerow(row)

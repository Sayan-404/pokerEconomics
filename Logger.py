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
import uuid
import hashlib

class Logger:
    def __init__(self, log_hands = False, benchmark = False, strategies = [], number_of_hands = 0):
        name = ""
        for strat in strategies:
            name += f"{strat}_"
        if benchmark:
            folder = f"b_{name}{number_of_hands}_{self.create_hash()}"
        else:
            folder = f"r_{name}{number_of_hands}_{self.create_hash()}"
        self.path = f"{os.path.abspath(os.getcwd())}/data/{folder}"
        os.makedirs(self.path)
        self.config_file = f"{self.path}/config.json"
        self.hand_file = f"{self.path}/hand_"
        self.games_file = f"{self.path}/games.csv"
        self.log_hands = log_hands
        original_print = builtins.print
        def custom_print(*args, **kwargs):
            hand_number = -1
            if "hand_number" in kwargs:
                hand_number = kwargs.pop("hand_number", "")
            original_print(*args)
            self.log_hand(*args, hand_number = hand_number)
        builtins.print = custom_print

    def create_hash(self):
        current_time = time.time()
        uid = uuid.uuid4()
        identifier_string = f"{current_time}_{uid}"
        digest = hashlib.md5(identifier_string.encode()).hexdigest()
        return digest


    def log_config(self, players, num, seed):
        config_data = {
            "players": {}
        }
        for i in range(len(players)):
            player_data = players[i].package_state()
            del player_data["hand"]
            del player_data["ingame"]
            del player_data["betamt"]
            config_data["players"][i] = player_data
        config_data["number_of_hands"] = num
        config_data["date"] = str(datetime.date.today())
        config_data["time"] = str(datetime.datetime.now())
        config_data["seed"] = seed
        print(config_data)
        with open(self.config_file, "w") as f:
            json.dump(config_data, f, indent=4)
        # initiating games csv
        with open(self.games_file, "w", newline='') as f:
            writer = csv.writer(f)
            row = ["hand_no"] + [p.package_state()["id"]+"("+p.package_state()["strategy"]+")" for p in players] + ["winner", "ending_round"]
            writer.writerow(row)
            row = [0] + [p.package_state()["bankroll"] for p in players] + ["", -1]
            writer.writerow(row)

    def log_hand(self, data, hand_number):
        if not self.log_hands:
            return
        if hand_number == -1:
            return
        with open(f"{self.hand_file}{hand_number}.txt", "a") as f:
            f.write(f"{data}\n")
        
    def log_result(self, data):
        with open(self.games_file, "a", newline="") as f:
            writer = csv.writer(f)
            row = [data["hand_no"] + 1]  + [p for p in data["bankrolls"]] + [data["winner"], data["round"]]
            writer.writerow(row)

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

# import builtins
import csv
import datetime
import hashlib
import json
import os
import time
import uuid
import inspect

class Logger:

    def __init__(self, log_hands = False, benchmark = False, strategies = [], number_of_hands = 0, simul = False):
        name = ""
        for strat in strategies:
            name += f"{strat}_"
        if benchmark:
            folder = f"b_{name}{number_of_hands}_{self.create_hash()}"
        else:
            folder = f"r_{name}{number_of_hands}_{self.create_hash()}"
        self.path = f"{os.path.abspath(os.getcwd())}/data/{folder}"
        os.makedirs(self.path)
        self.config_file = open(f"{self.path}/config.json", "w")

        if log_hands:
            self.hand_file = open(f"{self.path}/hand_0.json", "a")

        # log.txt logs print statements in cases where print is blocked and log_hands is on
        # helps in debugging
        # to print selectively, change the file parameter to any string
        # this helps in isolated debugging prints

        if simul and log_hands:
            self.misc_log_file = open(f"{self.path}/log.txt", "a")
            self.selective_misc_log_file = open(f"{self.path}/selective_log.txt", "a")
            def _misc_log(*args, sep=' ', end='\n', file=self.misc_log_file, flush=False):
                if type(file) == str:
                    file = self.selective_misc_log_file
                current_frame = inspect.currentframe()
                caller_frame = inspect.getouterframes(current_frame, 2)[1]
                caller_function_name = caller_frame.function
                caller_module = inspect.getmodule(caller_frame.frame)
                caller_module_name = caller_module.__name__ if caller_module else None
                prefix = f"[LOG@{caller_module_name}.{caller_function_name} {time.strftime('%D %H:%M:%S', time.localtime())}]"
                print(prefix, *args, sep=sep, end=end, file=file, flush=flush)
            self.print = _misc_log
        else:
            self.print = print

        self.current_hand_data = {
            "blinds": {
                "bankrolls": {},
                "blinds": {}
            },
            "pre-flop": {
                "bankrolls": {},
                "cards": {},
                "betting": []
            },
            "flop": {
                "bankrolls": {},
                "community_cards": [],
                "betting": []
            },
            "turn": {
                "bankrolls": {},
                "community_cards": [],
                "betting": []
            },
            "river": {
                "bankrolls": {},
                "community_cards": [],
                "betting": []
            },
            "gameover": {
                "winner" : "",
                "round" : 0,
                "bankrolls": {}
            }
        }
        self.games_file = open(f"{self.path}/games.csv", "a")
        self.log_hands = log_hands
        self.total_num_hands = number_of_hands

    def close_files(self):
        self.config_file.close()
        self.games_file.close()
        if self.log_hands:
            self.hand_file.close()

    def handle_hand_file(self, i):
        if not self.log_hands:
            return
        self.hand_file.close()
        self.current_hand_data = {
            "blinds": {
                "bankrolls": {},
                "blinds": {}
            },
            "pre-flop": {
                "bankrolls": {},
                "cards": {},
                "betting": []
            },
            "flop": {
                "bankrolls": {},
                "community_cards": [],
                "betting": []
            },
            "turn": {
                "bankrolls": {},
                "community_cards": [],
                "betting": []
            },
            "river": {
                "bankrolls": {},
                "community_cards": [],
                "betting": []
            },
            "gameover": {
                "winner" : "",
                "round" : 0,
                "bankrolls": {}
            }
        }
        self.hand_file = open(f"{self.path}/hand_{i}.json", "a")

    def create_hash(self):
        current_time = time.time()
        uid = uuid.uuid4()
        identifier_string = f"{current_time}_{uid}"
        digest = hashlib.md5(identifier_string.encode()).hexdigest()
        return digest

    def log_error(self, err):
        filename = f"{self.path}/error.txt"
        with open(filename, "w") as f:
            f.write(err)

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
        json.dump(config_data, self.config_file, indent=4)
        # initiating games csv
        writer = csv.writer(self.games_file)
        row = ["hand_no"] + [str(p.package_state()["id"])+"("+p.package_state()["strategy"]+")" for p in players] + [str(p.package_state()["id"])+"(AF)" for p in players] + ["winner", "ending_round"]
        writer.writerow(row)
        row = [0] + [p.package_state()["bankroll"] for p in players] + ["", "", -1]
        writer.writerow(row)

    def log_hand(self):
        if not self.log_hands:
            return
        if self.hand_file.closed:
            return
        json.dump(self.current_hand_data, self.hand_file, indent=4)

    def log_result(self, data):
        writer = csv.writer(self.games_file)

        row = [data["hand_no"] + 1]  + [p for p in data["bankrolls"]] + [p for p in data['tendency']] + [data["winner"], data["round"]]
        writer.writerow(row)

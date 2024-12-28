import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

def plot(file_path):
    # Check for the data directory
    data_path = file_path
    if not os.path.isdir(data_path):
        print(f"No data directory found in {data_path}")
        return

    # Iterate over all directories in the data directory
    for i in tqdm(range(0, len(os.listdir(data_path)))):
        subdir = os.listdir(data_path)[i]
        subdir_path = os.path.join(data_path, subdir)
        if os.path.isdir(subdir_path):
            csv_file = os.path.join(subdir_path, 'games.csv')
            if not os.path.isfile(csv_file):
                print(f"No games.csv found in {subdir_path}")
                continue

            try:
                # Load the CSV data
                df = pd.read_csv(csv_file)

                x = df["hand_no"]

                # Extract players and standardise scores
                players = [name for index, name in enumerate(
                    df.columns) if 0 < index < len(df.columns) - 4]
                for i in range(2):
                    df[players[i]] -= df[players[i]][0]

                # Extract tendency index
                tendency_index_keys = [name for index, name in enumerate(
                    df.columns) if 2 < index < len(df.columns) - 2]
                tendency_index = [df[i].iloc[-1] for i in tendency_index_keys]

                # Plot the smooth curves
                plt.figure(figsize=(10, 5))
                plt.plot(x, df[players[0]], label=f"{players[0]} {tendency_index[0]}", linestyle="dotted")
                plt.plot(x, df[players[1]], label=f"{players[1]} {tendency_index[1]}")
                plt.title("Scores Over Rounds")
                plt.xlabel("Hand Number")
                plt.ylabel("Scores")
                plt.legend()
                plt.grid(True)
                plt.savefig(f"{subdir_path}/_analysis.png")

                # Optionally, show the plot
                # plt.show()
            except Exception as e:
                print(e)
                continue


def show_hand(file_path):
    game_data_dir = input("input game data directory name: ")
    file_path = os.path.join(file_path, game_data_dir)
    if not os.path.isfile(f"{file_path}hand_0.json"):
        print("hands are not logged (hand_0 not found)")
        return
    while (1):
        hand = input("enter hand number (-1 to exit): ")
        if hand == "-1":
            break
        hand = f"{file_path}hand_{hand}.json"
        if not os.path.isfile(hand):
            print("hand not logged")
            continue
        with open(hand) as f:
            print(f.read())


# Set up command line argument parsing
parser = argparse.ArgumentParser(description="Analyser")
parser.add_argument(
    "file_path", type=str, help="path to the folder containing game data folder(s)"
)
parser.add_argument(
    "--plot", help="plot bankrolls in game data folder", action=argparse.BooleanOptionalAction
)
parser.add_argument(
    "--show_hand", help="prints individual hand details if present", action=argparse.BooleanOptionalAction
)
args = parser.parse_args()

if args.plot:
    plot(args.file_path)
if args.show_hand:
    show_hand(args.file_path)

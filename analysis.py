import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import argparse
import os

def plot(file_path):

    # Load the CSV data
    df = pd.read_csv(f"{file_path}/games.csv")

    # Interpolate data to create smooth curves
    x = df["hand_no"]
    x_new = np.linspace(
        x.min(), x.max(), 10000
    )  # Increase the number of points for smoothness

    players = [name for index, name in enumerate(df.columns) if 0 < index < len(df.columns) - 2]

    # Create smooth curves for Sayan and Sourjya
    spl_sayan = make_interp_spline(x, df[players[0]], k=3)
    spl_sourjya = make_interp_spline(x, df[players[1]], k=3)

    y_sayan_smooth = spl_sayan(x_new)
    y_sourjya_smooth = spl_sourjya(x_new)

    # Plot the smooth curves
    plt.figure(figsize=(10, 5))
    plt.plot(x_new, y_sayan_smooth, label=players[0])
    plt.plot(x_new, y_sourjya_smooth, label=players[1])
    plt.title("Scores Over Rounds")
    plt.xlabel("Hand Number")
    plt.ylabel("Scores")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{file_path}/analysis.png")

    # Optionally, show the plot
    plt.show()

def show_hand(file_path):
    if not os.path.isfile(f"{file_path}/hand_0.txt"):
        print("hands are not logged (hand_0 not found)")
        return
    while(1):
        hand = input("enter hand number (-1 to exit): ")
        if hand == "-1":
            break
        hand = f"{file_path}/hand_{hand}.txt"
        if not os.path.isfile(hand):
            print("hand not logged")
            continue
        with open(hand) as f:
            print(f.read())

# Set up command line argument parsing
parser = argparse.ArgumentParser(description="Analyser")
parser.add_argument(
    "file_path", type=str, help="path to the CSV file containing the game data"
)
parser.add_argument(
    "--plot", help="plot bankrolls", action=argparse.BooleanOptionalAction
)
parser.add_argument(
    "--show_hand", help="prints individual hand details if present", action=argparse.BooleanOptionalAction
)
args = parser.parse_args()

if args.plot:
    plot(args.file_path)
if args.show_hand:
    show_hand(args.file_path)
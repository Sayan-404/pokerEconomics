import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import argparse

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
    plt.savefig("analysis.png")

    # Optionally, show the plot
    plt.show()


# Set up command line argument parsing
parser = argparse.ArgumentParser(description="Analyser")
parser.add_argument(
    "file_path", type=str, help="Path to the CSV file containing the game data"
)
parser.add_argument(
    "--plot", help="Plot bankrolls", action=argparse.BooleanOptionalAction
)
args = parser.parse_args()

if args.plot:
    plot(args.file_path)
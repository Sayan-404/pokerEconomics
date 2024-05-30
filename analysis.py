import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Load the CSV data
file_path = "games.csv"  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Interpolate data to create smooth curves
x = df["hand_no"]
x_new = np.linspace(
    x.min(), x.max(), 10000
)  # Increase the number of points for smoothness

# Create smooth curves for Sayan and Sourjya
spl_sayan = make_interp_spline(x, df["Sayan"], k=3)
spl_sourjya = make_interp_spline(x, df["Sourjya"], k=3)

y_sayan_smooth = spl_sayan(x_new)
y_sourjya_smooth = spl_sourjya(x_new)

# Plot the smooth curves
plt.figure(figsize=(10, 5))
plt.plot(df["hand_no"], df["Sayan"], label="Sayan")
plt.plot(df["hand_no"], df["Sourjya"], label="Sourjya")
plt.title("Scores Over Rounds")
plt.xlabel("Hand Number")
plt.ylabel("Scores")
plt.legend()
plt.grid(True)
plt.savefig("analysis.png")

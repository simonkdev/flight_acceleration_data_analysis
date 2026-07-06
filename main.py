SMOOTHING_INCREMENT = 5

from time import time

from termcolor import colored

def printInit(msg):
    print(colored("[ INIT ]", "green"), msg)

def printSection(msg):
    print(colored("[ SECTION ]", "blue", attrs=["bold"]), colored(msg, "white", attrs=["bold"]))

def printInfo(msg):
    print(colored("[ INFO ] " + msg, "magenta"))

def printStatus(msg):
    print(colored("[ STAT ] ", "cyan"), msg)

printSection("Initialization")
printInit("Importing libraries...")
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from rich.progress import Progress
printInit("Library imports completed.")

printInit("Loading data...")
df = pd.read_csv("plane_landing.csv")
printInit("Data loaded successfully.")

printInfo("Seaborn version: " + sns.__version__)
printInit("Setting up Seaborn...")
sns.set_theme()
printInit("Seaborn set up successfully.")

printSection("Visualization")
printStatus("Creating noisy scatter plots...")

fig, axes = plt.subplots(1,4, figsize=(15, 4), sharex=True)

sns.scatterplot(data=df, x="time", y="acc_x", ax=axes[0])
axes[0].set_title("X acceleration")

sns.scatterplot(data=df, x="time", y="acc_y", ax=axes[1])
axes[1].set_title("Y acceleration")

sns.scatterplot(data=df, x="time", y="acc_z", ax=axes[2])
axes[2].set_title("Z acceleration")

sns.scatterplot(data=df, x="time", y="absolute_acc", ax=axes[3])
axes[3].set_title("Absolute acceleration")

for ax in axes:
    ax.set_xlabel("Time")
    ax.set_ylabel("Acceleration")

plt.tight_layout()
printStatus("Saving noisy scatter plots...")
plt.savefig("acceleration_scatterplots.png", dpi=300, bbox_inches="tight")
printStatus("Noisy plots saved.")

printSection("Smoothing")

printStatus("Preparing smoothing...")
arr = np.array([])
time_arr = np.array([])
tracker = 0

rows = len(df)
steps = rows // SMOOTHING_INCREMENT

with Progress() as p:
    t = p.add_task(colored("[ STAT ]  ", "cyan") + "Calculating smoothed values...", total=steps)
    while not p.finished:
        p.update(t, advance=1)
        if tracker + SMOOTHING_INCREMENT > rows:
            mean_of_15 = df["acc_x"].iloc[tracker:].mean()
            time_mean = df["time"].iloc[tracker:].mean()
        else:
            mean_of_15 = df["acc_x"].iloc[tracker:tracker+SMOOTHING_INCREMENT].mean()
            time_mean = df["time"].iloc[tracker:tracker+SMOOTHING_INCREMENT].mean()

        arr = np.append(arr, mean_of_15)
        time_arr = np.append(time_arr, time_mean)
        tracker += SMOOTHING_INCREMENT

smoothed_df = pd.DataFrame({"time": time_arr, "acc_x": arr})

smoothed_df.to_csv("smoothed_df.csv", index=False)

plt.figure(figsize=(8, 4))

sns.lineplot(data=smoothed_df, x="time", y="acc_x")
plt.title("Smoothed acceleration")
plt.xlabel("Time")
plt.ylabel("Acceleration")
plt.tight_layout()
printStatus("Saving smoothed plot...")
plt.savefig("smoothed_acceleration.png", dpi=300, bbox_inches="tight")
printStatus("Smoothed plot saved.")
plt.show()

ROLLING_WINDOW = 12
IMAGES_DIR = "images/"
CSV_DIR = "tables/"

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
df = pd.read_csv(CSV_DIR + "plane_landing.csv")
printInit("Data loaded successfully.")

printInfo("Seaborn version: " + sns.__version__)
printInit("Setting up Seaborn...")
sns.set_theme()

def grid_plot_one_row(dataframe, linePlot = False):
    fig, axes = plt.subplots(1,4, figsize=(15, 4), sharex=True)

    if linePlot:
        sns.lineplot(data=dataframe, x="time", y="acc_x", ax=axes[0])
    else:
        sns.scatterplot(data=dataframe, x="time", y="acc_x", ax=axes[0])
    axes[0].set_title("X acceleration")

    if linePlot:
        sns.lineplot(data=dataframe, x="time", y="acc_y", ax=axes[1])
    else:
        sns.scatterplot(data=dataframe, x="time", y="acc_y", ax=axes[1])
    axes[1].set_title("Y acceleration")

    if linePlot:
        sns.lineplot(data=dataframe, x="time", y="acc_z", ax=axes[2])
    else:
        sns.scatterplot(data=dataframe, x="time", y="acc_z", ax=axes[2])
    axes[2].set_title("Z acceleration")

    if linePlot:
        sns.lineplot(data=dataframe, x="time", y="absolute_acc", ax=axes[3])
    else:
        sns.scatterplot(data=dataframe, x="time", y="absolute_acc", ax=axes[3])
    axes[3].set_title("Absolute acceleration")

    for ax in axes:
        ax.set_xlabel("Time")
        ax.set_ylabel("Acceleration")

    plt.tight_layout()

printInit("Seaborn set up successfully.")

printSection("Visualization")

printStatus("Creating noisy scatter plots...")

grid_plot_one_row(df, True)

printStatus("Saving noisy scatter plots...")

plt.savefig(IMAGES_DIR + "acceleration_scatterplots.png", dpi=300, bbox_inches="tight")

printStatus("Noisy plots saved.")

printSection("Smoothing")

def smoothing(df_column, rows):
    arr = np.full(ROLLING_WINDOW, np.nan)
    tracker = ROLLING_WINDOW

    with Progress() as p:
        t = p.add_task(colored("[ STAT ]  ", "cyan") + "Calculating smoothed values...", total=rows-ROLLING_WINDOW)
        while not p.finished:
            p.update(t, advance=1)

            smoothed_value = df_column.iloc[tracker-ROLLING_WINDOW:tracker].mean()


            arr = np.append(arr, smoothed_value)
            tracker += 1

    return arr

printStatus("Preparing smoothing...")
rows = len(df)
time = df["time"]

acc_x, acc_y, acc_z, absolute_acc = df["acc_x"], df["acc_y"], df["acc_z"], df["absolute_acc"]

smoothed_df = pd.DataFrame({"time": time, "acc_x": smoothing(acc_x, rows), "acc_y": smoothing(acc_y, rows), "acc_z": smoothing(acc_z, rows), "absolute_acc": smoothing(absolute_acc, rows)})

smoothed_df.to_csv(CSV_DIR + "smoothed_df.csv", index=False)

printStatus("Creating smoothed plot...")

grid_plot_one_row(smoothed_df, True)

printStatus("Saving smoothed plot...")
plt.savefig(IMAGES_DIR + "smoothed_acceleration.png", dpi=300, bbox_inches="tight")
printStatus("Smoothed plot saved.")
plt.show()

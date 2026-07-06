ROLLING_WINDOW = 12
ZOOM_WINDOW_MIN = 180
ZOOM_WINDOW_MAX = 220
TOUCHDOWN_TIME = 195
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
def grid_plot_two_rows(dataframe1, dataframe2, linePlot=False):
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    columns = ["acc_x", "acc_y", "acc_z", "absolute_acc"]
    titles = ["X acceleration", "Y acceleration", "Z acceleration", "Absolute acceleration"]
    dataframes = [dataframe1, dataframe2]
    row_labels = ["Raw", "Smoothed"]

    plot_func = sns.lineplot if linePlot else sns.scatterplot

    for row_index, dataframe in enumerate(dataframes):
        for col_index, column in enumerate(columns):
            plot_func(data=dataframe, x="time", y=column, ax=axes[row_index, col_index])
            axes[row_index, col_index].set_title(f"{row_labels[row_index]} {titles[col_index]}")

    for ax in axes.flat:
        ax.set_xlim(ZOOM_WINDOW_MIN, ZOOM_WINDOW_MAX)
        ax.axvline(TOUCHDOWN_TIME, color="red", linestyle="--", linewidth=1.5)
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


printStatus("Preparing smoothing...")
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
rows = len(df)
time = df["time"]
acc_x, acc_y, acc_z, absolute_acc = df["acc_x"], df["acc_y"], df["acc_z"], df["absolute_acc"]

printStatus("Smoothing data...")
smoothed_df = pd.DataFrame({"time": time, "acc_x": smoothing(acc_x, rows), "acc_y": smoothing(acc_y, rows), "acc_z": smoothing(acc_z, rows), "absolute_acc": smoothing(absolute_acc, rows)})
printStatus("Smoothing completed.")
smoothed_df.to_csv(CSV_DIR + "smoothed_df.csv", index=False)

printStatus("Creating smoothed plot...")
grid_plot_one_row(smoothed_df, True)
printStatus("Saving smoothed plot...")
plt.savefig(IMAGES_DIR + "smoothed_acceleration.png", dpi=300, bbox_inches="tight")
printStatus("Smoothed plot saved.")

printStatus("Determining touchdown time...")
touchdown_time = smoothed_df[smoothed_df["absolute_acc"] == smoothed_df["absolute_acc"].max()]["time"].values[0]
TOUCHDOWN_TIME = touchdown_time
printStatus(f"Touchdown time: {touchdown_time}")

printStatus("Creating combination plot...")
grid_plot_two_rows(df, smoothed_df, True)
printStatus("Saving combination plot...")
plt.savefig(IMAGES_DIR + "combination_plot.png", dpi=300, bbox_inches="tight")
printStatus("Combination plot saved.")

plt.show()

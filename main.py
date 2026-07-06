ROLLING_WINDOW = 12
ZOOM_WINDOW_MIN = 180
ZOOM_WINDOW_MAX = 220

TOUCHDOWN_TIME = 0
TOUCHDOWN_TIME_RAW = 0
MAX_DYNAMIC_ACCELERATION_MS2 = 0
MAX_DYNAMIC_ACCELERATION_G = 0
ROLLOUT_ROUGHNESS = 0

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

    add_touchdown_markers(axes, zoom=False)

    plt.tight_layout()
def add_touchdown_markers(axes, zoom=True):
    for ax_index, ax in enumerate(axes.flat):
        if zoom:
            ax.set_xlim(ZOOM_WINDOW_MIN, ZOOM_WINDOW_MAX)
        if TOUCHDOWN_TIME_RAW:
            ax.axvline(TOUCHDOWN_TIME_RAW, color="orange", linestyle="--", linewidth=1.5)
            if ax_index == 0:
                ax.text(
                    TOUCHDOWN_TIME_RAW,
                    0.98,
                    "raw touchdown",
                    color="darkorange",
                    fontsize=8,
                    rotation=90,
                    va="top",
                    ha="right",
                    transform=ax.get_xaxis_transform(),
                )
        if TOUCHDOWN_TIME:
            ax.axvline(TOUCHDOWN_TIME, color="red", linestyle="--", linewidth=1.5)
            if ax_index == 0:
                ax.text(
                    TOUCHDOWN_TIME,
                    0.98,
                    "smoothed peak",
                    color="red",
                    fontsize=8,
                    rotation=90,
                    va="top",
                    ha="left",
                    transform=ax.get_xaxis_transform(),
                )
        ax.set_xlabel("Time")
def add_phase_zones(axes):
    touchdown_start = TOUCHDOWN_TIME_RAW - 1
    rollout_start = TOUCHDOWN_TIME + 1
    zones = [
        ("Approach", ZOOM_WINDOW_MIN, touchdown_start, "#4C78A8"),
        ("Touchdown", touchdown_start, rollout_start, "#F58518"),
        ("Rollout", rollout_start, ZOOM_WINDOW_MAX, "#54A24B"),
    ]

    for ax in axes.flat:
        for _, start, end, color in zones:
            ax.axvspan(start, end, color=color, alpha=0.12)

    for col_index, ax in enumerate(axes[0]):
        for label, start, end, color in zones:
            if col_index == 0:
                ax.text(
                    (start + end) / 2,
                    0.03,
                    label,
                    color=color,
                    fontsize=8,
                    ha="center",
                    va="bottom",
                    transform=ax.get_xaxis_transform(),
                )
def grid_plot_raw_and_smoothed(dataframe1, dataframe2, linePlot=False):
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
            axes[row_index, col_index].set_ylabel("Acceleration")

    add_touchdown_markers(axes)

    plt.tight_layout()
def grid_plot_smoothed_and_jerk(smoothed_frame, jerk_frame, linePlot=False):
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    acceleration_columns = ["acc_x", "acc_y", "acc_z", "absolute_acc"]
    jerk_columns = ["acc_x", "acc_y", "acc_z", "acc_abs"]
    titles = ["X", "Y", "Z", "Absolute"]

    plot_func = sns.lineplot if linePlot else sns.scatterplot

    for col_index, column in enumerate(acceleration_columns):
        plot_func(data=smoothed_frame, x="time", y=column, ax=axes[0, col_index])
        axes[0, col_index].set_title(f"Smoothed {titles[col_index]} acceleration")
        axes[0, col_index].set_ylabel("Acceleration")

    for col_index, column in enumerate(jerk_columns):
        plot_func(data=jerk_frame, x="time", y=column, ax=axes[1, col_index])
        axes[1, col_index].set_title(f"{titles[col_index]} jerk")
        axes[1, col_index].set_ylabel("Jerk")

    add_touchdown_markers(axes)

    plt.tight_layout()
def grid_plot_raw_smoothed_and_jerk(raw_frame, smoothed_frame, jerk_frame, linePlot=False):
    fig, axes = plt.subplots(3, 4, figsize=(16, 11))

    acceleration_columns = ["acc_x", "acc_y", "acc_z", "absolute_acc"]
    jerk_columns = ["acc_x", "acc_y", "acc_z", "acc_abs"]
    titles = ["X", "Y", "Z", "Absolute"]
    plot_func = sns.lineplot if linePlot else sns.scatterplot

    for col_index, column in enumerate(acceleration_columns):
        plot_func(data=raw_frame, x="time", y=column, ax=axes[0, col_index])
        axes[0, col_index].set_title(f"Raw {titles[col_index]} acceleration")
        axes[0, col_index].set_ylabel("Acceleration")

        plot_func(data=smoothed_frame, x="time", y=column, ax=axes[1, col_index])
        axes[1, col_index].set_title(f"Smoothed {titles[col_index]} acceleration")
        axes[1, col_index].set_ylabel("Acceleration")

    for col_index, column in enumerate(jerk_columns):
        plot_func(data=jerk_frame, x="time", y=column, ax=axes[2, col_index])
        axes[2, col_index].set_title(f"{titles[col_index]} jerk")
        axes[2, col_index].set_ylabel("Jerk")

    add_phase_zones(axes)
    add_touchdown_markers(axes)

    plt.tight_layout()
printInit("Seaborn set up successfully.")



printSection("Processing")


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



printSection("Analysis")


printStatus("Determining touchdown time...")
touchdown_time = smoothed_df[smoothed_df["absolute_acc"] == smoothed_df["absolute_acc"].max()]["time"].values[0]
TOUCHDOWN_TIME = touchdown_time
touchdown_time_raw = df[df["absolute_acc"] == df["absolute_acc"].max()]["time"].values[0]
TOUCHDOWN_TIME_RAW = touchdown_time_raw
printStatus(f"Touchdown time (raw): {touchdown_time_raw}")
printStatus(f"Touchdown time (after rolling): {touchdown_time}")

printStatus("Determining max acceleration...")
MAX_DYNAMIC_ACCELERATION_MS2 = smoothed_df["absolute_acc"].max()
MAX_DYNAMIC_ACCELERATION_G = MAX_DYNAMIC_ACCELERATION_MS2 / 9.81
printStatus(f"Peak dynamic acceleration: {MAX_DYNAMIC_ACCELERATION_MS2} m/s^2")
printStatus(f"Peak dynamic acceleration in g units: {MAX_DYNAMIC_ACCELERATION_G}")

printStatus("Calculating jerk...")
def calculate_jerk_one_col(df_column, time):
    index = 1
    jerk_values = []
    with Progress() as p:
        t = p.add_task(colored("[ STAT ]  ", "cyan") + "Calculating one jerk column...", total=rows-1)
        while not p.finished:
            p.update(t, advance=1)
            jerk = (df_column.iloc[index- 1] - df_column.iloc[index]) / (time.iloc[index - 1] - time.iloc[index])
            jerk_values.append(jerk)
            index += 1
    return jerk_values
def give_jerk_dataframe(origin_frame):
    acc_x, acc_y, acc_z, time, acc_abs = origin_frame["acc_x"], origin_frame["acc_y"], origin_frame["acc_z"], origin_frame["time"], origin_frame["absolute_acc"]
    jerk_frame = pd.DataFrame({ "time": time.iloc[1:], "acc_x": calculate_jerk_one_col(acc_x, time), "acc_y": calculate_jerk_one_col(acc_y, time), "acc_z": calculate_jerk_one_col(acc_z, time), "acc_abs": calculate_jerk_one_col(acc_abs, time)})
    return jerk_frame
jf = give_jerk_dataframe(smoothed_df)
jf.to_csv(CSV_DIR + "jerkframe.csv", index=False)
printStatus("Jerk finished.")

printStatus("Calculating roughness score...")
def calculate_roughness_score(jerk_frame):
    time_list = jerk_frame["time"].tolist()
    touchdown_index = time_list.index(TOUCHDOWN_TIME)
    jerk_after_touchdown = jerk_frame["acc_abs"].iloc[touchdown_index:]
    roughness_score = np.sqrt((jerk_after_touchdown ** 2).mean())
    return roughness_score
roughness = calculate_roughness_score(jf)
ROLLOUT_ROUGHNESS = roughness
printStatus(f"Roughness score: {roughness}")

printStatus("Calculating grade...")
def calculate_grade(roughness, max_accel, average_jerk):
    grade = 10 - (abs(roughness) / abs(max_accel))*3 - abs(average_jerk)*4
    return grade
grade = calculate_grade(roughness, MAX_DYNAMIC_ACCELERATION_MS2, jf["acc_abs"].mean())
FINAL_LANDING_GRADE = grade
printStatus(f"Grade: {grade}")



printSection("Visualization")


printStatus("Creating noisy scatter plots...")
grid_plot_one_row(df, True)
printStatus("Saving noisy scatter plots...")
plt.savefig(IMAGES_DIR + "acceleration_scatterplots.png", dpi=300, bbox_inches="tight")
printStatus("Noisy plots saved.")

printStatus("Creating smoothed plot...")
grid_plot_one_row(smoothed_df, True)
printStatus("Saving smoothed plot...")
plt.savefig(IMAGES_DIR + "smoothed_acceleration.png", dpi=300, bbox_inches="tight")
printStatus("Smoothed plot saved.")

printStatus("Creating combination plot...")
grid_plot_raw_and_smoothed(df, smoothed_df, True)
printStatus("Saving combination plot...")
plt.savefig(IMAGES_DIR + "combination_plot.png", dpi=300, bbox_inches="tight")
printStatus("Combination plot saved.")

printStatus("Creating smoothed and jerk plot...")
grid_plot_smoothed_and_jerk(smoothed_df, jf, True)
printStatus("Saving smoothed and jerk plot...")
plt.savefig(IMAGES_DIR + "smoothed_and_jerk_plot.png", dpi=300, bbox_inches="tight")
printStatus("Smoothed and jerk plot saved.")

printStatus("Creating raw, smoothed, and jerk plot...")
grid_plot_raw_smoothed_and_jerk(df, smoothed_df, jf, True)
printStatus("Saving raw, smoothed, and jerk plot...")
plt.savefig(IMAGES_DIR + "raw_smoothed_and_jerk_plot.png", dpi=300, bbox_inches="tight")
printStatus("Raw, smoothed, and jerk plot saved.")

#plt.show()

def write_landing_report():
    from pathlib import Path
    report_md_path = Path("landing_report.md")

    raw_peak_row = df.loc[df["absolute_acc"].idxmax()]
    max_abs_jerk_index = jf["acc_abs"].abs().idxmax()
    max_abs_jerk_row = jf.loc[max_abs_jerk_index]

    plot_files = [
        ("Raw acceleration overview", IMAGES_DIR + "acceleration_scatterplots.png"),
        ("Smoothed acceleration overview", IMAGES_DIR + "smoothed_acceleration.png"),
        ("Raw and smoothed comparison", IMAGES_DIR + "combination_plot.png"),
        ("Smoothed acceleration and jerk", IMAGES_DIR + "smoothed_and_jerk_plot.png"),
        ("Full landing analysis", IMAGES_DIR + "raw_smoothed_and_jerk_plot.png"),
    ]

    interpretation = (
        "The landing shows a clear acceleration event around 198 seconds. "
        "The raw signal captures the sharpest instant of impact, while the rolling-smoothed "
        "signal gives a more stable touchdown marker. The jerk signal peaks in the same "
        "time window, which supports the touchdown detection."
    )

    markdown = f"""# Landing Analysis Report

## Summary

This report analyzes phone accelerometer data recorded during an aircraft landing. The data was smoothed with a rolling mean, then used to estimate touchdown timing, dynamic acceleration, jerk, rollout roughness, and an overall landing grade.

## Key Metrics

| Metric | Value |
|---|---:|
| Raw touchdown time | {TOUCHDOWN_TIME_RAW:.2f} s |
| Smoothed touchdown time | {TOUCHDOWN_TIME:.2f} s |
| Raw peak dynamic acceleration | {raw_peak_row["absolute_acc"]:.2f} m/s^2 |
| Smoothed peak dynamic acceleration | {MAX_DYNAMIC_ACCELERATION_MS2:.2f} m/s^2 |
| Smoothed peak dynamic acceleration | {MAX_DYNAMIC_ACCELERATION_G:.2f} g |
| Max absolute jerk | {abs(max_abs_jerk_row["acc_abs"]):.2f} m/s^3 |
| Max absolute jerk time | {max_abs_jerk_row["time"]:.2f} s |
| Rollout roughness score | {ROLLOUT_ROUGHNESS:.2f} |
| Landing grade | {FINAL_LANDING_GRADE:.2f} / 10 |

## Touchdown Detection

Touchdown was estimated from the maximum absolute acceleration. The raw touchdown marker identifies the sharpest measured acceleration spike, while the smoothed touchdown marker uses the rolling-mean signal to reduce sensor noise.

## Jerk And Roughness

Jerk was calculated as the change in acceleration divided by the change in time. The roughness score uses RMS absolute jerk after touchdown, so stronger post-touchdown vibration increases the roughness value.

## Interpretation

{interpretation}

## Generated Plots

"""

    for title, path in plot_files:
        markdown += f"### {title}\n\n![{title}]({path})\n\n"

    report_md_path.write_text(markdown, encoding="utf-8")

    printStatus(f"Landing report saved: {report_md_path}")

printStatus("Creating MD report...")
write_landing_report()

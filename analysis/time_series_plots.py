import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from study_definition_measures import measures


def import_timeseries(column):
    path = f"output/measure_{m.id}.csv"
    df = pd.read_csv(path, usecols=["date", column, m.denominator] + m.group_by)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index(["date"] + m.group_by)
    df = redact_small_numbers(df)
    df = df.unstack(m.group_by)
    df.to_csv(f"output/table_{m.id}.csv")
    df = df[column]
    # Return columns in reverse order
    return df.iloc[:, ::-1]


def redact_small_numbers(df):
    mask_n = df[m.numerator].isin([1, 2, 3, 4, 5])
    mask_d = df[m.denominator].isin([1, 2, 3, 4, 5])
    mask = mask_n | mask_d
    df.loc[mask, :] = np.nan
    return df


def grammar_decider(word):
    if word == "died":
        return "who died"
    return f"with a recorded {word.replace('_', ' ')}"


def line_format(label):
    """
    Convert time label to the format of pandas line plot
    """
    lab = label.month_name()[:3]
    if lab == "Jan":
        lab += f"\n{label.year}"
    if lab == "Feb" and label.year == 2019:
        lab = f"\n{label.year}"
    return lab


def graphing_options(column):
    ax.grid(which="both", axis="y", color="#666666", linestyle="-", alpha=0.2)
    ax.set_title(title, loc="left")
    ax.set_ylim(ymin=0)
    ax.set_ylabel(f"people {grammar_decider(column)}")
    handles, labels = ax.get_legend_handles_labels()
    handles, labels = list(reversed(handles)), list(reversed(labels))
    ax.legend(handles, labels, loc=3, prop={"size": 9}).set_title("")
    ax.set_xticklabels(map(line_format, df.index), rotation="horizontal")
    for (n, l) in enumerate(ax.xaxis.get_ticklabels()):
        if (n > 0) and ((n + 1) % 2 != 0):
            l.set_visible(False)
    ax.xaxis.label.set_visible(False)
    plt.tight_layout()


fig, axes = plt.subplots(ncols=2, nrows=4, sharey=False, figsize=[10, 15])
for i, ax in enumerate(axes.flat):
    m = measures[i]
    df = import_timeseries(m.numerator)
    df.plot(
        kind="bar",
        stacked=True,
        ax=ax,
        width=0.85,
        alpha=0.9,
        color=["#176dde", "#e6e600", "#ffad33"],
    )
    title = f"{chr(97 + i)}) People {grammar_decider(m.numerator)} each month:"
    graphing_options(m.numerator)
plt.savefig("output/event_count_time_series.svg")

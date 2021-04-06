import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from study_definition_measures import measures
from scipy.stats import poisson


def import_timeseries():
    path = f"output/measure_{m.id}.csv"
    table = pd.read_csv(
        path,
        usecols=["date", m.numerator, m.denominator] + m.group_by,
        parse_dates=["date"],
    )
    table = table.set_index(["date"] + m.group_by)
    table = redact_small_numbers(table)
    table = table.unstack(m.group_by)
    table.to_csv(f"output/table_{m.id}.csv")
    out = table[m.numerator]
    # Return columns in reverse order
    return out.iloc[:, ::-1], out.iloc[:, ::-1]


def redact_small_numbers(df):
    mask_n = df[m.numerator].isin([1, 2, 3, 4, 5])
    mask = mask_n
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


def get_ci(df):
    errlo, errhi = poisson.interval(0.95, df)
    errlo = df - errlo
    errhi = errhi - df
    yerr = np.append(errlo, errhi, axis=1).T
    return yerr


def graphing_options(ax):
    ax.grid(which="both", axis="y", color="#666666", linestyle="-", alpha=0.2)
    ax.set_title(title, loc="left")
    ax.set_ylim(ymin=0, ymax=80)
    ax.set_ylabel("Count of people with a recorded code")
    handles, labels = ax.get_legend_handles_labels()
    handles, labels = list(reversed(handles)), list(reversed(labels))
    ax.get_legend().remove()
    ax.set_xticklabels(map(line_format, df.index), rotation="horizontal")
    for (n, l) in enumerate(ax.xaxis.get_ticklabels()):
        if (n > 0) and ((n) % 4 != 0):
            l.set_visible(False)
    ax.xaxis.label.set_visible(False)
    plt.figtext(
        0.05,
        0,
        "I63.6: Cerebral infarction due to cerebral venous thrombosis, nonpyogenic\nI67.6: Nonpyogenic thrombosis of intracranial venous system\nG08: Intracranial and intraspinal phlebitis and thrombophlebitis",
        ha="left",
        va="bottom",
        fontsize=11,
    )
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.2)


titles = ["I63.6 or I67.6", "G08"]

fig, axes = plt.subplots(ncols=2, nrows=1, sharey=False, figsize=[10.5, 4.8])
for i, ax in enumerate(axes.flat):
    m = measures[::-1][i]
    df, totals = import_timeseries()
    df.plot(kind="bar", stacked=True, ax=ax, width=0.9, alpha=0.9)
    # totals.plot(
    #     kind="bar",
    #     ax=ax,
    #     yerr=get_ci(totals),
    #     alpha=0,
    #     label="_nolegend_",
    #     error_kw=dict(alpha=0.4),
    # )
    title = f"{chr(97 + i)}) People with a code for {titles[i]} each month:"
    graphing_options(ax)
plt.savefig("output/event_count_time_series.svg")
